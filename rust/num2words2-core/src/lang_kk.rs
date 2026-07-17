//! Port of `lang_KK.py` (Kazakh).
//!
//! Shape: **self-contained**. `Num2Word_KK` subclasses `Num2Word_Base` but
//! defines no `high_numwords`/`mid_numwords`/`low_numwords` and no
//! `set_high_numwords`, so Python never populates `self.cards` and never sets
//! `MAXVAL`. `to_cardinal` is overridden outright and delegates to a hand
//! written `_int_to_word` recursion. `cards`/`maxval`/`merge` therefore stay
//! at their trait defaults here and are never reached — there is no overflow
//! check at all (see bug 3 below for what happens instead).
//!
//! `Num2Word_KK` overrides every in-scope entry point (`to_cardinal`,
//! `to_ordinal`, `to_ordinal_num`, `to_year`), so nothing is inherited from
//! `Num2Word_Base` on the four supported paths. `setup()` only assigns the
//! word tables reproduced below; the base `__init__` work (`self.cards`,
//! `self.MAXVAL`, `self.title`) is inert for this language.
//!
//! # Faithfully reproduced Python bugs
//!
//! This is a port, not a rewrite. All of the following look wrong and are
//! nevertheless exactly what Python emits — every one is pinned by the frozen
//! corpus:
//!
//! 1. **`to_cardinal(0)` == `"zero"`, in English.** `_int_to_word` opens with
//!    `return self.ones[0] if self.ones[0] else "zero"`. `ones[0]` is the
//!    empty string (a placeholder so that `ones[n]` indexes by digit), which
//!    is falsy, so the `else` branch always wins and the Kazakh converter
//!    answers with the English word. The Kazakh "нөл" appears nowhere in the
//!    module. Hence `to_ordinal(0)` == `"zero-інші"`.
//! 2. **`negword` is `"minus "`, also English** (not "минус"), so
//!    `to_cardinal(-1)` == `"minus бір"`. Likewise `pointword` is `"point"`.
//! 3. **Numbers >= 10^9 are returned as bare digits.** `_int_to_word`'s final
//!    `else` is `return str(number)` — commented "Fallback for very large
//!    numbers" — so `to_cardinal(10**9)` == `"1000000000"` and
//!    `to_ordinal(10**9)` == `"1000000000-інші"`. This is the de facto ceiling
//!    of the language: no `OverflowError` is ever raised, the digits just leak
//!    through. `billion`/`trillion` are never defined. The fallback prints the
//!    *absolute* value, because `to_cardinal` strips the sign before calling
//!    in, so `to_cardinal(-10**9)` == `"minus 1000000000"`.
//! 4. **100 is `"бір жүз"`, not `"жүз"`.** The `number < 1000` branch is
//!    unconditionally `self.ones[hundreds_val] + " " + self.hundred`, with no
//!    `hundreds_val == 1` special case, so the leading "бір" ("one") is always
//!    emitted. Natural Kazakh would say plain "жүз". Same for `1000` →
//!    `"бір мың"` (via the `_int_to_word(1)` recursion on the thousands part).
//!
//! # No overflow, no errors (integers) — one ValueError (floats)
//!
//! Nothing on the four *integer* paths can raise: `_int_to_word` indexes
//! `ones`/`tens` only with a digit it just computed by `% 10` or `// 100`, and
//! every value too large for the tables hits the `str(number)` fallback. The
//! frozen corpus agrees — no `err` row exists for kk on cardinal/ordinal/
//! ordinal_num/year with integer input. All four functions return `Ok` for
//! every `BigInt`.
//!
//! The **float/Decimal** path has exactly one raising surface: `to_cardinal`
//! re-parses the sign-stripped `str(number)` with `int()`, so any point-less
//! form that is not an integer literal — `repr(1e16)` == "1e+16",
//! `str(Decimal("1E+2"))` == "1E+2", "inf"/"nan"/"Infinity" — raises
//! `ValueError: invalid literal for int() with base 10: '...'`. Pointed forms
//! never raise, whatever their size (the >= 10^9 integer part just leaks
//! digits, bug 3). Pinned by the wholefloat corpus: ValueError rows for
//! 1e+16/1e+20/1E+2/1E+20 across cardinal/ordinal/year, `ok` rows for every
//! pointed form including "-0.0" -> "minus zero point zero". See
//! [`route_by_str`].
//!
//! # Currency
//!
//! `Num2Word_KK` overrides `to_currency` outright — `Num2Word_Base`'s version,
//! and with it `parse_currency_parts`, `pluralize`, `CURRENCY_PRECISION` and
//! `CURRENCY_ADJECTIVES`, is unreachable — but inherits `to_cheque` unchanged.
//! The two therefore disagree about unknown codes, which is the single most
//! important thing about this surface: `to_currency` *falls back* to KZT and
//! never raises, while `to_cheque` raises `NotImplementedError`. See the four
//! further reproduced bugs (5-9) documented on `to_currency` itself.
//!
//! The method is character-for-character the same as `Num2Word_FO`'s,
//! `Num2Word_BR`'s and several others' — a copy-paste family whose shared
//! quirks (string-surgery cent split, the eager `.get(..., values()[0])`
//! default, the ignored `adjective`) are ported identically across those
//! files.

