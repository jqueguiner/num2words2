//! Port of `lang_KY.py` (Kyrgyz).
//!
//! Shape: **self-contained**. `Num2Word_KY` subclasses `Num2Word_Base` but
//! defines no `high_numwords`/`mid_numwords`/`low_numwords`, so the guard in
//! `Num2Word_Base.__init__`
//!
//! ```text
//! if any(hasattr(self, field) for field in
//!        ["high_numwords", "mid_numwords", "low_numwords"]):
//! ```
//!
//! is never taken: Python never builds `self.cards` and never sets `MAXVAL`.
//! `cards`/`maxval`/`merge` therefore stay at their trait defaults here, and
//! **there is no overflow check at all** — see the `str(number)` fallback
//! below for what happens past the table's ceiling.
//!
//! All four in-scope methods are overridden by `Num2Word_KY`, so nothing from
//! `Num2Word_Base` reaches the output path:
//!   * `to_cardinal`    — own algorithm over `_int_to_word`.
//!   * `to_ordinal`     — `to_cardinal(n) + "-inchi"`.
//!   * `to_ordinal_num` — `str(n) + "-inchi"`.
//!   * `to_year`        — `to_cardinal(val)`, ignoring its own `longval` arg.
//!
//! Two consequences of those overrides are load-bearing:
//!
//! 1. `Num2Word_Base.to_cardinal` pipes its result through `self.title()`;
//!    KY's override does not, so titling never applies. (`is_title` is also
//!    left `False` by `setup`, so it would be a no-op regardless.)
//! 2. `Num2Word_Base.to_ordinal` calls `verify_ordinal`, which raises
//!    `TypeError` for negative input. KY's override skips it, so
//!    `to_ordinal(-1)` == "minus bir-inchi" rather than raising. Likewise
//!    `to_ordinal(0)` == "nöl-inchi" — no crash.
//!
//! # Faithfully reproduced Python quirks
//!
//! This is a port, not a rewrite. All of the following are what Python emits
//! and are verified against the frozen corpus:
//!
//! 1. **Numbers >= 10^9 are not spelled at all.** `_int_to_word` handles
//!    units/tens/hundreds/thousands/millions and then falls off the end with
//!    a bare `return str(number)`. There is no milliard/billion entry, and no
//!    `OverflowError` — `to_cardinal(10**9)` == "1000000000" (the digits),
//!    and `to_ordinal(10**9)` == "1000000000-inchi". This holds for arbitrary
//!    magnitudes, hence [`LangKy::int_to_word`] takes `&BigInt` and only
//!    narrows to `u64` *after* proving `number < 10^9`.
//! 2. **"bir million" but plain "min"/"jüz".** The thousands and hundreds
//!    branches suppress the leading "bir" via `if h > 1` / `if t > 1`, so
//!    100 == "jüz" and 1000 == "min". The millions branch has no such guard,
//!    so 10^6 == "bir million", not "million".
//! 3. **`thousand` is spelled "min"** (not "miŋ"/"mıŋ"), and the tens table
//!    mixes transliteration styles ("jıyırma", "elüü", "altymysh"). Kept
//!    verbatim.
//! 4. **`pointword` is "üтүр" — a mixed-script string.** The leading "ü" is
//!    Latin U+00FC while "тү р" is Cyrillic (U+0442 U+04AF U+0440). It is
//!    almost certainly meant to be all-Cyrillic "үтүр", but the corpus
//!    confirms the mixed form byte for byte. The float grammar consumes it;
//!    it also appears in `exclude_title`.
//!
//! # Float/Decimal entry routing (the `"." in str(number)` rule)
//!
//! `to_cardinal` never asks whether the value is *whole* — it asks whether the
//! *string* shows a point. That routing is reproduced by
//! [`Lang::cardinal_float_entry`] here (and, through it, the ordinal/year
//! entries), with these pinned consequences:
//!
//! * **Whole floats keep their ".0" tail.** `str(5.0)` == "5.0" has a point,
//!   so `to_cardinal(5.0)` == "besh üтүр nöl", *not* "besh". Likewise
//!   `Decimal("5.00")` == "besh üтүр nöl nöl" — every fractional character is
//!   spelled, trailing zeros included.
//! * **`-0.0` renders the negword.** The sign is read off the string
//!   (`str(-0.0)` == "-0.0" starts with "-"), so `to_cardinal(-0.0)` ==
//!   "minus nöl üтүр nöl". A `< 0` test would miss it.
//! * **Scientific notation is a `ValueError`.** `str(1e16)` == "1e+16" has no
//!   point, so Python runs `int("1e+16")` and dies: `invalid literal for
//!   int() with base 10: '1e+16'`. Same for `1e+20`, for tiny floats
//!   (`str(1e-05)` == "1e-05"), and for non-canonical Decimals
//!   (`str(Decimal("1E+2"))` == "1E+2"). The sign is stripped *before* the
//!   `int()` (Python recurses on `n[1:]`), so the message never shows a minus.
//! * **Point-less integral Decimals take the integer grammar.**
//!   `Decimal("100")` stringifies as "100" — no point — and `int("100")`
//!   succeeds, so it renders "jüz" like the int would.
//! * `to_ordinal(float)` is `to_cardinal(float) + "-inchi"` ("besh üтүр
//!   nöl-inchi"); `to_ordinal_num(float)` is `str(number) + "-inchi"`
//!   ("5.0-inchi", "1e+16-inchi" — no ValueError here, nothing is parsed);
//!   `to_year(float)` is `to_cardinal(float)` (the trait default already
//!   routes through the override above).
//! * **`"Infinity"`/`"NaN"` strings fall back to Python.** `Decimal("Infinity")`
//!   parses fine and dies later in `int("Infinity")` (ValueError) — but only
//!   on the modes that parse; `to_ordinal_num("Infinity")` happily returns
//!   "Infinity-inchi". `ParsedNumber` cannot carry Inf/NaN into that split, so
//!   `str_to_number` returns NotImplemented and the shim reruns the original
//!   pure-Python path, reproducing every mode exactly.
//!
//! # Sign handling
//!
//! Python's `to_cardinal` works on the *string* form: `n = str(number).strip()`,
//! then `if n.startswith("-"): return (self.negword + self.to_cardinal(n[1:])).strip()`.
//! For integral input `str(BigInt)` never contains ".", so this reduces to
//! "recurse on the absolute value and prefix `negword`" — reproduced directly
//! on `BigInt` here. The trailing `.strip()` is a no-op in practice (`negword`
//! is "minus " and `_int_to_word` never returns a blank for a non-negative
//! input) but is kept for fidelity.

use crate::base::{Lang, N2WError, Result};
use crate::currency::{CurrencyForms, CurrencyValue};
use crate::floatpath::FloatValue;
use crate::strnum::{python_decimal_parse, python_decimal_str, ParsedNumber};
use bigdecimal::BigDecimal;
use num_bigint::BigInt;
use num_traits::{One, Signed, ToPrimitive, Zero};
use std::collections::HashMap;

/// `setup`: `self.negword`. Note the trailing space — it is the word/number
/// separator, and the concatenation is `.strip()`ed afterwards.
const NEGWORD: &str = "minus ";

/// `setup`: `self.pointword`. Mixed Latin/Cyrillic in the original; see the
/// module docs. Unused by the four in-scope modes.
const POINTWORD: &str = "üтүр";

/// The literal `"nöl"` that `_int_to_word` returns for 0. Python has no
/// `self.ones[0]` entry for it — index 0 of `ones` is the empty string, and
/// zero is special-cased ahead of the table lookup.
const ZERO_WORD: &str = "nöl";

/// The suffix `to_ordinal`/`to_ordinal_num` append. Glued on with no
/// separator, so it lands directly against the final word: "min-inchi".
const ORDINAL_SUFFIX: &str = "-inchi";

/// `setup`: `self.ones`. Index 0 is the empty string (Python relies on this
/// only via the float path's `self.ones[int(digit)] or "nöl"` fallback).
const ONES: [&str; 10] = [
    "", "bir", "eki", "üch", "tört", "besh", "alty", "jeti", "segiz", "toguz",
];

