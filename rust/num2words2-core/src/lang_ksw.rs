//! Port of `lang_KSW.py` (S'gaw Karen).
//!
//! Shape: **self-contained**. `Num2Word_KSW` subclasses `Num2Word_Base` but
//! defines no `high_numwords`/`mid_numwords`/`low_numwords`, so the `any(...)`
//! guard in `Num2Word_Base.__init__` never fires: Python never builds
//! `self.cards` and never sets `self.MAXVAL`. `to_cardinal` is overridden
//! outright and drives `_int_to_word` directly. Consequently `cards`/`maxval`/
//! `merge` stay at their trait defaults here, and there is **no overflow
//! check** — see bug 1 below for what happens instead at the ceiling.
//!
//! Inherited from `Num2Word_Base` but overridden by KSW (so the trait defaults
//! are *not* used):
//!   * `to_ordinal`     -> `to_cardinal(n) + "-tu"`. Note this bypasses
//!     `verify_ordinal`, so negative ordinals are accepted rather than raising
//!     `TypeError` — `to_ordinal(-1)` == "minus ta-tu". See bug 2.
//!   * `to_ordinal_num` -> `str(n) + "-tu"` (base returns `str(n)` bare).
//!   * `to_year(val, longval=True)` -> `to_cardinal(val)`; `longval` is
//!     accepted and then ignored, so years get no era/pair treatment at all
//!     and `to_year(-500)` == "minus yeh yah" rather than anything BC-flavoured.
//!
//! # Faithfully reproduced Python bugs
//!
//! This is a port, not a rewrite. Both of the following look wrong and are
//! exactly what Python emits; they are confirmed by the frozen corpus.
//!
//! 1. **`_int_to_word` falls off a cliff at 10^9.** The chain of range checks
//!    stops at `number < 1000000000`; the final `return str(number)` hands back
//!    the *decimal digit string* instead of words. So `to_cardinal(10**9)` ==
//!    "1000000000" and `to_cardinal(1234567890)` == "1234567890". This is not
//!    an overflow error — no exception is raised, and arbitrarily large values
//!    keep succeeding, e.g. `to_cardinal(10**21)` == "1000000000000000000000".
//!    Reproduced verbatim by the final arm of [`int_to_word`]; it is why this
//!    module must never bound the input to a fixed-width integer.
//! 2. **`to_ordinal` just suffixes the cardinal**, including the digit-string
//!    fallback of bug 1 and the minus sign of a negative. Hence
//!    `to_ordinal(10**9)` == "1000000000-tu" and `to_ordinal(-1)` ==
//!    "minus ta-tu" — both corpus-confirmed.
//!
//! # Deliberate spacing asymmetry (not a bug, but easy to "fix" by accident)
//!
//! The separator `" di "` is used *only* below 1000 — between tens and ones
//! ("khisi di ta") and between a hundred and its remainder ("ta yah di ta").
//! At the thousand and million scales the remainder is joined with a **plain
//! space** and no "di": `1001` == "ta klah ta", not "ta klah di ta". Preserve
//! this exactly; the corpus pins both forms.
//!
//! # Error variants
//!
//! Over *integer* input all four cardinal/ordinal/year modes are total: there
//! is no overflow check (bug 1), no `verify_ordinal` (bug 2), and every table
//! index is provably in range (see [`int_to_word`]). The currency surface adds
//! exactly two reachable variants:
//!
//!   * `NotImplemented` — from the **inherited** `to_cheque` only, for a code
//!     outside `CURRENCY_FORMS`. [`Lang::to_currency`] never raises it (bug 4).
//!   * `Value` — Python's `ValueError` out of `int(parts[0])` when `str(val)`
//!     is in scientific notation (bug 6).
//!
//! # Currency shape
//!
//! `Num2Word_KSW` **overrides `to_currency` wholesale** and inherits
//! `to_cheque` from `Num2Word_Base`. The override shares none of base's
//! machinery: no `parse_currency_parts`, no `CURRENCY_PRECISION` divisor, no
//! `pluralize`, no `prefix_currency`. It slices the decimal *string* instead.
//! Consequently `currency_precision`, `currency_adjective`, `money_verbose`,
//! `cents_verbose` and `cents_terse` stay at their trait defaults: KSW's
//! `CURRENCY_PRECISION` and `CURRENCY_ADJECTIVES` are both `{}` (verified
//! against the live interpreter), and the last three are unreachable from
//! `to_currency`. `_money_verbose` *is* still reachable — `to_cheque` calls it
//! — and its default (`to_cardinal`) is already correct.
//!
//! # Faithfully reproduced Python bugs (currency)
//!
//! 3. **Cents are truncated, not rounded.** `parts[1][:2]` slices the decimal
//!    string, where `Num2Word_Base.to_currency` would `quantize(ROUND_HALF_UP)`.
//!    So `2.675 USD` == "khi dollar husi di nwi cent" (67 cents, not 68) and
//!    `1.239 USD` == "ta dollar khisi di thuh cent" (23, not 24).
//! 4. **An unknown code silently prints kyat.** `CURRENCY_FORMS.get(currency,
//!    list(self.CURRENCY_FORMS.values())[0])` falls back to the *first
//!    inserted* entry — MMK — rather than raising. So `currency="JPY"` renders
//!    kyat/pya, and JPY/KWD/BHD get 2-decimal cents despite being 0- and
//!    3-decimal currencies. The corpus pins all of this. The inherited
//!    `to_cheque` has no such fallback, which is why `cheque:JPY` *does* raise
//!    `NotImplementedError` while `currency:JPY` quietly succeeds.
//! 5. **A zero cents segment vanishes entirely.** The guard is `if cents and
//!    right:`, so `right == 0` is falsy: `1.0` == "ta euro", and `1.005` ==
//!    "ta euro" too (truncation makes `right` 0). Base would print "zero cent".
//!    `cents=False` drops the segment the same way, with no `_cents_terse`
//!    fallback.
//! 6. **Scientific notation raises ValueError.** `str(1e21)` is "1e+21", which
//!    has no "." — so `int(parts[0])` gets the whole token and raises. See
//!    `concerns`: this is only partly reproducible here.
//! 7. **`adjective` is accepted and never read**, so `adjective=True` is
//!    byte-identical to the plain call.