use crate::base::{Lang, N2WError, Result};
use crate::currency::{CurrencyForms, CurrencyValue};
use crate::floatpath::FloatValue;
use crate::strnum::{python_decimal_parse, python_decimal_str, ParsedNumber};
use bigdecimal::BigDecimal;
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One, Signed, ToPrimitive, Zero};
use std::collections::HashMap;

/// `self.negword`. English, verbatim from Python — see module bug 2.
const NEGWORD: &str = "minus ";

/// `self.ones`. Index 0 is the empty string; `_int_to_word` never reaches it
/// via the digit paths (they are guarded by `if ones_val == 0` / `if
/// remainder`), and the `number == 0` path turns it into "zero" (bug 1).
const ONES: [&str; 10] = [
    "", "бір", "екі", "үш", "төрт", "бес", "алты", "жеті", "сегіз", "тоғыз",
];

/// `self.tens`. Index 0 is the empty string and is unreachable: the `number <
/// 100` branch is only entered when `number >= 10`, so `tens_val >= 1`.
const TENS: [&str; 10] = [
    "", "он", "жиырма", "отыз", "қырық", "елу", "алпыс", "жетпіс", "сексен", "тоқсан",
];

/// `self.hundred`.
const HUNDRED: &str = "жүз";
/// `self.thousand`.
const THOUSAND: &str = "мың";
/// `self.million`.
const MILLION: &str = "миллион";

/// `self.to_ordinal`'s suffix, appended to the cardinal with a literal hyphen.
const ORDINAL_SUFFIX: &str = "-інші";

/// `self.__class__.__name__`, for the `NotImplementedError` message that
/// `Num2Word_Base.to_cheque` raises on an unknown code.
const LANG_NAME: &str = "Num2Word_KK";

/// `Num2Word_KK.to_currency`'s own default: `separator=" "`, a bare space —
/// *not* `Num2Word_Base`'s `","`.
const SEPARATOR_DEFAULT: &str = " ";

/// The separator the pyo3 binding hands us when the Python caller omitted one.
///
/// `Num2Word_KK.to_currency` declares `separator=" "` in its own signature, but
/// the `Lang` trait carries no per-language parameter defaults, and both
/// `__init__.py`'s currency fast path and `bench/diff_test.py` substitute
/// `kwargs.get("separator", ",")` — **`Num2Word_Base`'s** default, not KK's —
/// before the value crosses the boundary. By then "caller omitted separator"
/// and "caller explicitly passed a comma" are the same `&str`, and the
/// information needed to tell them apart no longer exists on this side.
///
/// So `,` is read back as the unset sentinel and KK's own default restored.
/// This is the only reading the oracle supports: every float row of the `kk`
/// currency corpus was generated by `num2words(v, lang="kk", to="currency",
/// currency=c)` with no `separator=`, which reaches `Num2Word_KK.to_currency`
/// with its *own* default, and every one of them expects a bare space
/// ("он екі euros отыз төрт cents", not "он екі euros,отыз төрт cents").
///
/// The cost is narrow and known: a caller who *explicitly* passes
/// `separator=","` gets " " where Python would give ",". Expressing that case
/// needs `Option<&str>` in the trait signature, which lives in `base.rs` —
/// outside this port's remit. Flagged in the port report. `lang_fo.rs`,
/// `lang_br.rs`, `lang_bs.rs` and `lang_ba.rs` resolve the identical conflict
/// the same way; `lang_FO.py`'s `to_currency` is character-for-character the
/// same method as this one.
const SEPARATOR_UNSET: &str = ",";

/// `to_currency`'s fallback code — see currency bug 5.
///
/// Python spells it `list(self.CURRENCY_FORMS.values())[0]`, i.e. "whichever
/// entry was inserted first". `CURRENCY_FORMS` is a dict literal ordered
/// `KZT, USD, EUR` and dicts preserve insertion order, so that is KZT. Pinning
/// the *key* rather than reproducing a positional lookup keeps the intent
/// legible; a `HashMap` has no insertion order to index into anyway.
///
/// Verified against the live interpreter rather than read off the source:
/// `list(CONVERTER_CLASSES["kk"].CURRENCY_FORMS.keys())` == `['KZT', 'USD',
/// 'EUR']`. Nothing mutates this dict — `Num2Word_KK` declares its own
/// `CURRENCY_FORMS` and inherits from `Num2Word_Base`, not `Num2Word_EUR`, so
/// the `Num2Word_EN.__init__` shared-dict rewrite documented in
/// PORTING_CURRENCY.md does not reach it (`c.CURRENCY_FORMS is
/// CONVERTER_CLASSES['en'].CURRENCY_FORMS` is `False`).
const FALLBACK_CURRENCY: &str = "KZT";

/// The hard-coded 2 in `parts[1][:2].ljust(2, "0")` — see currency bug 6.
const CENT_DIVISOR: i64 = 100;

/// Python's `int(s)` failure, message verbatim from CPython. `s` is the
/// point-less `str(number)` slice `to_cardinal` feeds it — sign already
/// stripped, because the leading "-" is peeled off the string before `int()`
/// ever runs.
fn int_value_error(s: &str) -> N2WError {
    N2WError::Value(format!("invalid literal for int() with base 10: '{}'", s))
}