/// `setup`: `self.tens`. Index 0 is the empty string and is unreachable —
/// the `number < 100` branch only runs for `number >= 10`, so `t >= 1`.
const TENS: [&str; 10] = [
    "", "on", "jıyırma", "otuz", "kırk", "elüü", "altymysh", "jetimish", "seksen", "tokson",
];

/// `setup`: `self.hundred`.
const HUNDRED: &str = "jüz";

/// `setup`: `self.thousand`. Spelled "min" in the source — see module docs.
const THOUSAND: &str = "min";

/// `setup`: `self.million`.
const MILLION: &str = "million";

/// 10^9 — the ceiling past which `_int_to_word` gives up and returns digits.
fn one_e9() -> BigInt {
    BigInt::from(1_000_000_000u64)
}

/// The key `to_currency` falls back to for an unknown currency code.
///
/// Python writes `self.CURRENCY_FORMS.get(currency, list(self.CURRENCY_FORMS.values())[0])`
/// — the *first* entry in the class dict, which since Python 3.7 means the
/// first one in the literal. That is "KGS". A `HashMap` has no insertion
/// order, so the identity of that first entry is pinned here rather than
/// recovered from iteration. Verified live:
/// `list(Num2Word_KY.CURRENCY_FORMS.values())[0] == (("som","som"),("tıyın","tıyın"))`.
const FALLBACK_CURRENCY: &str = "KGS";

/// `Num2Word_KY.CURRENCY_FORMS`, verbatim.
///
/// KY declares its **own** class-level dict, so — unlike the 16 classes that
/// read `Num2Word_EUR`'s dict after `Num2Word_EN.__init__` has mutated it —
/// none of EN's ~24 extra ISO codes (GBP, JPY, KWD, BHD, INR, CNY, CHF, ...)
/// exist here. The corpus proves the isolation: `to_cheque(1234.56, "GBP")`
/// raises NotImplementedError rather than rendering pounds.
///
/// Every entry carries exactly two forms, and both are identical — Kyrgyz does
/// not inflect the counted noun. `to_currency` still indexes `[0]`/`[1]`
/// literally, so the arity is kept even though the two are indistinguishable.
fn build_currency_forms() -> HashMap<&'static str, CurrencyForms> {
    let mut m: HashMap<&'static str, CurrencyForms> = HashMap::new();
    // Listed in the order of the Python dict literal. Only the first entry's
    // identity matters (see FALLBACK_CURRENCY); the rest is a plain lookup.
    m.insert("KGS", CurrencyForms::new(&["som", "som"], &["tıyın", "tıyın"]));
    m.insert("USD", CurrencyForms::new(&["dollar", "dollar"], &["sent", "sent"]));
    m.insert("EUR", CurrencyForms::new(&["evro", "evro"], &["sent", "sent"]));
    m.insert("RUB", CurrencyForms::new(&["rubl", "rubl"], &["kopek", "kopek"]));
    m
}

/// `parts = str(abs(val)).split(".")` → `(left, right)`, for the float/Decimal
/// arm of `to_currency`.
///
/// Python reads the *decimal string*, not the number:
///
/// ```text
/// parts = str(val).split(".")
/// left  = int(parts[0]) if parts[0] else 0
/// right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0
/// ```
///
/// `BigDecimal`'s `(int_val, scale)` pair *is* that string's structure —
/// "12.34" parses to `(1234, 2)`, "0.5" to `(5, 1)`, "1.0" to `(10, 1)` — so
/// the split is done on the digits rather than by re-formatting, which would
/// depend on `Display` agreeing with Python's `str()`.
///
/// Two behaviours here are Python's, not conveniences:
///
/// * **`[:2]` truncates, never rounds.** `12.345` → 34 cents, not 35.
/// * **`.ljust(2, "0")` pads on the *right*.** `0.5` → parts[1] == "5" → "50"
///   → **50** cents, not 5. Dropping the pad turns "nöl evro elüü sent" into
///   "nöl evro besh sent".
///
/// `abs()` runs before `str()` in Python, and negating changes no digit and no
/// scale, so taking `abs` of `int_val` here is equivalent.
fn split_currency_parts(value: &BigDecimal) -> Result<(BigInt, BigInt)> {
    let (int_val, scale) = value.as_bigint_and_exponent();
    let int_val = int_val.abs();

    // scale < 0 means the literal carried a positive exponent, which is the
    // only way `BigDecimal::from_str` produces one. Python's `str()` keeps
    // that form for floats (`str(1e21) == "1e+21"`) and for Decimals
    // (`str(Decimal("1E+2")) == "1E+2"`) alike, so `.split(".")` yields a
    // one-element list and `int("1e+21")` raises ValueError. Confirmed live:
    //   >>> Num2Word_KY().to_currency(1e21, "EUR")
    //   ValueError: invalid literal for int() with base 10: '1e+21'
    // Both possible source types agree, so this branch is unambiguous.
    if scale < 0 {
        return Err(N2WError::Value(format!(
            "invalid literal for int() with base 10: '{}'",
            value
        )));
    }

    // No ".": `len(parts) > 1` is false, so `right` stays 0.
    if scale == 0 {
        return Ok((int_val, BigInt::zero()));
    }

    // The last `scale` digits are what `str()` prints after the "."; pad on
    // the left so there is always at least one integer digit ("0.01" → "001",
    // giving parts[0] == "0" and parts[1] == "01").
    let digits = int_val.to_string();
    let s = scale as usize;
    let padded = if digits.len() <= s {
        format!("{}{}", "0".repeat(s - digits.len() + 1), digits)
    } else {
        digits
    };
    let split = padded.len() - s;
    let left: BigInt = padded[..split].parse().expect("digits only");

    // parts[1][:2].ljust(2, "0")
    let mut two: String = padded[split..].chars().take(2).collect();
    while two.len() < 2 {
        two.push('0');
    }
    let right: BigInt = two.parse().expect("digits only");
    Ok((left, right))
}

/// Reconstruct Python's `str(number).split(".")` for the float/Decimal cardinal
/// path, returning `(abs_left, right_digits, has_dot)`.
///
/// KY's `to_cardinal` reads the *decimal string*, not a rounded `(pre, post)`
/// tuple: every character after the "." is spelled as its own digit, with no
/// rounding, truncation, `< 0.01` heuristic, or `precision` consultation. So
/// this reproduces that string rather than routing through
/// `Num2Word_Base.float2tuple` (which KY's override never reaches).
///
/// * **Decimal** — the `(int_val, scale)` pair *is* the string's structure, so
///   the split is exact: "1.10" → left 1, right "10" (the trailing zero
///   survives because `BigDecimal` keeps the scale); "0.001" → left 0, right
///   "001"; "98746251323029.99" → left 98746251323029, right "99".
/// * **Float** — formatted to exactly `precision` fractional places. `precision`
///   is Python's shortest-round-trip digit count (`abs(Decimal(str(value))
///   .as_tuple().exponent)`, computed on the Python side), so `{:.precision}`
///   reproduces `str(float)` across the whole reachable range. The f64 artefacts
///   that force `base.float2tuple`'s heuristic never surface here: `2.675`
///   formats straight to "2.675" and `1.005` to "1.005", because `str()`
///   already collapses the binary noise to the clean shortest form.
///
/// `abs()` is taken first (on the f64, or on `int_val`), mirroring Python
/// stripping the leading "-" off the string before re-parsing; negating changes
/// no digit and no scale, so the absolute reconstruction is identical.
fn decompose_float(v: &FloatValue) -> (BigInt, String, bool) {
    match v {
        FloatValue::Decimal { value, .. } => {
            // Use the parsed scale, not the passed `precision`: they agree for
            // every reachable Decimal (both are `abs(exponent)`), and the scale
            // is what actually carries the digit count of `str()`.
            let (int_val, scale) = value.as_bigint_and_exponent();
            let abs = int_val.abs();
            if scale <= 0 {
                // Integral Decimal: `str()` has no ".", so Python's integer
                // branch runs. Unreachable from the dispatcher (integral values
                // take the int path), handled defensively as the integer form.
                return (abs, String::new(), false);
            }
            let digits = abs.to_string();
            let s = scale as usize;
            // Pad on the left so there is always at least one integer digit
            // ("0.01" → "001" → left "0", right "01").
            let padded = if digits.len() <= s {
                format!("{}{}", "0".repeat(s - digits.len() + 1), digits)
            } else {
                digits
            };
            let split = padded.len() - s;
            let left: BigInt = padded[..split].parse().expect("digits only");
            // Exactly `scale` characters — the full fractional part, no `[:2]`
            // truncation (that is the currency path's quirk, not this one).
            let right = padded[split..].to_string();
            (left, right, true)
        }
        FloatValue::Float { value, precision } => {
            // Fixed-notation, so large magnitudes never flip to Rust's `1e21`
            // Display form; `precision` fractional places reproduce `str()`.
            let s = format!("{:.*}", *precision as usize, value.abs());
            match s.split_once('.') {
                Some((l, r)) => (l.parse().expect("digits only"), r.to_string(), true),
                None => (s.parse().expect("digits only"), String::new(), false),
            }
        }
    }
}