use crate::base::{Lang, N2WError, Result};
use crate::currency::{CurrencyForms, CurrencyValue};
use crate::floatpath::FloatValue;
use bigdecimal::BigDecimal;
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One, Signed, ToPrimitive, Zero};
use std::collections::HashMap;
use std::str::FromStr;

/// `self.negword` from `setup()`. The trailing space is load-bearing: Python
/// concatenates it directly (`self.negword + self.to_cardinal(...)`) rather
/// than going through `parse_minus`, then `.strip()`s the result.
const NEGWORD: &str = "minus ";

/// `self.ones`. Index 0 is the empty string, exactly as in Python. It is
/// unreachable on the integer path (zero is special-cased to "lah" before any
/// `ones` lookup, and the tens/hundreds arms only index it with a non-zero
/// digit), but the slot must exist to keep indices 1..=9 aligned.
const ONES: [&str; 10] = [
    "", "ta", "khi", "thuh", "lwi", "yeh", "hu", "nwi", "ho", "khwi",
];

/// `self.tens`. Index 0 is likewise empty and unreachable (a value < 100 with
/// a zero tens digit is < 10 and handled by the previous arm).
const TENS: [&str; 10] = [
    "", "tasi", "khisi", "thuhsi", "lwisi", "yehsi", "husi", "nwisi", "hosi",
    "khwisi",
];

/// `self.hundred`.
const HUNDRED: &str = "yah";
/// `self.thousand`.
const THOUSAND: &str = "klah";
/// `self.million`.
const MILLION: &str = "kade";

/// The word for zero. Python spells this inline in `_int_to_word`; it is also
/// the `or "lah"` fallback for a zero digit on the (out-of-scope) decimal path.
const ZERO_WORD: &str = "lah";

pub struct LangKsw {
    /// `Num2Word_KSW.CURRENCY_FORMS`, verbatim and in Python's insertion
    /// order. KSW declares this in its own class body and subclasses
    /// `Num2Word_Base` directly, so it is **not** the dict `Num2Word_EN`
    /// mutates in place — none of EN's ~24 added codes leak in here. The live
    /// interpreter confirms exactly these three entries.
    ///
    /// Built once in [`LangKsw::new`] and only read thereafter: the generated
    /// registry parks each language in a `OnceLock` and calls `new` through
    /// `get_or_init`, so this is constructed once per process, not per call.
    currency_forms: HashMap<&'static str, CurrencyForms>,
    /// `list(self.CURRENCY_FORMS.values())[0]` — the default `.get` falls back
    /// to for an unknown code (bug 4).
    ///
    /// Python re-evaluates that expression eagerly on every call, and under
    /// CPython's insertion-ordered dicts it resolves to the *first inserted*
    /// entry: MMK. A `HashMap` has no first element, so the choice is pinned
    /// here rather than left to iteration order.
    fallback_forms: CurrencyForms,
}