/// Python `repr(float)` for the scientific range, on an already-`abs()`ed
/// finite f64 (`a >= 1e16`, or `0 < a < 1e-4`).
///
/// Rust's `{:e}` yields the shortest round-trip mantissa — the same digits
/// CPython's repr picks — but lays the exponent out as `1e16` / `1e-5` where
/// Python writes `1e+16` / `1e-05`: always a sign, zero-padded to two digits.
/// Only the exponent dressing needs fixing up. (Same helper as `lang_ky.rs`
/// and `lang_fo.rs`; `lang_KK.py`'s `to_cardinal` is character-for-character
/// the same method.)
fn py_float_sci_repr(a: f64) -> String {
    let sci = format!("{:e}", a); // "1e16", "1.5e20", "1e-5"
    let (mant, exp_str) = sci.split_once('e').expect("{:e} always emits an 'e'");
    let exp: i64 = exp_str.parse().expect("{:e} exponent is a base-10 integer");
    format!(
        "{}e{}{:02}",
        mant,
        if exp < 0 { '-' } else { '+' },
        exp.abs()
    )
}

/// Where `str(number)` sends the value in `to_cardinal` (sign already peeled).
enum StrRoute {
    /// `"." in n` — the decimal grammar spells every fractional character.
    Point,
    /// No "." and `int(n)` succeeds — `_int_to_word` runs on this magnitude.
    WholeDigits(BigInt),
}

/// Reproduce Python's `"." in str(number)` routing, including the `int(n)`
/// `ValueError` for the point-less forms that are not integer literals.
///
/// * **Float** — repr is fixed-notation (always with a ".") for every finite
///   value outside the scientific range, so the only no-point floats are the
///   scientific ones (`|v| >= 1e16`, `0 < |v| < 1e-4`) and inf/nan — all of
///   which make `int()` raise. `FloatValue::has_visible_point` is *not* used
///   here: it reports `true` for tiny scientific floats (`1e-05`), whose repr
///   has no point and must raise.
/// * **Decimal** — `str(Decimal)` is reconstructed by `python_decimal_str`;
///   a point routes to the decimal grammar, plain digits (canonical integral
///   Decimals like "100") parse, and everything else ("1E+2", "1E+20") is the
///   `int()` ValueError.
fn route_by_str(v: &FloatValue) -> Result<StrRoute> {
    match v {
        FloatValue::Float { value, .. } => {
            let a = value.abs();
            if !a.is_finite() {
                // str(float("inf")) == "inf", str(float("nan")) == "nan" —
                // no ".", so int() raises. The "-" of "-inf" is stripped by
                // the string-sign peel before int() ever sees it.
                return Err(int_value_error(if a.is_nan() { "nan" } else { "inf" }));
            }
            if a >= 1e16 || (a > 0.0 && a < 1e-4) {
                // repr picked exponent form: no "." in n -> int(n) raises.
                return Err(int_value_error(&py_float_sci_repr(a)));
            }
            // Every other finite float reprs with a point ("5.0", "0.0001").
            Ok(StrRoute::Point)
        }
        FloatValue::Decimal { value, .. } => {
            // abs() first: Python strips the string sign before this test.
            let s = python_decimal_str(&value.abs());
            if s.contains('.') {
                Ok(StrRoute::Point)
            } else if !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit()) {
                Ok(StrRoute::WholeDigits(s.parse().expect("digits only")))
            } else {
                // "1E+2", "1E+20", ... — int() raises.
                Err(int_value_error(&s))
            }
        }
    }
}

/// Python's `setup()` only assigns constant word tables, which are module-level
/// `const`s here. The one piece of real state is `CURRENCY_FORMS`.
pub struct LangKk {
    /// `Num2Word_KK.CURRENCY_FORMS`.
    ///
    /// Built once in [`LangKk::new`] and stored, never per call: the binding
    /// holds the converter in a `OnceLock`, so this table is constructed
    /// exactly once per process.
    ///
    /// Each entry is a 2-tuple of 2-tuples, `((unit_sg, unit_pl), (sub_sg,
    /// sub_pl))`. The arity is load-bearing even where the two forms are
    /// spelled identically (KZT's "теңге"/"теңге"): `to_currency` indexes `[1]`
    /// for the plural and `Num2Word_Base.to_cheque` takes `cr1[-1]`, so both
    /// slots must exist.
    currency_forms: HashMap<&'static str, CurrencyForms>,
}

impl Default for LangKk {
    fn default() -> Self {
        Self::new()
    }
}