/// Python's `int(s)` failure, message verbatim from CPython. The `s` is the
/// point-less `str(number)` slice KY feeds it — sign already stripped, because
/// `to_cardinal` peels the "-" off the string and recurses *before* `int()`.
fn int_value_error(s: &str) -> N2WError {
    N2WError::Value(format!("invalid literal for int() with base 10: '{}'", s))
}

/// Python `repr(float)` for the scientific range, on an already-`abs()`ed
/// finite f64 (`a >= 1e16`, or `0 < a < 1e-4`).
///
/// Rust's `{:e}` yields the shortest round-trip mantissa — the same digits
/// CPython's repr picks — but lays the exponent out as `1e16` / `1e-5` where
/// Python writes `1e+16` / `1e-05`: always a sign, zero-padded to two digits.
/// Only the exponent dressing needs fixing up.
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
                // the string-sign recursion before int() ever sees it.
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

pub struct LangKy {
    exclude_title: Vec<String>,
    forms: HashMap<&'static str, CurrencyForms>,
}

impl Default for LangKy {
    fn default() -> Self {
        Self::new()
    }
}

impl LangKy {
    pub fn new() -> Self {
        LangKy {
            // `setup`: self.exclude_title = ["minus", "üтүр"] — note "minus"
            // here has no trailing space, unlike `negword`.
            exclude_title: vec![NEGWORD.trim().to_string(), POINTWORD.to_string()],
            // Built once here, never per call. `to_currency` only ever reads
            // this table, and rebuilding it per call is what made an earlier
            // revision of this port slower than the Python it replaces.
            forms: build_currency_forms(),
        }
    }

    /// Port of `_int_to_word`, entry point on `BigInt`.
    ///
    /// Splits into the arbitrary-precision concerns (zero, the >= 10^9 digit
    /// fallback, and the unreachable negative-index quirk) and then hands the
    /// proven-bounded remainder to [`LangKy::int_to_word_small`].
    fn int_to_word(&self, number: &BigInt) -> Result<String> {
        // `if number == 0: return "nöl"`
        if number.is_zero() {
            return Ok(ZERO_WORD.to_string());
        }

        if number.is_negative() {
            // Unreachable from the four in-scope modes: `to_cardinal` strips
            // the "-" off the *string* before it ever calls `_int_to_word`.
            // Modelled anyway so this cannot panic, and because Python's
            // behaviour here is a genuine quirk rather than an error: a
            // negative `number` satisfies `number < 10`, so Python evaluates
            // `self.ones[number]` — a *negative list index*. For -10..=-1 that
            // silently wraps to `ONES[number + 10]` (so `_int_to_word(-5)`
            // == "besh"); anything <= -11 is out of range and raises
            // IndexError.
            let wrapped = number + BigInt::from(10);
            return match wrapped.to_usize() {
                Some(i) if i < ONES.len() => Ok(ONES[i].to_string()),
                _ => Err(N2WError::Index("list index out of range".to_string())),
            };
        }

        // Quirk 1: the final `return str(number)`. No OverflowError, no
        // milliard word — just the decimal digits. Must be checked on the
        // BigInt, since `number` is unbounded above.
        if number >= &one_e9() {
            return Ok(number.to_string());
        }

        // Proven: 0 < number < 10^9, so a u64 is lossless from here down.
        let n = number
            .to_u64()
            .expect("0 < number < 10^9 was just proven, so u64 conversion cannot fail");
        Ok(self.int_to_word_small(n))
    }

    /// Port of `_int_to_word`'s spelled-out branches, for `0 <= n < 10^9`.
    ///
    /// Each `+ (" " + ... if x else "")` in Python is a conditional suffix,
    /// *not* an unconditional join — hence the explicit `!= 0` guards, which
    /// are what keep 100 at "jüz" rather than "jüz nöl".
    fn int_to_word_small(&self, n: u64) -> String {
        // Mirrors Python's first line. Every call site below guards `r != 0`,
        // so this is defensive rather than reachable.
        if n == 0 {
            return ZERO_WORD.to_string();
        }

        // `if number < 10: return self.ones[number]`
        if n < 10 {
            return ONES[n as usize].to_string();
        }

        // `if number < 100:`
        //     `t, o = divmod(number, 10)`
        //     `return self.tens[t] + (" " + self.ones[o] if o else "")`
        if n < 100 {
            let (t, o) = (n / 10, n % 10);
            let mut s = TENS[t as usize].to_string();
            if o != 0 {
                s.push(' ');
                s.push_str(ONES[o as usize]);
            }
            return s;
        }

        // `if number < 1000:`
        //     `h, r = divmod(number, 100)`
        //     `base = (self.ones[h] + " " if h > 1 else "") + self.hundred`
        //     `return base + (" " + self._int_to_word(r) if r else "")`
        // Quirk 2: `h > 1` suppresses "bir", so 100 == "jüz".
        if n < 1_000 {
            let (h, r) = (n / 100, n % 100);
            let mut s = String::new();
            if h > 1 {
                s.push_str(ONES[h as usize]);
                s.push(' ');
            }
            s.push_str(HUNDRED);
            if r != 0 {
                s.push(' ');
                s.push_str(&self.int_to_word_small(r));
            }
            return s;
        }

        // `if number < 1000000:`
        //     `t, r = divmod(number, 1000)`
        //     `base = (self._int_to_word(t) + " " if t > 1 else "") + self.thousand`
        //     `return base + (" " + self._int_to_word(r) if r else "")`
        // Quirk 2 again: `t > 1` suppresses "bir", so 1000 == "min".
        if n < 1_000_000 {
            let (t, r) = (n / 1_000, n % 1_000);
            let mut s = String::new();
            if t > 1 {
                s.push_str(&self.int_to_word_small(t));
                s.push(' ');
            }
            s.push_str(THOUSAND);
            if r != 0 {
                s.push(' ');
                s.push_str(&self.int_to_word_small(r));
            }
            return s;
        }

        // `if number < 1000000000:`
        //     `m, r = divmod(number, 1000000)`
        //     `base = self._int_to_word(m) + " " + self.million`
        //     `return base + (" " + self._int_to_word(r) if r else "")`
        // Quirk 2, inverted: no `m > 1` guard here, so 10^6 == "bir million".
        let (m, r) = (n / 1_000_000, n % 1_000_000);
        let mut s = self.int_to_word_small(m);
        s.push(' ');
        s.push_str(MILLION);
        if r != 0 {
            s.push(' ');
            s.push_str(&self.int_to_word_small(r));
        }
        s
    }
}

impl Lang for LangKy {
    /// This language's own `to_currency(currency=...)` default,
    /// read from the live Python signature. Only 44 of 156 use EUR.
    fn default_currency(&self) -> &str {
        "KGS"
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
        "üтүр"
    }

    // `is_title` is left at Num2Word_Base's `False`; `setup` never touches it.
    // KY's `to_cardinal` override never calls `title()` anyway.

    fn exclude_title(&self) -> &[String] {
        &self.exclude_title
    }

