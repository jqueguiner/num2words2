//! String-input parsing: the Rust side of `converter.str_to_number` and the
//! `Decimal(value)` constructor semantics it relies on.
//!
//! Python's dispatcher hands string input to `str_to_number`, whose base
//! implementation is `Decimal(value)`. That constructor is *not*
//! `BigDecimal::from_str`: it strips whitespace, accepts a trailing dot
//! ("12."), PEP-515 underscores ("1_000"), any Unicode decimal digit
//! ("١٢٣"), and the special values Infinity/NaN. Reproducing its acceptance
//! set exactly is what keeps `num2words("12.")` and `num2words("abc")`
//! behaving identically to the Python original.

use crate::base::{N2WError, Result};
use bigdecimal::BigDecimal;
use num_bigint::BigInt;
use std::str::FromStr;

/// What `str_to_number` produced, including the per-language side effects
/// Python stashes on `self` for the same-call handshake.
#[derive(Debug, Clone)]
pub enum ParsedNumber {
    /// Plain `Decimal(value)`.
    Dec(BigDecimal),
    /// `Decimal("Infinity")` — representable in Python, but `int()` on it
    /// raises OverflowError, which the integer path does not catch.
    Inf { negative: bool },
    /// `Decimal("NaN")` — `int()` raises ValueError, which the base integer
    /// path *does* catch, sending NaN into the float path (where it raises).
    NaN,
    /// lang_ES: "1ro" stashes `(n, gender)`; `to_cardinal` consumes it and
    /// renders `to_ordinal(n, gender=...)` instead.
    EsOrdinal { n: BigInt, gender: char },
    /// lang_PT_BR: US-style "1.50" (dot, no comma) pronounces "ponto"
    /// instead of "vírgula" for this call only.
    DecPoint {
        value: BigDecimal,
        pointword: &'static str,
    },
}

fn invalid() -> N2WError {
    // decimal.InvalidOperation — a real class from the decimal module, so
    // `except decimal.InvalidOperation` in caller code keeps working.
    N2WError::Custom {
        module: "decimal",
        class: "InvalidOperation",
        msg: "[<class 'decimal.ConversionSyntax'>]".into(),
    }
}

/// The value of `ch` as a Unicode decimal digit, as Python's `int()` /
/// `Decimal()` accept (Nd category). Covers the blocks that show up in
/// practice; anything unlisted is rejected, which surfaces as
/// InvalidOperation exactly like a genuinely invalid character.
pub fn unicode_digit(ch: char) -> Option<u32> {
    if ch.is_ascii_digit() {
        return Some(ch as u32 - '0' as u32);
    }
    let c = ch as u32;
    for &start in &[
        0x0660, // Arabic-Indic
        0x06F0, // Extended Arabic-Indic
        0x0966, // Devanagari
        0x09E6, // Bengali
        0x0A66, // Gurmukhi
        0x0AE6, // Gujarati
        0x0B66, // Oriya
        0x0BE6, // Tamil
        0x0C66, // Telugu
        0x0CE6, // Kannada
        0x0D66, // Malayalam
        0x0E50, // Thai
        0x0ED0, // Lao
        0x0F20, // Tibetan
        0x1040, // Myanmar
        0x17E0, // Khmer
        0x1810, // Mongolian
        0xFF10, // Fullwidth
    ] {
        if (start..start + 10).contains(&c) {
            return Some(c - start);
        }
    }
    None
}

/// `any(ch.isdigit() for ch in s)` — the dispatcher's "does this string
/// contain digits" test that decides between the sentence fallback and
/// re-raising. str.isdigit() is wider than Nd (superscripts count), but the
/// decimal blocks above cover every case the library's callers hit.
pub fn has_py_digit(s: &str) -> bool {
    s.chars().any(|c| unicode_digit(c).is_some() || c.is_numeric())
}