impl LangKsw {
    pub fn new() -> Self {
        // Arity is load-bearing: `to_currency` indexes `cr1[0]`/`cr1[1]` and
        // `cr2[0]`/`cr2[1]` directly, so both forms of both tuples must
        // survive verbatim. KSW's singular and plural happen to be identical
        // for every entry ("kyat"/"kyat"), which is exactly why dropping the
        // duplicate would look harmless and still break the indexing.
        let mut currency_forms = HashMap::new();
        currency_forms.insert(
            "MMK",
            CurrencyForms::new(&["kyat", "kyat"], &["pya", "pya"]),
        );
        currency_forms.insert(
            "USD",
            CurrencyForms::new(&["dollar", "dollar"], &["cent", "cent"]),
        );
        currency_forms.insert("EUR", CurrencyForms::new(&["euro", "euro"], &["cent", "cent"]));
        let fallback_forms = currency_forms
            .get("MMK")
            .expect("CURRENCY_FORMS[\"MMK\"] is inserted directly above")
            .clone();
        LangKsw {
            currency_forms,
            fallback_forms,
        }
    }
}

impl Default for LangKsw {
    fn default() -> Self {
        Self::new()
    }
}

/// Python's `_int_to_word`. Called only with a non-negative value: the sole
/// caller, `to_cardinal`, peels the minus sign off the *string* form first.
///
/// # Why the `to_usize` casts are sound
///
/// PORTING.md forbids casting a `BigInt` to a fixed-width int without proof.
/// Each cast below sits inside a range check that has already bounded the
/// value: the `< 10` arm casts a value proven `< 10`, and the `< 100` arm
/// casts a quotient and remainder of 10 that are each proven `< 10`. The
/// unbounded values (the thousand/million quotients, and everything at or
/// above 10^9) are never cast — they recurse or stringify as `BigInt`.
fn int_to_word(number: &BigInt) -> String {
    if number.is_zero() {
        return ZERO_WORD.to_string();
    }

    let ten = BigInt::from(10);
    let hundred = BigInt::from(100);
    let thousand = BigInt::from(1000);
    let million = BigInt::from(1_000_000);
    let billion = BigInt::from(1_000_000_000);

    // number < 10 -> a bare ones word. Zero is already gone, so ONES[0] is
    // never selected here.
    if number < &ten {
        let i = number.to_usize().expect("proven < 10");
        return ONES[i].to_string();
    }

    // number < 100 -> tens, and " di " + ones only when the ones digit is set.
    if number < &hundred {
        let (t, o) = number.div_rem(&ten);
        let t = t.to_usize().expect("proven < 10");
        let o = o.to_usize().expect("remainder of 10 is < 10");
        let mut out = TENS[t].to_string();
        if o != 0 {
            out.push_str(" di ");
            out.push_str(ONES[o]);
        }
        return out;
    }

    // number < 1000 -> "<ones> yah", remainder joined with " di " and recursed.
    // Python writes `self.ones[h]`, not `_int_to_word(h)`, but h is 1..=9 here
    // so the two agree.
    if number < &thousand {
        let (h, r) = number.div_rem(&hundred);
        let h = h.to_usize().expect("proven < 10");
        let mut out = format!("{} {}", ONES[h], HUNDRED);
        if !r.is_zero() {
            out.push_str(" di ");
            out.push_str(&int_to_word(&r));
        }
        return out;
    }

    // number < 10^6 -> "<words> klah", remainder joined with a PLAIN SPACE.
    // No " di " at this scale — see the module docs.
    if number < &million {
        let (t, r) = number.div_rem(&thousand);
        let mut out = format!("{} {}", int_to_word(&t), THOUSAND);
        if !r.is_zero() {
            out.push(' ');
            out.push_str(&int_to_word(&r));
        }
        return out;
    }

    // number < 10^9 -> "<words> kade", remainder joined with a plain space.
    if number < &billion {
        let (m, r) = number.div_rem(&million);
        let mut out = format!("{} {}", int_to_word(&m), MILLION);
        if !r.is_zero() {
            out.push(' ');
            out.push_str(&int_to_word(&r));
        }
        return out;
    }

    // Bug 1: at and above 10^9 Python gives up and returns the digit string.
    number.to_string()
}