    /// Port of `to_cardinal`.
    ///
    /// The Python operates on `str(number)`; for integral input the "." branch
    /// is dead and the "-" branch reduces to a recursion on the absolute
    /// value. See the module docs.
    fn to_cardinal(&self, value: &BigInt) -> Result<String> {
        // `if n.startswith("-"):`
        //     `return (self.negword + self.to_cardinal(n[1:])).strip()`
        if value.is_negative() {
            let inner = self.to_cardinal(&-value)?;
            return Ok(format!("{}{}", NEGWORD, inner).trim().to_string());
        }
        // `return self._int_to_word(int(n))`
        self.int_to_word(value)
    }

    /// Port of `to_ordinal`: `self.to_cardinal(number) + "-inchi"`.
    ///
    /// No `verify_ordinal`, so negatives and zero pass straight through:
    /// `to_ordinal(-1)` == "minus bir-inchi", `to_ordinal(0)` == "nöl-inchi".
    /// Past 10^9 it inherits the digit fallback: `to_ordinal(10**9)` ==
    /// "1000000000-inchi".
    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        Ok(format!("{}{}", self.to_cardinal(value)?, ORDINAL_SUFFIX))
    }

    /// Port of `to_ordinal_num`: `str(number) + "-inchi"`.
    ///
    /// Purely textual — the minus sign survives, so `to_ordinal_num(-1)` ==
    /// "-1-inchi".
    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        Ok(format!("{}{}", value, ORDINAL_SUFFIX))
    }

    /// Port of `to_year`: `return self.to_cardinal(val)`.
    ///
    /// KY declares `longval=True` but ignores it, and does no century
    /// pairing or BC/AD handling — years are plain cardinals, so
    /// `to_year(1984)` == "min toguz jüz seksen tört" and `to_year(-44)` ==
    /// "minus kırk tört".
    fn to_year(&self, value: &BigInt) -> Result<String> {
        self.to_cardinal(value)
    }

    /// Port of `to_cardinal`'s float/Decimal branch.
    ///
    /// `Num2Word_KY` overrides `to_cardinal` and handles non-integers *inline*
    /// off `str(number)`; it never reaches `Num2Word_Base.to_cardinal_float`
    /// / `float2tuple`. So this reproduces that string-based branch directly:
    ///
    /// ```text
    /// n = str(number).strip()
    /// if n.startswith("-"):
    ///     return (self.negword + self.to_cardinal(n[1:])).strip()
    /// if "." in n:
    ///     left, right = n.split(".", 1)
    ///     ret = self._int_to_word(int(left)) + " " + self.pointword
    ///     for digit in right:
    ///         ret += " " + (self.ones[int(digit)] or "nöl")
    ///     return ret.strip()
    /// ```
    ///
    /// Notes on fidelity:
    ///
    /// * **No rounding, truncation, or precision.** Each fractional character is
    ///   spelled as its own digit; `2.675` → "eki üтүр alty jeti besh" and
    ///   `Decimal("1.10")` → "bir üтүр bir nöl" (the trailing zero is kept).
    /// * **`precision_override` is ignored.** KY's `to_cardinal` never reads
    ///   `self.precision`, so the `precision=` kwarg has no effect on the
    ///   output — verified live: `num2words(2.675, lang="ky", precision=1)`
    ///   still yields all three fractional digits.
    /// * **The `>= 10^9` digit fallback reaches the integer part.** The `left`
    ///   of `98746251323029.99` renders as its bare digits, since `_int_to_word`
    ///   gives up past a billion.
    /// * **The fractional digit uses `self.ones[d]`, not `_int_to_word`.**
    ///   `ones[0]` is `""` (falsy) → "nöl"; every other index is its own word.
    fn to_cardinal_float(
        &self,
        value: &FloatValue,
        _precision_override: Option<u32>,
    ) -> Result<String> {
        // `if n.startswith("-"):` — the sign is read off the string, then the
        // absolute value is rendered and prefixed with negword.
        let is_negative = value.is_negative();
        let (left, right, has_dot) = decompose_float(value);

        let mut body = if has_dot {
            // `ret = self._int_to_word(int(left)) + " " + self.pointword`
            let mut s = format!("{} {}", self.int_to_word(&left)?, POINTWORD);
            // `for digit in right: ret += " " + (self.ones[int(digit)] or "nöl")`
            for ch in right.chars() {
                let d = ch.to_digit(10).expect("fractional part is digits only") as usize;
                s.push(' ');
                // `self.ones[d] or "nöl"` — ONES[0] == "" is falsy → "nöl".
                s.push_str(if ONES[d].is_empty() { ZERO_WORD } else { ONES[d] });
            }
            s
        } else {
            // No ".": Python falls through to `_int_to_word(int(n))`. Only
            // reachable for the defensive integral-Decimal case above.
            self.int_to_word(&left)?
        };

        // `(self.negword + ...).strip()` — negword ("minus ") carries its own
        // trailing space, which becomes the separator.
        if is_negative {
            body = format!("{}{}", NEGWORD, body);
        }
        Ok(body.trim().to_string())
    }

    /// `to_cardinal(float/Decimal)` — the full entry, routing on
    /// `"." in str(number)` rather than on whole-ness (see the module docs).
    ///
    /// A whole float therefore keeps its ".0" tail (`5.0` -> "besh üтүр nöl",
    /// `-0.0` -> "minus nöl üтүр nöl"), a point-less integral Decimal takes
    /// the integer grammar (`Decimal("100")` -> "jüz"), and a point-less
    /// non-integer form is Python's `int()` ValueError (`1e+16`,
    /// `Decimal("1E+2")`).
    ///
    /// `precision_override` is threaded through untouched; KY's grammar never
    /// reads a precision, so it is inert either way (see `to_cardinal_float`).
    fn cardinal_float_entry(
        &self,
        value: &FloatValue,
        precision_override: Option<u32>,
    ) -> Result<String> {
        match route_by_str(value)? {
            StrRoute::Point => self.to_cardinal_float(value, precision_override),
            StrRoute::WholeDigits(abs_int) => {
                // `return self._int_to_word(int(n))`, with the string sign
                // already peeled and re-attached as negword by the recursion:
                // `(self.negword + self.to_cardinal(n[1:])).strip()`.
                let body = self.int_to_word(&abs_int)?;
                if value.is_negative() {
                    Ok(format!("{}{}", NEGWORD, body).trim().to_string())
                } else {
                    Ok(body)
                }
            }
        }
    }

    /// `to_ordinal(float/Decimal)`: `self.to_cardinal(number) + "-inchi"` —
    /// same blind suffix as the integer path, so `5.0` == "besh üтүр
    /// nöl-inchi" and the ValueError of `1e+16` propagates unchanged.
    fn ordinal_float_entry(&self, value: &FloatValue) -> Result<String> {
        Ok(format!(
            "{}{}",
            self.cardinal_float_entry(value, None)?,
            ORDINAL_SUFFIX
        ))
    }

    /// `to_ordinal_num(float/Decimal)`: `str(number) + "-inchi"`. Purely
    /// textual — nothing is parsed, so even the scientific forms succeed:
    /// `1e+16` == "1e+16-inchi", `Decimal("1E+2")` == "1E+2-inchi".
    fn ordinal_num_float_entry(&self, _value: &FloatValue, repr_str: &str) -> Result<String> {
        Ok(format!("{}{}", repr_str, ORDINAL_SUFFIX))
    }

    // `year_float_entry` is deliberately NOT overridden: KY's `to_year` is
    // `self.to_cardinal(val)`, and the trait default routes through the
    // overridden `cardinal_float_entry` above — so `to_year(5.0)` == "besh
    // üтүр nöl" and `to_year(1e+16)` raises ValueError, as the corpus pins.

    /// `converter.str_to_number` — Base's `Decimal(value)`, which KY does not
    /// override. `ParsedNumber` cannot carry Inf/NaN into KY's per-mode split
    /// (`to_cardinal` dies in `int("Infinity")` with ValueError, but
    /// `to_ordinal_num` returns "Infinity-inchi" successfully), so both
    /// return NotImplemented: the shim catches it and reruns the original
    /// pure-Python string path, which produces exactly those outcomes for
    /// every mode.
    fn str_to_number(&self, s: &str) -> Result<ParsedNumber> {
        // Inf/NaN are carried through natively now (see `inf_result` /
        // `nan_result`), so the per-mode split runs in Rust instead of the
        // Python fallback.
        python_decimal_parse(s)
    }

    /// `Decimal('Infinity')` / `Decimal('-Infinity')` per mode. KY overrides
    /// every in-scope method and reads `str(number)`:
    ///
    /// * `to_cardinal` / `to_ordinal` (== cardinal + suffix) / `to_year`
    ///   (== cardinal) do `int("Infinity")` after stripping the sign, so they
    ///   raise `ValueError` with the sign-stripped token — never OverflowError.
    /// * `to_ordinal_num` is purely `str(number) + "-inchi"`; nothing is
    ///   parsed, so it succeeds ("Infinity-inchi" / "-Infinity-inchi").
    ///
    /// The currency/fraction fallbacks also `int()` the token, so they land on
    /// the same ValueError.
    fn inf_result(&self, negative: bool, to: &str) -> Result<String> {
        match to {
            "ordinal_num" => Ok(format!(
                "{}{}",
                if negative { "-Infinity" } else { "Infinity" },
                ORDINAL_SUFFIX
            )),
            // Sign is peeled off the string before `int()`, so the message
            // always quotes the bare "Infinity".
            _ => Err(int_value_error("Infinity")),
        }
    }

    /// `Decimal('NaN')` per mode — same split as `inf_result`: the parsing
    /// modes `int("NaN")` → ValueError, while `to_ordinal_num` returns
    /// "NaN-inchi" without parsing.
    fn nan_result(&self, to: &str) -> Result<String> {
        match to {
            "ordinal_num" => Ok(format!("NaN{}", ORDINAL_SUFFIX)),
            _ => Err(int_value_error("NaN")),
        }
    }

    // ---- currency -------------------------------------------------------
    //
    // `Num2Word_KY` overrides `to_currency` and `pluralize`, and adds its own
    // `CURRENCY_FORMS`. Everything else on the currency path — `to_cheque`,
    // `_money_verbose`, `_cents_verbose`, `_cents_terse` — is inherited from
    // `Num2Word_Base` untouched, so the trait defaults already mirror it.
    //
    // It defines neither `CURRENCY_PRECISION` nor `CURRENCY_ADJECTIVES`, so
    // both stay at `Num2Word_Base`'s empty dicts: `currency_precision` is 100
    // for every code (the trait default) and `currency_adjective` is always
    // None. Not overriding them here *is* the port.

    fn lang_name(&self) -> &str {
        "Num2Word_KY"
    }

    /// `CURRENCY_FORMS[code]` — a **strict** lookup, missing code → None.
    ///
    /// This is the subscript in `Num2Word_Base.to_cheque`
    /// (`cr1, _cr2 = self.CURRENCY_FORMS[currency]`, whose `KeyError` is
    /// caught and re-raised as NotImplementedError). `to_currency` must *not*
    /// route through here — it uses `.get(currency, <first entry>)` and so
    /// never raises. That asymmetry is real and the corpus pins both halves:
    ///
    /// ```text
    /// currency:GBP 12.34 → "on eki som otuz tört tıyın"   (falls back to KGS)
    /// cheque:GBP   1234.56 → NotImplementedError
    /// ```
    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.forms.get(code)
    }

    /// Port of `Num2Word_KY.pluralize`:
    ///
    /// ```text
    /// if not forms:
    ///     return ""
    /// return forms[0] if n == 1 else forms[-1]
    /// ```
    ///
    /// Dead code in practice: KY's `to_currency` indexes `cr1`/`cr2` directly
    /// instead of calling this, and `Num2Word_Base.to_cheque` never pluralizes
    /// (it takes `cr1[-1]` unconditionally). Ported because it is a real
    /// override, and it would come alive if `to_currency` were ever reverted
    /// to Base's. Note the empty-`forms` guard — unlike `Num2Word_EUR`'s
    /// version, this one cannot raise IndexError.
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

    /// Port of `Num2Word_KY.to_currency`.
    ///
    /// ```text
    /// is_negative = val < 0
    /// val = abs(val)
    /// parts = str(val).split(".")
    /// left  = int(parts[0]) if parts[0] else 0
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
    /// A wholesale replacement of `Num2Word_Base.to_currency` that shares
    /// almost nothing with it. Four differences carry the behaviour:
    ///
    /// 1. **An unknown currency never raises.** Base subscripts the dict and
    ///    turns the `KeyError` into NotImplementedError; KY `.get`s it with the
    ///    first entry (KGS) as the default, so `currency:JPY` renders soms.
    ///    Every non-KGS/USD/EUR/RUB row in the corpus is that fallback.
    /// 2. **`CURRENCY_PRECISION` is never consulted.** The divisor is hard-wired
    ///    to 100 by `parts[1][:2]`, so the 3-decimal (KWD/BHD) and 0-decimal
    ///    (JPY) branches of Base simply do not exist — `currency:JPY 12.34` is
    ///    "on eki som otuz tört tıyın", subunits and all, where Base would round
    ///    to a whole yen and drop them.
    /// 3. **`has_decimal` is irrelevant.** Base prints a zero-cents segment for
    ///    any float; KY gates on `right` being non-zero, so `1.0` → "bir evro"
    ///    and `Decimal("5.00")` → "besh evro" (both verified live).
    /// 4. **`adjective` is accepted and ignored** — there is no
    ///    `CURRENCY_ADJECTIVES` to consult and no call to `prefix_currency`.
    ///
    /// `pluralize` is bypassed too: the forms are indexed literally.
    fn to_currency(
        &self,
        val: &CurrencyValue,
        currency: &str,
        cents: bool,
        separator: Option<&str>,
        _adjective: bool,
    ) -> Result<String> {
        // None = the caller omitted separator=, so KY's own default (" ")
        // applies. Resolved here because overriding `to_currency` bypasses the
        // trait default's body, which is where that normally happens.
        let separator = separator.unwrap_or(self.default_separator());

        // `is_negative = val < 0` — evaluated before `abs`, on the number.
        let is_negative = val.is_negative();

        let (left, right) = match val {
            // `str(int)` never contains a ".", so `parts` is one element and
            // `right` stays 0. This is why `currency:EUR 1` shows no cents
            // while `currency:EUR 1.0` goes through the branch below (and then
            // shows none anyway, because right == 0).
            CurrencyValue::Int(v) => (v.abs(), BigInt::zero()),
            CurrencyValue::Decimal { value, .. } => split_currency_parts(value)?,
        };

        // `.get(currency, list(values())[0])` — the default is always KGS.
        let forms = self
            .forms
            .get(currency)
            .or_else(|| self.forms.get(FALLBACK_CURRENCY))
            .expect("KGS is always present");
        let (cr1, cr2) = (&forms.unit, &forms.subunit);

        // `cr1[1] if left != 1 else cr1[0]` — a literal tuple index, not
        // `pluralize`. Both KY forms are identical, so the branch is invisible
        // in the output; it is kept because it is what Python evaluates.
        let unit = index_form(cr1, &left)?;
        let mut result = format!("{} {}", self.int_to_word(&left)?, unit);

        // `if cents and right:` — `right` is falsy at 0, which is what
        // suppresses the segment for "1.0" and "100.0".
        if cents && !right.is_zero() {
            let sub = index_form(cr2, &right)?;
            // Python concatenates `separator` with no space of its own: the
            // default separator " " *is* the gap. So separator="," yields
            // "on eki evro,otuz tört sent" — verified live. Do not add a
            // space here to make it look like Base's "%s%s %s%s %s %s".
            result.push_str(separator);
            result.push_str(&self.int_to_word(&right)?);
            result.push(' ');
            result.push_str(sub);
        }

        if is_negative {
            result = format!("{}{}", NEGWORD, result);
        }
        // `.strip()` — a no-op for every reachable input (`negword` is the only
        // thing that could add whitespace and it prepends), kept for fidelity.
        Ok(result.trim().to_string())
    }
}