impl LangKk {
    pub fn new() -> Self {
        // Insertion order is irrelevant to a HashMap; FALLBACK_CURRENCY
        // captures the one place Python's ordering was observable.
        let currency_forms: HashMap<&'static str, CurrencyForms> = [
            ("KZT", &["теңге", "теңге"][..], &["тиын", "тиын"][..]),
            ("USD", &["dollar", "dollars"][..], &["cent", "cents"][..]),
            ("EUR", &["euro", "euros"][..], &["cent", "cents"][..]),
        ]
        .into_iter()
        .map(|(k, u, s)| (k, CurrencyForms::new(u, s)))
        .collect();
        LangKk { currency_forms }
    }

    /// The `(left, right)` split at the head of `Num2Word_KK.to_currency`, for
    /// a value already made non-negative.
    ///
    /// Python works on the *string*:
    ///
    /// ```python
    /// parts = str(val).split(".")
    /// left = int(parts[0]) if parts[0] else 0
    /// right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0
    /// ```
    ///
    /// Taking the first two fractional digits and right-padding to two is
    /// exactly `trunc(frac * 100)` for any plain decimal string — `"5"` →
    /// `"50"` → 50 is `trunc(0.5 * 100)`, `"345"` → `"34"` is
    /// `trunc(0.345 * 100)` — so this computes the split arithmetically rather
    /// than round-tripping the value back through `BigDecimal`'s `Display`,
    /// which switches to exponential form on its own thresholds and is not a
    /// formatting impl this port controls. (`lang_fo.rs` and `lang_eu.rs` port
    /// the same idiom the same way.)
    ///
    /// `with_scale(0)` truncates (it divides the underlying `BigInt`), which is
    /// what `int()` does, and both operands are non-negative here, so floor and
    /// truncation agree.
    ///
    /// A true `int` has no "." in `str(val)`, so `len(parts) > 1` is false and
    /// `right` is 0 — which is also what `frac == 0` gives here. KK therefore
    /// needs no `isinstance(val, int)` branch: currency bug 7 means the
    /// int/float distinction is invisible in this language's output.
    fn split_currency(val: &CurrencyValue) -> (BigInt, BigInt) {
        match val {
            CurrencyValue::Int(i) => (i.abs(), BigInt::zero()),
            CurrencyValue::Decimal { value: d, .. } => {
                let abs = d.abs();
                // int(parts[0]) — truncation toward zero; abs is non-negative.
                let left = abs.with_scale(0).as_bigint_and_exponent().0;
                let frac = &abs - BigDecimal::from(left.clone());
                let right = (frac * BigDecimal::from(CENT_DIVISOR))
                    .with_scale(0)
                    .as_bigint_and_exponent()
                    .0;
                (left, right)
            }
        }
    }

    /// Python's `_int_to_word`.
    ///
    /// Kept as a direct transcription, including the unreachable arms, so the
    /// correspondence with the source stays checkable. Cannot fail.
    fn int_to_word(&self, number: &BigInt) -> String {
        // `if number == 0: return self.ones[0] if self.ones[0] else "zero"`
        // ONES[0] is "" → falsy → always the English "zero". See bug 1.
        if number.is_zero() {
            return if ONES[0].is_empty() {
                "zero".to_string()
            } else {
                ONES[0].to_string()
            };
        }

        // `if number < 0: return self.negword + self._int_to_word(abs(number))`
        // Dead code in practice: `to_cardinal` strips the sign from the string
        // before parsing, so a negative never reaches here. Ported anyway.
        if number.is_negative() {
            return format!("{}{}", NEGWORD, self.int_to_word(&number.abs()));
        }

        let ten = BigInt::from(10);
        let hundred = BigInt::from(100);
        let thousand = BigInt::from(1_000);
        let million = BigInt::from(1_000_000);
        let billion = BigInt::from(1_000_000_000);

        if number < &ten {
            // 1..=9, so the cast and the index are both in range.
            return ONES[number.to_usize().unwrap()].to_string();
        }

        if number < &hundred {
            // Python: `number // 10`, `number % 10`. `number` is positive here,
            // so floor-division and truncating division agree; div_rem is safe.
            let (tens_val, ones_val) = number.div_rem(&ten);
            let t = TENS[tens_val.to_usize().unwrap()]; // 1..=9
            let o = ones_val.to_usize().unwrap(); // 0..=9
            return if o == 0 {
                t.to_string()
            } else {
                format!("{} {}", t, ONES[o])
            };
        }

        if number < &thousand {
            let (hundreds_val, remainder) = number.div_rem(&hundred);
            // No `hundreds_val == 1` special case in Python → "бір жүз". Bug 4.
            let mut result = format!("{} {}", ONES[hundreds_val.to_usize().unwrap()], HUNDRED);
            if !remainder.is_zero() {
                result.push(' ');
                result.push_str(&self.int_to_word(&remainder));
            }
            return result;
        }

        if number < &million {
            let (thousands_val, remainder) = number.div_rem(&thousand);
            let mut result = format!("{} {}", self.int_to_word(&thousands_val), THOUSAND);
            if !remainder.is_zero() {
                result.push(' ');
                result.push_str(&self.int_to_word(&remainder));
            }
            return result;
        }

        if number < &billion {
            let (millions_val, remainder) = number.div_rem(&million);
            let mut result = format!("{} {}", self.int_to_word(&millions_val), MILLION);
            if !remainder.is_zero() {
                result.push(' ');
                result.push_str(&self.int_to_word(&remainder));
            }
            return result;
        }

        // `return str(number)  # Fallback for very large numbers`. See bug 3.
        number.to_string()
    }
}

impl Lang for LangKk {
    /// This language's own `to_currency(currency=...)` default,
    /// read from the live Python signature. Only 44 of 156 use EUR.
    fn default_currency(&self) -> &str {
        "KZT"
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
        "point"
    }