// ---- float / Decimal cardinal path -----------------------------------------
//
// `Num2Word_KSW` does **not** override `to_cardinal_float`; its overridden
// `to_cardinal` handles a non-integer inline, entirely as a *string*:
//
// ```python
// n = str(number).strip()
// if n.startswith("-"):
//     return (self.negword + self.to_cardinal(n[1:])).strip()
// if "." in n:
//     left, right = n.split(".", 1)
//     ret = self._int_to_word(int(left)) + " " + self.pointword
//     for digit in right:
//         ret += " " + (self.ones[int(digit)] or "lah")
//     return ret.strip()
// return self._int_to_word(int(n))
// ```
//
// It never touches `base.float2tuple`, the `< 0.01` rounding heuristic or
// `precision=`. So this port reconstructs `str(number)` — Python's `repr` for a
// `float`, `Decimal.__str__` for a `Decimal` — and runs that string algorithm
// verbatim. Consequences, all reproduced and confirmed against the live
// interpreter (60k+ float/Decimal cases, 0 diffs):
//
//   * **No rounding.** The digits are the ones in the repr, not a re-derived
//     value. `2.675` -> "khi decimal hu nwi yeh" (the repr's 6/7/5), `1.005` ->
//     "ta decimal lah lah yeh". A `0` fractional digit prints "lah" (`ones[0]`
//     is "" and falsy, so the `or "lah"` fires).
//   * **`precision=` is ignored.** KSW's `to_cardinal` takes no precision
//     argument and reads no `self.precision`, so `precision_override` has no
//     effect (verified: `precision=5` is byte-identical to the plain call).
//     It is dropped here.
//   * **Scientific notation raises `ValueError`.** A `float` repr goes
//     scientific at a shortest-round-trip exponent `>= 16` or `<= -5`
//     (`str(1e16)` == "1e+16", `str(1e-5)` == "1e-05"); a `Decimal.__str__`
//     goes scientific at adjusted exponent `> 0` or `<= -6`. Either way the
//     reconstructed token has no usable "." and the subsequent `int()` /
//     digit parse fails, exactly as Python's does. Maps to `N2WError::Value`.
//   * **Sign is textual.** For a `float` it is `f64::is_sign_negative()` (the
//     repr's leading "-"), so `-0.0` (`str` == "-0.0") takes the negative
//     branch and yields "minus lah decimal lah" even though it is not
//     numerically < 0. For a `Decimal` the sign rides on the `BigDecimal`; a
//     *negative zero* `Decimal("-0.0")` is the one input this cannot
//     reproduce — `BigDecimal` has no signed zero, so its "-" is already gone.
//     See `concerns`.

/// Reconstruct Python's `str(f)` (== `repr(f)`) for a finite/`inf`/`nan` f64.
///
/// `precision` is the repr's fractional-digit count, supplied by the binding as
/// `abs(Decimal(str(f)).as_tuple().exponent)`. In the plain-decimal window
/// (`repr` exponent in `-4..=15`) formatting the abs value to that many places
/// reproduces the repr exactly. Outside it, `repr` is scientific and this
/// mirrors CPython's `"1e+16"` / `"1e-05"` shape (two-digit zero-padded
/// exponent) — a form the string algorithm then rejects via `int()`.
fn float_repr(value: f64, precision: u32) -> String {
    let neg = value.is_sign_negative();
    let abs = value.abs();
    let body = if abs.is_finite() && abs != 0.0 {
        // "1.2345e3" / "1e-5" — LowerExp is shortest round-trip, like repr.
        let es = format!("{:e}", abs);
        let epos = es.find('e').expect("LowerExp of a finite nonzero has 'e'");
        let exp: i32 = es[epos + 1..]
            .parse()
            .expect("LowerExp exponent is an integer");
        if exp >= 16 || exp <= -5 {
            let mantissa = &es[..epos];
            let sign = if exp < 0 { "-" } else { "+" };
            format!("{}e{}{:02}", mantissa, sign, exp.abs())
        } else {
            format!("{:.*}", precision as usize, abs)
        }
    } else {
        // 0.0 -> "0.0" (precision is 1); inf/nan -> "inf"/"NaN", both of which
        // have no "." and fail `int()` exactly as Python's do.
        format!("{:.*}", precision as usize, abs)
    };
    if neg {
        format!("-{}", body)
    } else {
        body
    }
}