/// `forms[1] if n != 1 else forms[0]`.
///
/// Python indexes the tuple directly, so a single-form entry with `n != 1`
/// would raise IndexError. Every `Num2Word_KY` entry has exactly two forms, so
/// that is unreachable — but it is mapped to `Index` rather than allowed to
/// panic, so the exception *type* survives if the table ever changes.
fn index_form<'a>(forms: &'a [String], n: &BigInt) -> Result<&'a str> {
    let i = if n.is_one() { 0 } else { 1 };
    forms
        .get(i)
        .map(|s| s.as_str())
        .ok_or_else(|| N2WError::Index("tuple index out of range".to_string()))
}

#[cfg(test)]
mod currency_tests {
    use super::*;
    use std::str::FromStr;

    /// Drive a `currency:<CODE>` corpus row. The corpus was generated without
    /// the `separator=` kwarg, so `None` is passed — exactly as `diff_test.py`
    /// does — which must resolve through `default_separator()` to " ".
    fn cur(arg: &str, is_int: bool, code: &str) -> String {
        let v = CurrencyValue::parse(arg, is_int, !is_int, !is_int).unwrap();
        LangKy::new()
            .to_currency(&v, code, true, None, false)
            .unwrap()
    }

    fn cheque(arg: &str, code: &str) -> Result<String> {
        LangKy::new().to_cheque(&BigDecimal::from_str(arg).unwrap(), code)
    }