/// Python's `Decimal(str)` constructor.
///
/// Grammar (case-insensitive, surrounding whitespace stripped):
///   sign? ( digits '.' digits? | '.' digits | digits ) ('e' sign? digits)?
///   sign? ('inf' | 'infinity')
///   sign? ('nan' | 'snan') digits?
/// PEP 515: '_' allowed only between two digits.
pub fn python_decimal_parse(s: &str) -> Result<ParsedNumber> {
    let t = s.trim();
    if t.is_empty() {
        return Err(invalid());
    }
    let lower = t.to_lowercase();
    let (sign_neg, rest) = match lower.strip_prefix('-') {
        Some(r) => (true, r),
        None => (false, lower.strip_prefix('+').unwrap_or(&lower)),
    };
    if rest == "inf" || rest == "infinity" {
        return Ok(ParsedNumber::Inf { negative: sign_neg });
    }
    if rest == "nan" || rest == "snan"
        || (rest.starts_with("nan") && rest[3..].chars().all(|c| c.is_ascii_digit()) && !rest[3..].is_empty())
        || (rest.starts_with("snan") && rest[4..].chars().all(|c| c.is_ascii_digit()) && !rest[4..].is_empty())
    {
        return Ok(ParsedNumber::NaN);
    }

    // Numeric form: normalise unicode digits to ASCII and validate the
    // shape, then let BigDecimal parse the clean ASCII.
    let src = t; // keep original case (irrelevant for digits) minus strip
    let mut out = String::with_capacity(src.len());
    let mut chars = src.chars().peekable();
    if let Some(&c) = chars.peek() {
        if c == '+' || c == '-' {
            if c == '-' {
                out.push('-');
            }
            chars.next();
        }
    }
    let mut int_digits = 0usize;
    let mut frac_digits = 0usize;
    let mut seen_dot = false;
    let mut exp_part = String::new();
    let mut prev_was_digit = false;
    while let Some(c) = chars.next() {
        if let Some(d) = unicode_digit(c) {
            out.push(char::from(b'0' + d as u8));
            if seen_dot {
                frac_digits += 1;
            } else {
                int_digits += 1;
            }
            prev_was_digit = true;
        } else if c == '_' {
            // PEP 515: must sit between two digits.
            let next_is_digit = chars.peek().is_some_and(|&n| unicode_digit(n).is_some());
            if !prev_was_digit || !next_is_digit {
                return Err(invalid());
            }
            prev_was_digit = false;
        } else if c == '.' {
            if seen_dot {
                return Err(invalid());
            }
            seen_dot = true;
            out.push('.');
            prev_was_digit = false;
        } else if c == 'e' || c == 'E' {
            // exponent: sign? digits (underscores allowed between digits)
            exp_part.push('E');
            if let Some(&sc) = chars.peek() {
                if sc == '+' || sc == '-' {
                    exp_part.push(sc);
                    chars.next();
                }
            }
            let mut exp_digits = 0usize;
            let mut prev_exp_digit = false;
            for ec in chars.by_ref() {
                if let Some(d) = unicode_digit(ec) {
                    exp_part.push(char::from(b'0' + d as u8));
                    exp_digits += 1;
                    prev_exp_digit = true;
                } else if ec == '_' {
                    if !prev_exp_digit {
                        return Err(invalid());
                    }
                    prev_exp_digit = false;
                } else {
                    return Err(invalid());
                }
            }
            if exp_digits == 0 || !prev_exp_digit {
                return Err(invalid());
            }
            break;
        } else {
            return Err(invalid());
        }
    }
    if int_digits == 0 && frac_digits == 0 {
        return Err(invalid());
    }
    // "12." is valid; BigDecimal's parser rejects a trailing dot, so drop it.
    if out.ends_with('.') {
        out.pop();
    }
    // ".5" needs a leading zero for BigDecimal.
    if out.starts_with('.') {
        out.insert(0, '0');
    } else if out.starts_with("-.") {
        out.insert(1, '0');
    }
    out.push_str(&exp_part);
    BigDecimal::from_str(&out)
        .map(ParsedNumber::Dec)
        .map_err(|_| invalid())
}

/// Python's `int(str)` — used by the "n/d" fraction-string branch. Accepts
/// surrounding whitespace, a sign, PEP-515 underscores and Unicode digits;
/// no dot, no exponent.
pub fn python_int_parse(s: &str) -> Option<BigInt> {
    let t = s.trim();
    if t.is_empty() {
        return None;
    }
    let (neg, rest) = match t.strip_prefix('-') {
        Some(r) => (true, r),
        None => (false, t.strip_prefix('+').unwrap_or(t)),
    };
    if rest.is_empty() {
        return None;
    }
    let mut ascii = String::with_capacity(rest.len());
    let mut prev_was_digit = false;
    let mut iter = rest.chars().peekable();
    while let Some(c) = iter.next() {
        if let Some(d) = unicode_digit(c) {
            ascii.push(char::from(b'0' + d as u8));
            prev_was_digit = true;
        } else if c == '_' {
            let next_is_digit = iter.peek().is_some_and(|&n| unicode_digit(n).is_some());
            if !prev_was_digit || !next_is_digit {
                return None;
            }
            prev_was_digit = false;
        } else {
            return None;
        }
    }
    let mut v = BigInt::from_str(&ascii).ok()?;
    if neg {
        v = -v;
    }
    Some(v)
}

/// Python's `str(Decimal)` — the to-scientific-string algorithm from the
/// General Decimal Arithmetic spec. Needed because `has_decimal` checks
/// `"." in str(number)` and `to_ordinal_num`'s base default returns the
/// value itself, which the dispatcher then str()s.
pub fn python_decimal_str(d: &BigDecimal) -> String {
    let (mant, scale) = d.as_bigint_and_exponent();
    let exponent = -scale; // Python's as_tuple().exponent
    let neg = mant.sign() == num_bigint::Sign::Minus;
    let digits = mant.magnitude().to_string();
    let ndigits = digits.len() as i64;
    let adjusted = exponent + ndigits - 1;
    let sign = if neg { "-" } else { "" };

    if exponent <= 0 && adjusted >= -6 {
        // Fixed-point notation.
        if exponent == 0 {
            return format!("{}{}", sign, digits);
        }
        let point = ndigits + exponent;
        if point <= 0 {
            return format!("{}0.{}{}", sign, "0".repeat((-point) as usize), digits);
        }
        let (i, f) = digits.split_at(point as usize);
        return format!("{}{}.{}", sign, i, f);
    }
    // Scientific notation.
    let exp = adjusted;
    let mantissa = if digits.len() == 1 {
        digits
    } else {
        format!("{}.{}", &digits[..1], &digits[1..])
    };
    format!("{}{}E{}{}", sign, mantissa, if exp >= 0 { "+" } else { "" }, exp)
}