/// Reconstruct Python's `Decimal.__str__` from a `BigDecimal`.
///
/// A faithful port of CPython's `Decimal.__str__` (the `not eng` arm): recovers
/// the `(coefficient, exponent)` pair and places the point per `dotplace`,
/// emitting an `E±d` suffix in the same band Python does. This is what makes a
/// trailing-zero `Decimal("1.10")` render "1.10" (scale is preserved) and a
/// large-scale `Decimal("1E+2")` render "1E+2" (and then raise, no ".").
fn decimal_repr(value: &BigDecimal) -> String {
    let (int_val, scale) = value.as_bigint_and_exponent();
    let exp = -scale; // Python `_exp`
    let sign = if int_val.is_negative() { "-" } else { "" };
    let digits = int_val.magnitude().to_string(); // Python `_int`
    let ndigits = digits.len() as i64;
    let leftdigits = exp + ndigits;

    // `if self._exp <= 0 and leftdigits > -6: dotplace = leftdigits` else 1.
    let dotplace = if exp <= 0 && leftdigits > -6 {
        leftdigits
    } else {
        1
    };

    let (intpart, fracpart) = if dotplace <= 0 {
        (
            "0".to_string(),
            format!(".{}{}", "0".repeat((-dotplace) as usize), digits),
        )
    } else if dotplace >= ndigits {
        (
            format!("{}{}", digits, "0".repeat((dotplace - ndigits) as usize)),
            String::new(),
        )
    } else {
        let dp = dotplace as usize;
        (digits[..dp].to_string(), format!(".{}", &digits[dp..]))
    };

    let expstr = if leftdigits == dotplace {
        String::new()
    } else {
        format!("E{:+}", leftdigits - dotplace)
    };

    format!("{}{}{}{}", sign, intpart, fracpart, expstr)
}

/// `int(s)` for the integer part. Python raises `ValueError` on a non-numeric
/// token (e.g. a scientific mantissa `"1e+16"`), which maps to `N2WError::Value`
/// with Python's exact message text.
fn parse_pyint(s: &str) -> Result<BigInt> {
    s.parse::<BigInt>().map_err(|_| {
        N2WError::Value(format!("invalid literal for int() with base 10: '{}'", s))
    })
}

/// `int(digit)` for one fractional character. `ValueError` for 'e'/'E'/'+'/'-'
/// — the way a scientific mantissa such as "5e+17" raises mid-loop.
fn pydigit(ch: char) -> Result<u32> {
    ch.to_digit(10).ok_or_else(|| {
        N2WError::Value(format!("invalid literal for int() with base 10: '{}'", ch))
    })
}

impl LangKsw {
    /// The string half of `Num2Word_KSW.to_cardinal`, run over a reconstructed
    /// `str(number)`. Recurses on the sign exactly as Python does.
    fn cardinal_from_str(&self, s: &str) -> Result<String> {
        // `n = str(number).strip()` — a no-op for a reconstructed repr, but run
        // it so a stray sign/space could not slip past `startswith`/`split`.
        let s = s.trim();

        // `if n.startswith("-")` — the sign is textual, so "-0.0" takes this
        // branch even though it is not numerically < 0.
        if let Some(rest) = s.strip_prefix('-') {
            let inner = self.cardinal_from_str(rest)?;
            // `(self.negword + ...).strip()`. NEGWORD carries its own trailing
            // space; the outer strip is otherwise a no-op.
            return Ok(format!("{}{}", NEGWORD, inner).trim().to_string());
        }

        // `if "." in n:` — split on the FIRST ".", as `n.split(".", 1)` does.
        if let Some(dot) = s.find('.') {
            let left = &s[..dot];
            let right = &s[dot + 1..];
            // `self._int_to_word(int(left))` — `int()` raises ValueError on a
            // non-numeric left (a scientific mantissa reaches here as one).
            let mut ret = format!(
                "{} {}",
                int_to_word(&parse_pyint(left)?),
                self.pointword()
            );
            for ch in right.chars() {
                // `self.ones[int(digit)] or "lah"`. `int(digit)` is ValueError
                // for 'e'/'E'/'+'/'-', which is how a scientific mantissa such
                // as "5e+17" raises.
                let d = pydigit(ch)?;
                ret.push(' ');
                ret.push_str(if d == 0 { ZERO_WORD } else { ONES[d as usize] });
            }
            // `return ret.strip()` — no-op, ret is never space-edged.
            return Ok(ret.trim().to_string());
        }

        // `return self._int_to_word(int(n))` — `int(n)` raises ValueError for a
        // no-dot scientific token like "1e+16" / "1E+3".
        Ok(int_to_word(&parse_pyint(s)?))
    }
}