    /// Every expectation is copied verbatim from the frozen corpus
    /// (`grep '"lang": "ky", "to": "currency' bench/corpus.jsonl`).
    #[test]
    fn corpus_currency_known_codes() {
        assert_eq!(cur("0", true, "EUR"), "nöl evro");
        assert_eq!(cur("1", true, "EUR"), "bir evro");
        assert_eq!(cur("2", true, "EUR"), "eki evro");
        assert_eq!(cur("100", true, "EUR"), "jüz evro");
        assert_eq!(cur("1000000", true, "EUR"), "bir million evro");
        assert_eq!(cur("12.34", false, "EUR"), "on eki evro otuz tört sent");
        assert_eq!(cur("0.01", false, "EUR"), "nöl evro bir sent");
        assert_eq!(cur("0.5", false, "EUR"), "nöl evro elüü sent");
        assert_eq!(
            cur("99.99", false, "EUR"),
            "tokson toguz evro tokson toguz sent"
        );
        assert_eq!(
            cur("1234.56", false, "EUR"),
            "min eki jüz otuz tört evro elüü alty sent"
        );
        assert_eq!(cur("-12.34", false, "EUR"), "minus on eki evro otuz tört sent");

        assert_eq!(cur("0", true, "USD"), "nöl dollar");
        assert_eq!(cur("1", true, "USD"), "bir dollar");
        assert_eq!(cur("2", true, "USD"), "eki dollar");
        assert_eq!(cur("100", true, "USD"), "jüz dollar");
        assert_eq!(cur("1000000", true, "USD"), "bir million dollar");
        assert_eq!(cur("12.34", false, "USD"), "on eki dollar otuz tört sent");
        assert_eq!(cur("0.01", false, "USD"), "nöl dollar bir sent");
        assert_eq!(cur("0.5", false, "USD"), "nöl dollar elüü sent");
        assert_eq!(
            cur("99.99", false, "USD"),
            "tokson toguz dollar tokson toguz sent"
        );
        assert_eq!(
            cur("1234.56", false, "USD"),
            "min eki jüz otuz tört dollar elüü alty sent"
        );
        assert_eq!(
            cur("-12.34", false, "USD"),
            "minus on eki dollar otuz tört sent"
        );
    }

    /// `1.0` is a float, so Python reaches `parts[1] == "0"` → `right == 0` →
    /// falsy → no cents segment. Same text as the int `1`, by a different path.
    #[test]
    fn corpus_currency_float_with_zero_cents() {
        assert_eq!(cur("1.0", false, "EUR"), "bir evro");
        assert_eq!(cur("1.0", false, "USD"), "bir dollar");
        assert_eq!(cur("1.0", false, "GBP"), "bir som");
        assert_eq!(cur("1", true, "EUR"), "bir evro");
    }

    /// Unknown codes silently render as KGS — `.get(currency, values()[0])`,
    /// never NotImplementedError. Note JPY still shows subunits and KWD/BHD
    /// are plain 100ths: KY never reads CURRENCY_PRECISION.
    #[test]
    fn corpus_currency_unknown_code_falls_back_to_kgs() {
        for code in ["GBP", "JPY", "KWD", "BHD", "INR", "CNY", "CHF"] {
            assert_eq!(cur("0", true, code), "nöl som");
            assert_eq!(cur("1", true, code), "bir som");
            assert_eq!(cur("2", true, code), "eki som");
            assert_eq!(cur("100", true, code), "jüz som");
            assert_eq!(cur("1000000", true, code), "bir million som");
            assert_eq!(cur("12.34", false, code), "on eki som otuz tört tıyın");
            assert_eq!(cur("0.01", false, code), "nöl som bir tıyın");
            assert_eq!(cur("1.0", false, code), "bir som");
            assert_eq!(cur("0.5", false, code), "nöl som elüü tıyın");
            assert_eq!(
                cur("99.99", false, code),
                "tokson toguz som tokson toguz tıyın"
            );
            assert_eq!(
                cur("1234.56", false, code),
                "min eki jüz otuz tört som elüü alty tıyın"
            );
            assert_eq!(
                cur("-12.34", false, code),
                "minus on eki som otuz tört tıyın"
            );
        }
    }

    /// Not corpus rows — each verified directly against the live interpreter,
    /// since the corpus generator never varies these kwargs.
    #[test]
    fn currency_quirks_verified_against_python() {
        let ky = LangKy::new();
        let v = CurrencyValue::parse("12.34", false, true, true).unwrap();

        // cents=False drops the segment entirely; it does NOT fall back to
        // `_cents_terse` the way Num2Word_Base would.
        assert_eq!(ky.to_currency(&v, "EUR", false, None, false).unwrap(), "on eki evro");

        // adjective is accepted and ignored (CURRENCY_ADJECTIVES is empty and
        // KY never calls prefix_currency).
        assert_eq!(
            ky.to_currency(&v, "EUR", true, None, true).unwrap(),
            "on eki evro otuz tört sent"
        );

        // KY concatenates `separator` with no space of its own, so an explicit
        // separator="," closes the gap. Live: 'on eki evro,otuz tört sent'.
        assert_eq!(
            ky.to_currency(&v, "EUR", true, Some(","), false).unwrap(),
            "on eki evro,otuz tört sent"
        );

        // parts[1][:2] truncates, never rounds: 12.345 → 34 sent, not 35.
        let v = CurrencyValue::parse("12.345", false, true, true).unwrap();
        assert_eq!(
            ky.to_currency(&v, "EUR", true, None, false).unwrap(),
            "on eki evro otuz tört sent"
        );

        // Decimal("5.00") → parts[1] == "00" → right == 0 → no cents.
        let v = CurrencyValue::parse("5.00", false, true, true).unwrap();
        assert_eq!(ky.to_currency(&v, "EUR", true, None, false).unwrap(), "besh evro");
        // float 100.0 → parts[1] == "0" → right == 0 → no cents.
        let v = CurrencyValue::parse("100.0", false, true, true).unwrap();
        assert_eq!(ky.to_currency(&v, "EUR", true, None, false).unwrap(), "jüz evro");
        // 0.0001 → parts[1][:2] == "00" → right == 0.
        let v = CurrencyValue::parse("0.0001", false, true, true).unwrap();
        assert_eq!(ky.to_currency(&v, "EUR", true, None, false).unwrap(), "nöl evro");

        // RUB is the one code the corpus never exercises.
        let v = CurrencyValue::parse("2.05", false, true, true).unwrap();
        assert_eq!(
            ky.to_currency(&v, "RUB", true, None, false).unwrap(),
            "eki rubl besh kopek"
        );

        // The 10^9 digit fallback reaches the currency path too.
        let v = CurrencyValue::parse("1000000000", true, false, false).unwrap();
        assert_eq!(ky.to_currency(&v, "EUR", true, None, false).unwrap(), "1000000000 evro");
    }