    /// Python's `to_cardinal`.
    ///
    /// The original round-trips through the decimal string (`n =
    /// str(number).strip()`) to split off the sign and a possible fractional
    /// part. For integral input the `"." in n` branch is unreachable, so this
    /// reproduces only the `else` arm — sign strip, `int(n)`, `_int_to_word`,
    /// then a final `.strip()`.
    fn to_cardinal(&self, value: &BigInt) -> Result<String> {
        let n = value.to_string(); // already stripped: no stray whitespace
        let (ret, digits) = match n.strip_prefix('-') {
            Some(rest) => (NEGWORD, rest),
            None => ("", n.as_str()),
        };

        // `int(n)` on the sign-stripped digits — the magnitude. Cannot fail:
        // `BigInt::to_string` always yields a parseable decimal literal, and
        // it is never the bare "-" that trips other languages up.
        let parsed: BigInt = digits.parse().unwrap_or_else(|_| BigInt::zero());

        // `(ret + self._int_to_word(int(n))).strip()`
        Ok(format!("{}{}", ret, self.int_to_word(&parsed))
            .trim()
            .to_string())
    }

    /// Python: `return self.to_cardinal(number) + "-інші"`.
    ///
    /// A flat suffix with no agreement, no stem change, and no zero/negative
    /// guard — hence `"zero-інші"` and `"minus бір-інші"`, and, above 10^9,
    /// `"1000000000-інші"`.
    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        Ok(format!("{}{}", self.to_cardinal(value)?, ORDINAL_SUFFIX))
    }

    /// Python: `return str(number) + "."` — the sign survives ("-1.").
    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        Ok(format!("{}.", value))
    }

    /// Python: `def to_year(self, val, longval=True): return
    /// self.to_cardinal(val)`. `longval` is accepted and ignored, and there is
    /// no century/"hundred" pairing — 1905 is "бір мың тоғыз жүз бес", i.e.
    /// plain 1905, not "nineteen oh five".
    fn to_year(&self, value: &BigInt) -> Result<String> {
        self.to_cardinal(value)
    }

    /// Port of the float/Decimal path of `Num2Word_KK.to_cardinal`.
    ///
    /// KK does **not** inherit `Num2Word_Base.to_cardinal_float`/`float2tuple`.
    /// It overrides `to_cardinal(number)`, which operates on `str(number)`:
    ///
    /// ```python
    /// n = str(number).strip()
    /// if n.startswith("-"):
    ///     n = n[1:]; ret = self.negword
    /// else:
    ///     ret = ""
    /// if "." in n:
    ///     left, right = n.split(".", 1)
    ///     ret += self._int_to_word(int(left)) + " " + self.pointword + " "
    ///     for digit in right:
    ///         ret += self._int_to_word(int(digit)) + " "
    ///     return ret.strip()
    /// ```
    ///
    /// The fractional part is read **digit by digit off the decimal string**,
    /// so the `float2tuple` f64-artefact heuristic never applies here: `2.675`
    /// becomes `str` `"2.675"` → `"алты жеті бес"` directly, with no
    /// `674.999…` to rescue. Reproduce that by rebuilding the repr string, not
    /// by arithmetic on the raw double (which *would* reintroduce the artefact).
    ///
    /// * **Float** — Rust's `{}` drops the `.0` on whole floats (`1.0` → "1"),
    ///   so the repr is reconstructed with `{:.precision$}` on the absolute
    ///   value. `precision` is the repr-derived fractional length (== Python's
    ///   `abs(Decimal(str(v)).as_tuple().exponent)`), and formatting the double
    ///   back to that many places recovers exactly the shortest-round-trip
    ///   digits (verified: `2.675` → "2.675", `1.005` → "1.005", `1.0` →
    ///   "1.0").
    /// * **Decimal** — reconstructed arithmetically (exact): `int(left)` is the
    ///   truncated integer part, and the fractional digits are
    ///   `(abs - left) * 10**precision` left-padded to `precision`. This keeps
    ///   trailing zeros the way `str(Decimal("1.10"))` does ("1.10" → "10") and
    ///   stays exact at trillion scale (`98746251323029.99`, issue #603), where
    ///   `int(left)` overflows KK's `_int_to_word` word tables and leaks through
    ///   as bare digits (module bug 3).
    ///
    /// The integer part `int(left)` runs back through KK's `int_to_word`, so
    /// module bugs 1/3/4 all reach here: `0.x` → "zero point …" (English
    /// "zero", bug 1), `100.5` → "бір жүз point …" (bug 4), and integer parts
    /// ≥ 10^9 render as raw digits (bug 3).
    ///
    /// `precision_override` (the `precision=` kwarg, issue #580) is **inert**
    /// for KK: `to_cardinal` takes no such parameter, so the kwarg is dropped
    /// before it can matter. Verified live:
    /// `num2words(0.5, lang="kk", precision=3)` == "zero point бес".
    fn to_cardinal_float(
        &self,
        value: &FloatValue,
        _precision_override: Option<u32>,
    ) -> Result<String> {
        // Rebuild `n` (already sign-stripped) as "<left>.<right>" with exactly
        // `precision` fractional digits — or no "." when precision is 0, which
        // mirrors Python's `if "." in n` guard falling through to the integer
        // branch. `neg` mirrors `str(number).startswith("-")`.
        let (neg, left, right_str) = match value {
            FloatValue::Float { value, precision } => {
                // Sign *bit*, not `< 0.0`: repr(-0.0) is "-0.0", so Python's
                // startswith("-") is true and KK answers "minus zero point
                // zero". A `< 0.0` test would drop the minus.
                let neg = value.is_sign_negative();
                let prec = *precision as usize;
                let s = format!("{:.p$}", value.abs(), p = prec);
                match s.split_once('.') {
                    Some((l, r)) => (
                        neg,
                        l.parse::<BigInt>().unwrap_or_else(|_| BigInt::zero()),
                        r.to_string(),
                    ),
                    None => (
                        neg,
                        s.parse::<BigInt>().unwrap_or_else(|_| BigInt::zero()),
                        String::new(),
                    ),
                }
            }
            FloatValue::Decimal { value, precision } => {
                let neg = value.is_negative();
                let abs = value.abs();
                // int(left) — truncate the absolute value toward zero.
                let left = abs.with_scale(0).as_bigint_and_exponent().0;
                if *precision == 0 {
                    (neg, left, String::new())
                } else {
                    let frac = &abs - BigDecimal::from(left.clone());
                    let scale = BigInt::from(10).pow(*precision);
                    let right = (frac * BigDecimal::from(scale))
                        .with_scale(0)
                        .as_bigint_and_exponent()
                        .0;
                    // Left-pad to `precision` digits (right is non-negative and
                    // < 10**precision, so this never truncates). Manual pad
                    // rather than a numeric fill so BigInt's Display is used
                    // verbatim.
                    let rs = right.to_string();
                    let pad = (*precision as usize).saturating_sub(rs.len());
                    (neg, left, format!("{}{}", "0".repeat(pad), rs))
                }
            }
        };

        // ret += _int_to_word(int(left)) [+ " point " + per-digit words];
        // strip. `pointword` ("point") is used raw — KK's `to_cardinal` applies
        // no title() here (and is_title is false anyway).
        let mut tokens: Vec<String> = vec![self.int_to_word(&left)];
        if !right_str.is_empty() {
            tokens.push(self.pointword().to_string());
            for ch in right_str.chars() {
                // Each char is one decimal digit; int(digit) ∈ 0..=9.
                let d = ch.to_digit(10).unwrap_or(0);
                tokens.push(self.int_to_word(&BigInt::from(d)));
            }
        }
        let joined = tokens.join(" ");
        // negword ("minus ") is prepended raw, then the whole thing stripped —
        // exactly Python's `ret = self.negword + ...; return ret.strip()`.
        let result = if neg {
            format!("{}{}", NEGWORD, joined)
        } else {
            joined
        };
        Ok(result.trim().to_string())
    }

    /// `to_cardinal(float/Decimal)` — the full entry, routing on
    /// `"." in str(number)` rather than on whole-ness (Base's
    /// `int(value) == value` test never runs; KK overrides `to_cardinal`
    /// outright).
    ///
    /// A whole float therefore keeps its ".0" tail (`5.0` -> "бес point
    /// zero", `-0.0` -> "minus zero point zero"), a point-less integral
    /// Decimal takes the integer grammar (`Decimal("100")` -> "бір жүз"),
    /// and a point-less non-integer form is Python's `int()` ValueError
    /// (`1e+16`, `Decimal("1E+2")`).
    ///
    /// `precision_override` is threaded through untouched; KK's grammar never
    /// reads a precision, so it is inert either way (see `to_cardinal_float`).
    fn cardinal_float_entry(
        &self,
        value: &FloatValue,
        precision_override: Option<u32>,
    ) -> Result<String> {
        match route_by_str(value)? {
            StrRoute::Point => self.to_cardinal_float(value, precision_override),
            StrRoute::WholeDigits(abs_int) => {
                // `(ret + self._int_to_word(int(n))).strip()`, with the sign
                // already peeled off the string into `ret = self.negword`.
                let body = self.int_to_word(&abs_int);
                if value.is_negative() {
                    Ok(format!("{}{}", NEGWORD, body).trim().to_string())
                } else {
                    Ok(body)
                }
            }
        }
    }

    /// `to_ordinal(float/Decimal)`: `self.to_cardinal(number) + "-інші"` —
    /// the same blind suffix as the integer path, so `5.0` == "бес point
    /// zero-інші" and the ValueError of `1e+16` propagates unchanged.
    fn ordinal_float_entry(&self, value: &FloatValue) -> Result<String> {
        Ok(format!(
            "{}{}",
            self.cardinal_float_entry(value, None)?,
            ORDINAL_SUFFIX
        ))
    }

    /// `to_ordinal_num(float/Decimal)`: `str(number) + "."`. Purely textual —
    /// nothing is parsed, so even the scientific forms succeed: `1e+16` ==
    /// "1e+16." and `Decimal("1E+2")` == "1E+2.".
    fn ordinal_num_float_entry(&self, _value: &FloatValue, repr_str: &str) -> Result<String> {
        Ok(format!("{}.", repr_str))
    }

    // `year_float_entry` is deliberately NOT overridden: KK's `to_year` is
    // `return self.to_cardinal(val)`, and the trait default routes through
    // the overridden `cardinal_float_entry` above — so `to_year(5.0)` ==
    // "бес point zero" and `to_year(1e+16)` raises ValueError, as the
    // corpus pins.

    /// `converter.str_to_number` — Base's `Decimal(value)`, which KK does not
    /// override. Inf/NaN parse fine here; the per-mode behaviour is served
    /// natively by [`Lang::inf_result`] / [`Lang::nan_result`] below.
    fn str_to_number(&self, s: &str) -> Result<ParsedNumber> {
        python_decimal_parse(s)
    }

    /// `Decimal('Infinity')` / `-Infinity` reached KK. `to_cardinal` strips the
    /// sign textually then does `int("Infinity")` → `ValueError`; `to_ordinal`
    /// (`to_cardinal(...) + "-інші"`) and `to_year` (`to_cardinal`) raise the
    /// same `ValueError` before their suffix/wrap. `to_ordinal_num` is a purely
    /// textual `str(number) + "."`, so it echoes the token (sign preserved).
    fn inf_result(&self, negative: bool, to: &str) -> Result<String> {
        match to {
            "ordinal_num" => {
                let token = if negative { "-Infinity" } else { "Infinity" };
                Ok(format!("{}.", token))
            }
            // cardinal/ordinal/year: int() sees the sign-stripped token.
            _ => Err(int_value_error("Infinity")),
        }
    }

    /// `Decimal('NaN')` reached KK. `int("NaN")` → `ValueError` on the
    /// cardinal/ordinal/year paths; `to_ordinal_num` echoes "NaN.".
    fn nan_result(&self, to: &str) -> Result<String> {
        match to {
            "ordinal_num" => Ok("NaN.".to_string()),
            _ => Err(int_value_error("NaN")),
        }
    }

    // ---- currency ------------------------------------------------------
    //
    // `Num2Word_KK` overrides `to_currency` outright and inherits `to_cheque`
    // from `Num2Word_Base`. Those two entry points reach the class's state by
    // completely separate routes, which is why only `currency_forms` and
    // `lang_name` are overridden alongside `to_currency`:
    //
    // * `to_currency` never raises — it *falls back* to the first
    //   `CURRENCY_FORMS` entry for an unknown code (bug 5).
    // * `to_cheque` does `self.CURRENCY_FORMS[currency]` and turns the
    //   `KeyError` into `NotImplementedError`.
    //
    // So the fallback must live in `to_currency` and must NOT leak into
    // `currency_forms`, or `cheque:GBP` would return "... ТЕҢГЕ" instead of
    // raising. The corpus pins both halves:
    //   currency:GBP 12.34 -> "он екі теңге отыз төрт тиын"  (fallback)
    //   cheque:GBP  1234.56 -> NotImplementedError            (no fallback)
    //
    // Not overridden, because `Num2Word_KK` does not override them either:
    //
    // * `currency_precision` — `Num2Word_KK` defines no `CURRENCY_PRECISION`
    //   and inherits `Num2Word_Base`'s empty `{}`, so `.get(code, 100)` is 100
    //   for every code. The trait default is already 100. KK inherits from
    //   `Num2Word_Base`, not from `Num2Word_EN`, so it never sees EN's
    //   KWD/BHD-style overrides: `cheque:KWD` would be /100, not /1000 — and
    //   in fact never gets that far, since KWD is absent from the table and
    //   raises first. Confirmed live: `CONVERTER_CLASSES["kk"].
    //   CURRENCY_PRECISION == {}`.
    // * `currency_adjective` — `CURRENCY_ADJECTIVES` is `{}` (inherited,
    //   empty), and `to_currency` ignores `adjective` anyway (bug 8).
    // * `pluralize` — abstract in `Num2Word_Base` and left abstract by
    //   `Num2Word_KK`. Unreachable: `to_currency` selects the plural inline
    //   with `left != 1`, and `to_cheque` takes `cr1[-1]` unconditionally. The
    //   trait default (raise NotImplemented) is the faithful mirror.
    // * `money_verbose` / `cents_verbose` / `cents_terse` — `Num2Word_Base`'s
    //   `_money_verbose` is `return self.to_cardinal(number)`, which is the
    //   trait default. `to_cheque` calls it; the other two are unreachable
    //   because KK's `to_currency` never delegates to the base.
    // * `cardinal_from_decimal` — the fractional-cents branch lives in
    //   `Num2Word_Base.to_currency`, which KK never enters. Left at its
    //   default.

    /// `self.__class__.__name__`, read by `Num2Word_Base.to_cheque`'s
    /// `NotImplementedError` message.
    fn lang_name(&self) -> &str {
        LANG_NAME
    }

    /// `self.CURRENCY_FORMS[code]` — a *strict* lookup, as `to_cheque` does it.
    ///
    /// Returns `None` for an unknown code so the inherited `to_cheque` raises
    /// `NotImplementedError`. `to_currency`'s forgiving
    /// `.get(code, <first entry>)` is a different lookup and is spelled out
    /// there; the two must not be merged.
    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.currency_forms.get(code)
    }

    /// Port of `Num2Word_KK.to_currency`.
    ///
    /// ```python
    /// def to_currency(
    ///     self, val, currency="KZT", cents=True, separator=" ", adjective=False
    /// ):
    ///     """Convert to currency in Kazakh."""
    ///     is_negative = False
    ///     if val < 0:
    ///         is_negative = True
    ///         val = abs(val)
    ///
    ///     parts = str(val).split(".")
    ///     left = int(parts[0]) if parts[0] else 0
    ///     right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0
    ///
    ///     cr1, cr2 = self.CURRENCY_FORMS.get(
    ///         currency, list(self.CURRENCY_FORMS.values())[0]
    ///     )
    ///
    ///     left_str = self._int_to_word(left)
    ///     result = left_str + " " + (cr1[1] if left != 1 else cr1[0])
    ///
    ///     if cents and right:
    ///         cents_str = self._int_to_word(right)
    ///         result += separator + cents_str + " " + (cr2[1] if right != 1 else cr2[0])
    ///
    ///     if is_negative:
    ///         result = self.negword + result
    ///
    ///     return result.strip()
    /// ```
    ///
    /// A complete override: `Num2Word_Base.to_currency` is never called, so
    /// none of `parse_currency_parts`, `pluralize`, `_cents_verbose`,
    /// `_cents_terse`, `CURRENCY_PRECISION` or `CURRENCY_ADJECTIVES` is
    /// reachable from here. Infallible — there is no `NotImplementedError`
    /// path (bug 5) and no table index that can escape its range.
    ///
    /// # Faithfully reproduced Python bugs (currency)
    ///
    /// 5. **An unknown currency code silently becomes KZT.** Python's
    ///    `.get(currency, list(self.CURRENCY_FORMS.values())[0])` falls back to
    ///    the first-inserted entry instead of raising, so `currency:GBP`,
    ///    `:JPY`, `:KWD`, `:BHD`, `:INR`, `:CNY` and `:CHF` all quietly render
    ///    in теңге/тиын. All 84 such rows are in the corpus. The amounts are
    ///    *not* converted — 12.34 GBP prints as 12 теңге 34 тиын.
    /// 6. **Cents are always /100, whatever the currency.** `parts[1][:2]`
    ///    hard-codes two fractional digits, so a 3-decimal currency would lose
    ///    its third digit and a 0-decimal one would gain a subunit. Moot in
    ///    practice given bug 5 — JPY and KWD never reach their own forms.
    /// 7. **`int` and `float` are indistinguishable.** `Num2Word_Base`
    ///    branches on `isinstance(val, int)` to skip cents; KK instead tests
    ///    `if cents and right:`, a truthiness test on the *cent count*. So
    ///    `1.0` and `1` both give "бір euro" — the float does not render a
    ///    zero-cents segment the way the base class would. The corpus pins
    ///    `1.0` -> "бір euro".
    /// 8. **`adjective` is accepted and never read.** The parameter is in the
    ///    signature and appears nowhere in the body, so `adjective=True` is a
    ///    no-op. (`CURRENCY_ADJECTIVES` is empty anyway, so even the base class
    ///    would have been a no-op here.)
    /// 9. **The English "zero" leaks into every currency string.** `left == 0`
    ///    routes through `_int_to_word`'s module bug 1, hence
    ///    "zero euros бір cent" for 0.01.
    fn to_currency(
        &self,
        val: &CurrencyValue,
        currency: &str,
        cents: bool,
        separator: Option<&str>,
        _adjective: bool, // declared by Python, never read — bug 8.
    ) -> Result<String> {
        // Trait now hands us None when the caller omitted separator=;
        // resolve it to this language's own default before the ported body.
        let separator = separator.unwrap_or(self.default_separator());
        let separator = if separator == SEPARATOR_UNSET {
            SEPARATOR_DEFAULT
        } else {
            separator
        };

        // Python: `if val < 0: is_negative = True; val = abs(val)`. The abs is
        // folded into split_currency, which every later step reads through.
        let is_negative = val.is_negative();
        let (left, right) = Self::split_currency(val);

        // `.get(currency, list(CURRENCY_FORMS.values())[0])` — bug 5. Python
        // evaluates the default eagerly on every call, but it cannot fail:
        // KZT is always present.
        let forms = match self.currency_forms.get(currency) {
            Some(f) => f,
            None => &self.currency_forms[FALLBACK_CURRENCY],
        };

        let one = BigInt::one();
        let left_str = self.int_to_word(&left);
        let mut result = format!(
            "{} {}",
            left_str,
            if left != one { &forms.unit[1] } else { &forms.unit[0] }
        );

        // `if cents and right:` — a truthiness test on the cent count, not on
        // the type of `val`. See bug 7.
        if cents && !right.is_zero() {
            let cents_str = self.int_to_word(&right);
            result.push_str(separator);
            result.push_str(&cents_str);
            result.push(' ');
            result.push_str(if right != one {
                &forms.subunit[1]
            } else {
                &forms.subunit[0]
            });
        }

        if is_negative {
            // negword carries a trailing space ("minus "), so this is the seam
            // the final strip() does *not* touch.
            result = format!("{}{}", NEGWORD, result);
        }

        Ok(result.trim().to_string())
    }
}