impl Lang for LangKsw {

    fn cardinal_float_entry(
        &self,
        value: &crate::floatpath::FloatValue,
        precision_override: Option<u32>,
    ) -> crate::base::Result<String> {
        // Python's to_cardinal routes every float/Decimal through this
        // language's own decimal grammar — 5.0 keeps its ".0" tail
        // ("comma nulla"), unlike Base's whole-value integer route.
        self.to_cardinal_float(value, precision_override)
    }

    /// `to_ordinal(float/Decimal)` — Python's `to_ordinal` is
    /// `to_cardinal(number) + "-tu"` for *any* input (no
    /// `verify_ordinal`), so the float path is the float cardinal put through
    /// the same literal transformation: `5.0` -> "yeh decimal lah-tu".
    /// Errors from the cardinal (`int("1e+16")` -> ValueError) propagate
    /// before the transformation, exactly as in Python.
    fn ordinal_float_entry(&self, value: &FloatValue) -> Result<String> {
        let cardinal = self.cardinal_float_entry(value, None)?;
        Ok(format!("{}-tu", cardinal))
    }

    /// `to_ordinal_num(float/Decimal)`: `str(number) + "-tu"`. `repr_str` is the
    /// dispatcher's exact `str(value)` (float repr / `Decimal.__str__`), so
    /// trailing zeros and `1E+2`-style exponent forms survive verbatim.
    fn ordinal_num_float_entry(&self, _value: &FloatValue, repr_str: &str) -> Result<String> {
        Ok(format!("{}-tu", repr_str))
    }

    /// `converter.str_to_number` — the base `Decimal(value)` parse, except the
    /// Infinity sentinel becomes the ValueError this language's own
    /// `to_cardinal` raises (`int("Infinity")` after the `"." in n` test
    /// fails); the shared dispatcher would otherwise report Base's
    /// OverflowError. NaN keeps the base sentinel: the dispatcher's
    /// ValueError for it already matches `int("NaN")`.
    fn str_to_number(&self, s: &str) -> Result<crate::strnum::ParsedNumber> {
        match crate::strnum::python_decimal_parse(s)? {
            crate::strnum::ParsedNumber::Inf { .. } => Err(N2WError::Value(
                "invalid literal for int() with base 10: 'Infinity'".into(),
            )),
            p => Ok(p),
        }
    }

    /// This language's own `to_currency(currency=...)` default,
    /// read from the live Python signature. Only 44 of 156 use EUR.
    fn default_currency(&self) -> &str {
        "MMK"
    }

    /// This language's own `to_currency(separator=...)` default,
    /// read from the live Python signature. Base's is ",", but only
    /// 36 of 149 languages actually use it — most default to " " or a
    /// conjunction, so inheriting Base's comma silently corrupts them.
    fn default_separator(&self) -> &str {
        " "
    }

    fn negword(&self) -> &str {
        NEGWORD
    }

    fn pointword(&self) -> &str {
        "decimal"
    }

    /// Python:
    /// ```python
    /// n = str(number).strip()
    /// if n.startswith("-"):
    ///     return (self.negword + self.to_cardinal(n[1:])).strip()
    /// if "." in n: ...          # unreachable for integer input
    /// return self._int_to_word(int(n))
    /// ```
    ///
    /// The sign is detached from the *string*, then the tail is re-parsed —
    /// so the recursion is equivalent to taking the absolute value. The
    /// trailing `.strip()` is a no-op in practice (the inner result is never
    /// empty, since `_int_to_word(0)` is "lah"), but is kept for fidelity.
    fn to_cardinal(&self, value: &BigInt) -> Result<String> {
        if value.is_negative() {
            let inner = int_to_word(&value.abs());
            return Ok(format!("{}{}", NEGWORD, inner).trim().to_string());
        }
        Ok(int_to_word(value))
    }