    /// `str(1e+21) == "1e+21"` → `int("1e+21")` → ValueError. The parsed
    /// BigDecimal keeps the negative scale, so the notation stays recoverable;
    /// this guards the assumption that from_str does not normalise it away.
    #[test]
    fn currency_exponential_repr_is_valueerror() {
        for arg in ["1e+21", "1e+16", "1E+2"] {
            let v = CurrencyValue::parse(arg, false, true, true).unwrap();
            match LangKy::new().to_currency(&v, "EUR", true, None, false) {
                Err(N2WError::Value(_)) => {}
                other => panic!("{} expected ValueError, got {:?}", arg, other),
            }
        }
        // Documented divergence: Python raises ValueError for the float 1e-05
        // ("1e-05" has no "."), but renders Decimal("0.00001") as "nöl evro".
        // Both parse to the same BigDecimal (int_val 1, scale 5), so the two
        // are indistinguishable here and we match the Decimal branch. See
        // `concerns` in the port report.
        assert_eq!(cur("1e-05", false, "EUR"), "nöl evro");
    }

    /// Inherited `Num2Word_Base.to_cheque` — KY adds no override. The unit is
    /// `cr1[-1]` unconditionally, and KY's forms are identical singular/plural.
    /// Verbatim from `grep '"lang": "ky", "to": "cheque' bench/corpus.jsonl`.
    #[test]
    fn corpus_cheque() {
        assert_eq!(
            cheque("1234.56", "EUR").unwrap(),
            "MIN EKI JÜZ OTUZ TÖRT AND 56/100 EVRO"
        );
        assert_eq!(
            cheque("1234.56", "USD").unwrap(),
            "MIN EKI JÜZ OTUZ TÖRT AND 56/100 DOLLAR"
        );
        // `self.CURRENCY_FORMS[currency]` → KeyError → NotImplementedError.
        // Unlike to_currency, to_cheque has no KGS fallback. This asymmetry is
        // the whole reason `currency_forms()` stays a strict lookup.
        for code in ["GBP", "JPY", "KWD", "BHD", "INR", "CNY", "CHF"] {
            match cheque("1234.56", code) {
                Err(N2WError::NotImplemented(m)) => assert_eq!(
                    m,
                    format!(
                        "Currency code \"{}\" not implemented for \"Num2Word_KY\"",
                        code
                    )
                ),
                other => panic!("{} expected NotImplementedError, got {:?}", code, other),
            }
        }
    }

    /// Not corpus rows — verified live against `Num2Word_KY().to_cheque(...)`.
    #[test]
    fn cheque_quirks_verified_against_python() {
        assert_eq!(
            cheque("1234.56", "KGS").unwrap(),
            "MIN EKI JÜZ OTUZ TÖRT AND 56/100 SOM"
        );
        // Negative → "MINUS " prefix; the whole body is upper-cased.
        assert_eq!(cheque("-1.0", "USD").unwrap(), "MINUS BIR AND 00/100 DOLLAR");
    }

    /// KY's `pluralize` is dead code on every reachable path (`to_currency`
    /// indexes the forms literally, `to_cheque` takes `cr1[-1]`), but it is a
    /// real override, so its contract is pinned here.
    #[test]
    fn pluralize_matches_python() {
        let ky = LangKy::new();
        let forms: Vec<String> = vec!["som".into(), "som".into()];
        assert_eq!(ky.pluralize(&BigInt::from(1), &forms).unwrap(), "som");
        assert_eq!(ky.pluralize(&BigInt::from(2), &forms).unwrap(), "som");
        // forms[-1], not forms[1] — a three-form entry would take the last.
        let three: Vec<String> = vec!["a".into(), "b".into(), "c".into()];
        assert_eq!(ky.pluralize(&BigInt::from(2), &three).unwrap(), "c");
        // `if not forms: return ""` — cannot raise IndexError, unlike EUR's.
        assert_eq!(ky.pluralize(&BigInt::from(2), &[]).unwrap(), "");
    }
}

#[cfg(test)]
mod float_tests {
    use super::*;
    use std::str::FromStr;

    /// Drive a `to: "cardinal"` float corpus row. `precision` is the value the
    /// Python binding computes (`abs(Decimal(str(value)).as_tuple().exponent)`)
    /// and hands across — the number of fractional digits in Python's `repr`.
    fn f(value: f64, precision: u32) -> String {
        LangKy::new()
            .to_cardinal_float(&FloatValue::Float { value, precision }, None)
            .unwrap()
    }

    /// Drive a `to: "cardinal_dec"` Decimal corpus row from its literal string.
    /// The output does not depend on the `precision` field (decompose reads the
    /// parsed scale), but it is set to the true scale for realism.
    fn d(s: &str) -> String {
        let value = BigDecimal::from_str(s).unwrap();
        let precision = value.as_bigint_and_exponent().1.max(0) as u32;
        LangKy::new()
            .to_cardinal_float(&FloatValue::Decimal { value, precision }, None)
            .unwrap()
    }

    /// Every expectation copied verbatim from the frozen corpus
    /// (`grep '"lang": "ky", "to": "cardinal", "arg": "[0-9-]*\.' ...`).
    #[test]
    fn corpus_cardinal_float() {
        assert_eq!(f(0.0, 1), "nöl üтүр nöl");
        assert_eq!(f(0.5, 1), "nöl üтүр besh");
        assert_eq!(f(1.0, 1), "bir üтүр nöl");
        assert_eq!(f(1.5, 1), "bir üтүр besh");
        assert_eq!(f(2.25, 2), "eki üтүр eki besh");
        assert_eq!(f(3.14, 2), "üch üтүр bir tört");
        assert_eq!(f(0.01, 2), "nöl üтүр nöl bir");
        assert_eq!(f(0.1, 1), "nöl üтүр bir");
        assert_eq!(f(0.99, 2), "nöl üтүр toguz toguz");
        assert_eq!(f(1.01, 2), "bir üтүр nöl bir");
        assert_eq!(f(12.34, 2), "on eki üтүр üch tört");
        assert_eq!(f(99.99, 2), "tokson toguz üтүр toguz toguz");
        assert_eq!(f(100.5, 1), "jüz üтүр besh");
        assert_eq!(f(1234.56, 2), "min eki jüz otuz tört üтүр besh alty");
        assert_eq!(f(-0.5, 1), "minus nöl üтүр besh");
        assert_eq!(f(-1.5, 1), "minus bir üтүр besh");
        assert_eq!(f(-12.34, 2), "minus on eki üтүр üch tört");
    }

    /// The two f64-artefact cases. KY sidesteps `float2tuple`'s
    /// `674.9999999999998` heuristic entirely: `str(2.675) == "2.675"` and
    /// `str(1.005) == "1.005"`, and `{:.precision}` reproduces those clean
    /// shortest-repr strings, so no rounding rescue is ever needed.
    #[test]
    fn corpus_cardinal_float_artefacts() {
        assert_eq!(f(1.005, 3), "bir üтүр nöl nöl besh");
        assert_eq!(f(2.675, 3), "eki üтүр alty jeti besh");
    }

    /// `precision_override` is inert for KY (its `to_cardinal` never consults
    /// `self.precision`). Verified live: all three digits survive regardless.
    #[test]
    fn precision_override_is_ignored() {
        let ky = LangKy::new();
        let v = FloatValue::Float { value: 2.675, precision: 3 };
        assert_eq!(ky.to_cardinal_float(&v, Some(1)).unwrap(), "eki üтүр alty jeti besh");
        assert_eq!(ky.to_cardinal_float(&v, Some(5)).unwrap(), "eki üтүр alty jeti besh");
    }

    /// Every expectation copied verbatim from the frozen corpus
    /// (`grep '"lang": "ky", "to": "cardinal_dec"' ...`). The Decimal arm keeps
    /// trailing zeros ("1.10" → "bir üтүр bir nöl"), renders the full fractional
    /// part with no `[:2]` truncation ("12.345" → three digits), and inherits
    /// the `>= 10^9` digit fallback on the integer part.
    #[test]
    fn corpus_cardinal_dec() {
        assert_eq!(d("0.01"), "nöl üтүр nöl bir");
        assert_eq!(d("1.10"), "bir üтүр bir nöl");
        assert_eq!(d("12.345"), "on eki üтүр üch tört besh");
        assert_eq!(d("98746251323029.99"), "98746251323029 üтүр toguz toguz");
        assert_eq!(d("0.001"), "nöl üтүр nöl nöl bir");
    }

    /// Not corpus rows — verified live against `num2words(Decimal(...), 'ky')`.
    /// A Decimal whose fractional part is all zeros still spells them out
    /// (unlike the currency path, where `right == 0` suppresses the segment),
    /// because KY reads the *string* form, not a numeric magnitude.
    #[test]
    fn cardinal_dec_quirks_verified_against_python() {
        assert_eq!(d("5.00"), "besh üтүр nöl nöl");
    }
}

#[cfg(test)]
mod entry_routing_tests {
    use super::*;
    use std::str::FromStr;

    fn fv(value: f64, precision: u32) -> FloatValue {
        FloatValue::Float { value, precision }
    }

    fn dv(s: &str) -> FloatValue {
        let value = BigDecimal::from_str(s).unwrap();
        let precision = value.as_bigint_and_exponent().1.max(0) as u32;
        FloatValue::Decimal { value, precision }
    }

    /// `"." in str(number)` routing — corpus_wholefloat rows, verbatim.
    #[test]
    fn corpus_cardinal_entry() {
        let ky = LangKy::new();
        // Whole floats keep their ".0" tail.
        assert_eq!(ky.cardinal_float_entry(&fv(5.0, 1), None).unwrap(), "besh üтүр nöl");
        assert_eq!(ky.cardinal_float_entry(&fv(0.0, 1), None).unwrap(), "nöl üтүр nöl");
        assert_eq!(
            ky.cardinal_float_entry(&fv(-1000000.0, 1), None).unwrap(),
            "minus bir million üтүр nöl"
        );
        // -0.0: the sign lives in the *string*, so the negword survives.
        assert_eq!(
            ky.cardinal_float_entry(&fv(-0.0, 1), None).unwrap(),
            "minus nöl üтүр nöl"
        );
        // The >= 10^9 digit fallback composes with the ".0" tail.
        assert_eq!(
            ky.cardinal_float_entry(&fv(1e9, 1), None).unwrap(),
            "1000000000 üтүр nöl"
        );
        // Decimals: trailing zeros of the literal are all spelled.
        assert_eq!(ky.cardinal_float_entry(&dv("5.00"), None).unwrap(), "besh üтүр nöl nöl");
        assert_eq!(
            ky.cardinal_float_entry(&dv("12345.000"), None).unwrap(),
            "on eki min üch jüz kırk besh üтүр nöl nöl nöl"
        );
        // Point-less integral Decimals take the integer grammar.
        assert_eq!(ky.cardinal_float_entry(&dv("0"), None).unwrap(), "nöl");
        assert_eq!(ky.cardinal_float_entry(&dv("100"), None).unwrap(), "jüz");
    }

    /// Scientific repr has no "." -> `int(n)` ValueError, message verbatim.
    #[test]
    fn corpus_cardinal_entry_scientific_is_valueerror() {
        let ky = LangKy::new();
        for (v, repr) in [(1e16, "1e+16"), (1e20, "1e+20"), (1e-5, "1e-05")] {
            match ky.cardinal_float_entry(&fv(v, 0), None) {
                Err(N2WError::Value(m)) => assert_eq!(
                    m,
                    format!("invalid literal for int() with base 10: '{}'", repr)
                ),
                other => panic!("{} expected ValueError, got {:?}", v, other),
            }
        }
        // Negative: the string sign is stripped before int(), so no minus.
        match ky.cardinal_float_entry(&fv(-1e16, 0), None) {
            Err(N2WError::Value(m)) => {
                assert_eq!(m, "invalid literal for int() with base 10: '1e+16'")
            }
            other => panic!("expected ValueError, got {:?}", other),
        }
        for (s, repr) in [("1E+2", "1E+2"), ("1E+20", "1E+20")] {
            match ky.cardinal_float_entry(&dv(s), None) {
                Err(N2WError::Value(m)) => assert_eq!(
                    m,
                    format!("invalid literal for int() with base 10: '{}'", repr)
                ),
                other => panic!("{} expected ValueError, got {:?}", s, other),
            }
        }
    }

    /// `to_ordinal(float)` = cardinal + "-inchi"; errors propagate unchanged.
    #[test]
    fn corpus_ordinal_entry() {
        let ky = LangKy::new();
        assert_eq!(
            ky.ordinal_float_entry(&fv(5.0, 1)).unwrap(),
            "besh üтүр nöl-inchi"
        );
        assert_eq!(
            ky.ordinal_float_entry(&fv(-0.0, 1)).unwrap(),
            "minus nöl üтүр nöl-inchi"
        );
        assert_eq!(
            ky.ordinal_float_entry(&fv(3.25, 2)).unwrap(),
            "üch üтүр eki besh-inchi"
        );
        assert_eq!(ky.ordinal_float_entry(&dv("0")).unwrap(), "nöl-inchi");
        assert_eq!(
            ky.ordinal_float_entry(&dv("5.00")).unwrap(),
            "besh üтүр nöl nöl-inchi"
        );
        assert!(matches!(
            ky.ordinal_float_entry(&fv(1e16, 0)),
            Err(N2WError::Value(_))
        ));
    }

    /// `to_ordinal_num(float)` = `str(number) + "-inchi"` — nothing parses,
    /// so the scientific forms succeed here.
    #[test]
    fn corpus_ordinal_num_entry() {
        let ky = LangKy::new();
        assert_eq!(
            ky.ordinal_num_float_entry(&fv(5.0, 1), "5.0").unwrap(),
            "5.0-inchi"
        );
        assert_eq!(
            ky.ordinal_num_float_entry(&fv(-0.0, 1), "-0.0").unwrap(),
            "-0.0-inchi"
        );
        assert_eq!(
            ky.ordinal_num_float_entry(&fv(1e16, 0), "1e+16").unwrap(),
            "1e+16-inchi"
        );
        assert_eq!(
            ky.ordinal_num_float_entry(&dv("1E+2"), "1E+2").unwrap(),
            "1E+2-inchi"
        );
        assert_eq!(
            ky.ordinal_num_float_entry(&dv("5.00"), "5.00").unwrap(),
            "5.00-inchi"
        );
    }

    /// `to_year(float)` — the trait default routes through the overridden
    /// `cardinal_float_entry`, giving KY's plain-cardinal years.
    #[test]
    fn corpus_year_entry() {
        let ky = LangKy::new();
        assert_eq!(ky.year_float_entry(&fv(5.0, 1)).unwrap(), "besh üтүр nöl");
        assert_eq!(
            ky.year_float_entry(&fv(-0.0, 1)).unwrap(),
            "minus nöl üтүр nöl"
        );
        assert!(matches!(
            ky.year_float_entry(&fv(1e20, 0)),
            Err(N2WError::Value(_))
        ));
    }

    /// "Infinity"/"NaN" strings fall back to Python (NotImplemented), which
    /// reproduces the per-mode split (`cardinal` ValueError vs `ordinal_num`
    /// "Infinity-inchi") that `ParsedNumber` cannot carry.
    #[test]
    fn str_to_number_inf_nan_falls_through() {
        let ky = LangKy::new();
        // Inf/NaN are now carried through natively (see `inf_result`/
        // `nan_result`), so str_to_number succeeds rather than declining.
        for s in ["Infinity", "-Infinity", "NaN"] {
            assert!(ky.str_to_number(s).is_ok());
        }
        // Everything else keeps Base's Decimal(value) semantics.
        assert!(matches!(ky.str_to_number("5"), Ok(ParsedNumber::Dec(_))));
        assert!(matches!(ky.str_to_number("1e3"), Ok(ParsedNumber::Dec(_))));
    }

    /// String inputs land on the same entries via Decimal: "1e3" parses to
    /// Decimal("1E+3"), whose point-less non-integer str raises int()'s
    /// ValueError — the corpus_strings rows for "1e3"/"1E3".
    #[test]
    fn corpus_strings_scientific_decimal_is_valueerror() {
        let ky = LangKy::new();
        match ky.cardinal_float_entry(&dv("1E+3"), None) {
            Err(N2WError::Value(m)) => {
                assert_eq!(m, "invalid literal for int() with base 10: '1E+3'")
            }
            other => panic!("expected ValueError, got {:?}", other),
        }
    }
}