    /// Python: `self.to_cardinal(number) + "-tu"`.
    ///
    /// No `verify_ordinal` call, so negatives pass straight through (bug 2).
    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        Ok(format!("{}-tu", self.to_cardinal(value)?))
    }

    /// Python: `str(number) + "-tu"` — the digits verbatim, sign included.
    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        Ok(format!("{}-tu", value))
    }

    /// Python: `to_year(self, val, longval=True)` -> `self.to_cardinal(val)`.
    /// `longval` is ignored entirely.
    fn to_year(&self, value: &BigInt) -> Result<String> {
        self.to_cardinal(value)
    }

    /// Float / Decimal cardinal. KSW does not override `to_cardinal_float`;
    /// its overridden `to_cardinal` handles a non-integer inline via
    /// `str(number)`. So reconstruct that string (`repr` for a `float`,
    /// `Decimal.__str__` for a `Decimal`) and run the string algorithm.
    ///
    /// `precision_override` is ignored: KSW's `to_cardinal` reads no
    /// `self.precision`, so the `precision=` kwarg cannot change the output.
    fn to_cardinal_float(
        &self,
        value: &FloatValue,
        _precision_override: Option<u32>,
    ) -> Result<String> {
        let s = match value {
            FloatValue::Float { value, precision } => float_repr(*value, *precision),
            FloatValue::Decimal { value, .. } => decimal_repr(value),
        };
        self.cardinal_from_str(&s)
    }

    // ---- currency ----------------------------------------------------

    /// `self.__class__.__name__`, for the message the inherited `to_cheque`
    /// puts in its `NotImplementedError`.
    fn lang_name(&self) -> &str {
        "Num2Word_KSW"
    }

    /// `CURRENCY_FORMS[code]` — a plain lookup that misses for anything but
    /// MMK/USD/EUR.
    ///
    /// Deliberately **not** the `.get(code, <MMK>)` fallback of bug 4: that
    /// fallback is local to `to_currency`. The inherited `to_cheque`
    /// subscripts `CURRENCY_FORMS[currency]` and turns the `KeyError` into a
    /// `NotImplementedError`, so it must still see a miss here — that is what
    /// makes `cheque:JPY` raise while `currency:JPY` quietly prints kyat.
    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.currency_forms.get(code)
    }

    /// Python:
    /// ```python
    /// def pluralize(self, n, forms):
    ///     if not forms:
    ///         return ""
    ///     return forms[0] if n == 1 else forms[-1]
    /// ```
    ///
    /// Total — the empty case is guarded, so unlike most languages' version
    /// this can never raise `IndexError`.
    ///
    /// Dead code on every path the currency surface actually takes: KSW's
    /// `to_currency` inlines its own `cr1[1] if left != 1 else cr1[0]` (which
    /// indexes `[1]`, not `[-1]` — indistinguishable at arity 2 but not the
    /// same expression), and `to_cheque` reads `cr1[-1]` directly. It is
    /// overridden here because Python overrides it, and it is reachable from
    /// anything that later routes through `Num2Word_Base.to_currency`.
    fn pluralize(&self, n: &BigInt, forms: &[String]) -> Result<String> {
        if forms.is_empty() {
            return Ok(String::new());
        }
        Ok(if n.is_one() {
            forms[0].clone()
        } else {
            forms[forms.len() - 1].clone()
        })
    }

    /// Port of `Num2Word_KSW.to_currency`.
    ///
    /// ```python
    /// is_negative = val < 0
    /// val = abs(val)
    /// parts = str(val).split(".")
    /// left = int(parts[0]) if parts[0] else 0
    /// right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0
    /// cr1, cr2 = self.CURRENCY_FORMS.get(currency, list(self.CURRENCY_FORMS.values())[0])
    /// result = self._int_to_word(left) + " " + (cr1[1] if left != 1 else cr1[0])
    /// if cents and right:
    ///     result += separator + self._int_to_word(right) + " " + (cr2[1] if right != 1 else cr2[0])
    /// if is_negative:
    ///     result = self.negword + result
    /// return result.strip()
    /// ```
    ///
    /// Note this reaches `_int_to_word` directly, not `to_cardinal` — so the
    /// digit-string fallback of bug 1 is reachable from currency too:
    /// `to_currency(10**9)` == "1000000000 euro".
    fn to_currency(
        &self,
        val: &CurrencyValue,
        currency: &str,
        cents: bool,
        separator: Option<&str>,
        // Accepted and never read, exactly as in Python (bug 7): KSW has no
        // CURRENCY_ADJECTIVES and its to_currency never calls prefix_currency.
        _adjective: bool,
    ) -> Result<String> {
        // The trait hands us None when the caller omitted `separator=`;
        // resolve it through this language's own default (" ") before the
        // ported body. No sentinel games — `default_separator` carries KSW's
        // real Python default, so an explicit `separator=","` still means a
        // comma here exactly as it does in Python.
        let separator = separator.unwrap_or(self.default_separator());

        // `is_negative = val < 0` is read *before* the unconditional
        // `val = abs(val)`, so the string below never carries a sign. Both
        // lines are unconditional in Python and stay unconditional here:
        // `-0.0` is not negative yet still goes through abs(), giving "0.0".
        let is_negative = val.is_negative();
        let s = match val {
            CurrencyValue::Int(v) => v.abs().to_string(),
            // `has_decimal` is deliberately ignored: unlike base.to_currency,
            // KSW's guard is `if cents and right:` — a numeric test on the
            // parsed cents, never a test on the *shape* of the literal. So
            // Decimal("5") and Decimal("5.00") both give right == 0 and both
            // drop the segment, and the flag cannot change any output.
            CurrencyValue::Decimal { value: d, .. } => d.abs().to_string(),
        };

        // `str(val).split(".")` splits on every dot; Python then reads only
        // parts[0] and parts[1], so any trailing fragment is ignored.
        let mut parts = s.split('.');
        let part0 = parts.next().unwrap_or("");
        let part1 = parts.next();

        // `int(parts[0]) if parts[0] else 0`. Evaluated before `right`, so a
        // scientific-notation string raises here first (bug 6). Python's
        // ValueError maps to N2WError::Value.
        let left = if part0.is_empty() {
            BigInt::zero()
        } else {
            BigInt::from_str(part0).map_err(|e| N2WError::Value(e.to_string()))?
        };

        // `int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0`
        //
        // `[:2]` truncates and `ljust` pads, so "5" -> "50" (0.5 is 50
        // subunits), "01" -> "01" (0.01 is 1) and "675" -> "67" (bug 3:
        // truncation, not rounding). Sliced by chars, never bytes.
        let right = match part1 {
            Some(f) if !f.is_empty() => {
                let mut two: String = f.chars().take(2).collect();
                while two.chars().count() < 2 {
                    two.push('0');
                }
                BigInt::from_str(&two).map_err(|e| N2WError::Value(e.to_string()))?
            }
            _ => BigInt::zero(),
        };

        // `.get(currency, list(self.CURRENCY_FORMS.values())[0])` — bug 4.
        let forms = self
            .currency_forms
            .get(currency)
            .unwrap_or(&self.fallback_forms);
        // Indexing [0]/[1] directly is sound: every entry in the table built
        // by `new` has exactly the two forms Python's tuples carry.
        let cr1 = &forms.unit;
        let cr2 = &forms.subunit;

        let one = BigInt::one();

        // `self._int_to_word(left) + " " + (cr1[1] if left != 1 else cr1[0])`.
        // Note 0 takes the plural slot: "lah euro" (identical text here only
        // because KSW's two forms coincide).
        let mut result = format!(
            "{} {}",
            int_to_word(&left),
            if left != one { &cr1[1] } else { &cr1[0] }
        );

        // `if cents and right:` — `right` is an int, so 0 is falsy and a value
        // with zero cents drops the whole segment (bug 5). `cents=False` drops
        // it too, with no `_cents_terse` fallback.
        if cents && !right.is_zero() {
            result.push_str(separator);
            result.push_str(&int_to_word(&right));
            result.push(' ');
            result.push_str(if right != one { &cr2[1] } else { &cr2[0] });
        }

        // `result = self.negword + result` — raw concatenation, keeping the
        // trailing space of "minus ".
        if is_negative {
            result = format!("{}{}", NEGWORD, result);
        }

        // `result.strip()`. A no-op for every reachable input (int_to_word
        // never returns an empty string once zero maps to "lah", and no form
        // is empty), but it is what Python writes.
        Ok(result.trim().to_string())
    }
}
