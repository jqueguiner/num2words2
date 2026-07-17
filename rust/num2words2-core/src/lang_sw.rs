//! Port of `lang_SW.py` (Swahili / Kiswahili).
//!
//! Shape: **engine**. `Num2Word_SW` subclasses `Num2Word_Base` directly and
//! defines `high_numwords` / `mid_numwords` / `low_numwords` plus `merge`, so
//! Python builds `self.cards`, sets `MAXVAL`, and lets the inherited
//! `to_cardinal` drive `splitnum`/`clean`. Cards + merge live here; the
//! default `to_cardinal` in `base.rs` does the rest.
//!
//! Registry check: `__init__.py` maps `"sw" -> lang_SW.Num2Word_SW()`, so this
//! is the class the key actually resolves to.
//!
//! # Card table
//!
//! `set_high_numwords` computes `cap = 9 + 9*len(high)` = 18 and zips
//! `high` against `range(cap, 8, -9)` = `[18, 9]`. `high` holds a single word
//! ("trilioni"), and `zip` stops at the shorter sequence, so **only** `10**18`
//! is ever registered — the `10**9` slot from the range is silently dropped
//! (1e9 comes from `mid_numwords` as "bilioni" instead). `MAXVAL` is
//! `1000 * 10**18` = `10**21`, hence `to_cardinal(10**21)` → `OverflowError`.
//!
//! Note `mid_numwords` includes `100000 -> "laki"` (a South-Asian-style lakh
//! borrowing), which sits between "elfu" (1000) and "milioni" (1e6). It is a
//! real card, so 123456 renders as "laki moja na elfu ishirini na tatu ..."
//! rather than a pure thousands decomposition.
//!
//! # Faithfully reproduced Python bugs
//!
//! This is a port, not a rewrite. The following are wrong-looking but are
//! exactly what Python emits, and are covered by the frozen corpus:
//!
//! 1. **`merge` branch 4 reverses operand order and *multiplies* whenever the
//!    right operand is >= 1e6, even when the left operand is the larger,
//!    already-merged partial.** This mangles any value that pairs a billion
//!    with a >= 1e6 remainder. The corpus pins it:
//!    `to_cardinal(1234567890)` == "milioni mia mbili na thelathini na nne na
//!    laki tano na elfu sitini na saba na mia nane na tisini bilioni moja" —
//!    i.e. the 234,567,890 remainder is emitted *before* "bilioni moja" with
//!    no "na" joining them, and the returned numeric value is `1e9 *
//!    234567890` rather than their sum. The numeric value is discarded by
//!    `to_cardinal` (only the text survives), so the bogus product is
//!    unobservable here, but the word order is. Smaller siblings such as
//!    `to_cardinal(1000000001)` are unaffected (remainder < 1e6 takes
//!    branch 3).
//!
//! 2. **Thousands are ambiguous by construction.** `to_cardinal(10001)` ==
//!    "elfu kumi na moja", which is also exactly what 11000 would read as in
//!    natural Swahili. This is why the corpus's `w2n_cardinal` rows for
//!    "elfu kumi na moja" and friends are all recorded as failures — the
//!    round trip genuinely does not close. Not our problem to fix.
//!
//! 3. **`ordinal_words` is keyed on the *whole* cardinal string, not on the
//!    last word.** So only bare "moja" and "mbili" ever get their suppletive
//!    ordinals ("kwanza"/"pili"); `to_ordinal(21)` == "wa ishirini na moja",
//!    never "...na kwanza". The remaining eight entries ("tatu" -> "tatu",
//!    ... "kumi" -> "kumi") are identity mappings and change nothing — the
//!    fallback arm would produce the same string. Kept anyway for fidelity.
//!
//! 4. **`to_currency` accepts `adjective=` and never reads it**, and spells
//!    `cents=False` as an inline `"%02d"` rather than deferring to
//!    `_cents_terse`. Both are unobservable given SW's data (empty
//!    `CURRENCY_ADJECTIVES`, divisor always 100) but both are real divergences
//!    from `Num2Word_Base.to_currency`. See [`LangSw::to_currency`].
//!
//! # Inherited from `Num2Word_Base`
//!
//! `verify_ordinal` raises `TypeError` on negatives, so `to_ordinal(-1)` and
//! `to_ordinal_num(-1)` are `N2WError::Type` — reproduced in [`LangSw::
//! verify_ordinal`]. `to_year` is overridden in Python but its body is just
//! `self.to_cardinal(value)`, identical to the base/trait default; it is
//! spelled out below to keep the mapping to the source obvious. Negative
//! years therefore render via the plain negword path
//! (`to_year(-500)` == "hasi mia tano"), with no BC/AD suffix.

use crate::base::{set_low_numwords, set_mid_numwords, Cards, Lang, N2WError, Result};
use crate::currency::{parse_currency_parts, CurrencyForms, CurrencyValue};
use bigdecimal::BigDecimal;
use num_bigint::BigInt;
use num_traits::{One, Signed, ToPrimitive, Zero};
use std::collections::HashMap;

/// `Num2Word_SW.CURRENCY_FORMS`, verbatim.
///
/// SW declares this in its own class body, so — unlike the 16 classes that read
/// `Num2Word_EUR`'s dict — it is **not** the table `Num2Word_EN.__init__`
/// mutates in place. Confirmed against the live interpreter: SW's runtime dict
/// is exactly these six codes, with none of EN's ~24 additions. Hence
/// JPY/KWD/BHD/INR/CNY/CHF all raise NotImplementedError, which the corpus pins
/// (54 of its 108 currency rows are that error).
///
/// Every entry carries two forms that are identical to each other — Swahili
/// nouns of this class do not inflect for number — so `pluralize`'s choice is
/// unobservable here. The arity is kept at Python's two all the same.
fn build_currency_forms() -> HashMap<&'static str, CurrencyForms> {
    const SENTI: [&str; 2] = ["senti", "senti"];
    const SHILINGI: [&str; 2] = ["shilingi", "shilingi"];

    let mut m: HashMap<&'static str, CurrencyForms> = HashMap::new();
    m.insert("TZS", CurrencyForms::new(&SHILINGI, &SENTI)); // Tanzanian Shilling
    m.insert("KES", CurrencyForms::new(&SHILINGI, &SENTI)); // Kenyan Shilling
    m.insert("UGX", CurrencyForms::new(&SHILINGI, &SENTI)); // Ugandan Shilling
    m.insert("USD", CurrencyForms::new(&["dola", "dola"], &SENTI)); // US Dollar
    m.insert("EUR", CurrencyForms::new(&["yuro", "yuro"], &SENTI)); // Euro
    m.insert("GBP", CurrencyForms::new(&["pauni", "pauni"], &["peni", "peni"])); // British Pound
    m
}

/// Python's `str(float)` for the values SW's fractional-cents branch can reach.
///
/// Only `to_currency(..., cents=False)` on a value with sub-cent precision gets
/// here, via `str(float(right))`. `right` is then a fractional count of cents,
/// so `0 < right < 100`; across that domain Rust's `{}` and Python's `repr`
/// agree (both are shortest-round-trip) except that Python switches to exponent
/// form below `1e-4` (`str(1e-05) == "1e-05"`, `str(0.0001) == "0.0001"`) where
/// Rust would print `"0.00001"`. Rust's `{:e}` has the right mantissa but an
/// unpadded exponent (`"1e-5"`), so the two-digit padding is reapplied.
///
/// Duplicated from the identical helper in `lang_id.rs` rather than shared: it
/// is private to that module and this port may edit only this file.
fn py_repr_float(f: f64) -> String {
    if f == 0.0 || f.abs() >= 1e-4 {
        return format!("{}", f);
    }
    let s = format!("{:e}", f);
    match s.split_once('e') {
        Some((mantissa, exp)) => {
            let (sign, digits) = match exp.strip_prefix('-') {
                Some(d) => ("-", d),
                None => ("+", exp.strip_prefix('+').unwrap_or(exp)),
            };
            format!("{}e{}{:0>2}", mantissa, sign, digits)
        }
        None => s,
    }
}

pub struct LangSw {
    cards: Cards,
    maxval: BigInt,
    ordinal_words: HashMap<&'static str, &'static str>,
    currency_forms: HashMap<&'static str, CurrencyForms>,
}

impl Default for LangSw {
    fn default() -> Self {
        Self::new()
    }
}

impl LangSw {
    pub fn new() -> Self {
        let mut cards = Cards::new();

        // set_high_numwords: cap = 9 + 9*len(high); zip(high, range(cap, 8, -9)).
        // zip() stops at the shorter sequence, so with one high word only the
        // first exponent (18) is consumed. The loop below reproduces that.
        let high = ["trilioni"];
        let cap = 9 + 9 * high.len() as i64;
        let mut n = cap;
        for word in high.iter() {
            // range(cap, 8, -9) is exhausted once n <= 8.
            if n <= 8 {
                break;
            }
            cards.insert(BigInt::from(10u8).pow(n as u32), *word);
            n -= 9;
        }

        set_mid_numwords(
            &mut cards,
            &[
                (1000000000, "bilioni"),
                (1000000, "milioni"),
                (100000, "laki"),
                (1000, "elfu"),
                (100, "mia"),
                (90, "tisini"),
                (80, "themanini"),
                (70, "sabini"),
                (60, "sitini"),
                (50, "hamsini"),
                (40, "arobaini"),
                (30, "thelathini"),
                (20, "ishirini"),
            ],
        );

        // 19 down to 0.
        set_low_numwords(
            &mut cards,
            &[
                "kumi na tisa",
                "kumi na nane",
                "kumi na saba",
                "kumi na sita",
                "kumi na tano",
                "kumi na nne",
                "kumi na tatu",
                "kumi na mbili",
                "kumi na moja",
                "kumi",
                "tisa",
                "nane",
                "saba",
                "sita",
                "tano",
                "nne",
                "tatu",
                "mbili",
                "moja",
                "sifuri",
            ],
        );

        // MAXVAL = 1000 * highest card = 1000 * 10**18 = 10**21.
        let maxval = cards.highest().cloned().unwrap_or_else(BigInt::zero) * BigInt::from(1000);

        let ordinal_words: HashMap<&str, &str> = [
            ("moja", "kwanza"),
            ("mbili", "pili"),
            ("tatu", "tatu"),
            ("nne", "nne"),
            ("tano", "tano"),
            ("sita", "sita"),
            ("saba", "saba"),
            ("nane", "nane"),
            ("tisa", "tisa"),
            ("kumi", "kumi"),
        ]
        .into_iter()
        .collect();

        LangSw {
            cards,
            maxval,
            ordinal_words,
            // Built once here, never per call: `to_currency`/`to_cheque` only
            // read this table, and rebuilding it on each call is what made an
            // earlier revision of this port slower than the Python it replaces.
            currency_forms: build_currency_forms(),
        }
    }

    /// `Num2Word_Base.verify_ordinal`. Input is integral by construction here,
    /// so only the negative check can fire — as `TypeError`, not ValueError.
    fn verify_ordinal(&self, value: &BigInt) -> Result<()> {
        if value.sign() == num_bigint::Sign::Minus {
            return Err(N2WError::Type(format!(
                "Cannot treat negative num {} as ordinal.",
                value
            )));
        }
        Ok(())
    }

    /// `Num2Word_Base.verify_ordinal` over the float/Decimal entry, plus the
    /// truncating `int(value)` the two checks perform first: NaN raises
    /// ValueError and ±inf OverflowError inside the first comparison;
    /// fractional values are `errmsg_floatord`, negative whole ones
    /// `errmsg_negord` (both TypeError). `-0.0` passes both checks and
    /// ordinalises as zero → "wa sifuri". Returns the whole value as the
    /// integer the ordinal path then renders.
    fn verify_ordinal_float(&self, value: &crate::floatpath::FloatValue) -> Result<BigInt> {
        if let crate::floatpath::FloatValue::Float { value: f, .. } = value {
            if f.is_nan() {
                return Err(N2WError::Value(
                    "cannot convert float NaN to integer".into(),
                ));
            }
            if f.is_infinite() {
                return Err(N2WError::Overflow(
                    "cannot convert float infinity to integer".into(),
                ));
            }
        }
        match value.as_whole_int() {
            None => Err(N2WError::Type(
                "Cannot treat float as ordinal.".into(),
            )),
            Some(i) if i.sign() == num_bigint::Sign::Minus => Err(N2WError::Type(format!(
                "Cannot treat negative num {} as ordinal.",
                i
            ))),
            Some(i) => Ok(i),
        }
    }
}

impl Lang for LangSw {
    /// This language's own `to_currency(currency=...)` default,
    /// read from the live Python signature. Only 44 of 156 use EUR.
    fn default_currency(&self) -> &str {
        "TZS"
    }

    /// This language's own `to_currency(separator=...)` default,
    /// read from the live Python signature. Base's is ",", but only
    /// 36 of 149 languages actually use it — most default to " " or a
    /// conjunction, so inheriting Base's comma silently corrupts them.
    fn default_separator(&self) -> &str {
        " na"
    }

    fn cards(&self) -> &Cards {
        &self.cards
    }

    fn maxval(&self) -> &BigInt {
        &self.maxval
    }

    fn negword(&self) -> &str {
        // Python's "hasi " — base strips it and re-adds one space, giving
        // "hasi " either way.
        "hasi "
    }

    fn pointword(&self) -> &str {
        "nukta"
    }

    /// Port of `Num2Word_SW.merge`.
    ///
    /// Branch order is load-bearing and reproduced verbatim. Note the Python
    /// chained comparisons: `100 > lnum > rnum` means `lnum < 100 && lnum >
    /// rnum`, and `lnum >= 100 > rnum` means `lnum >= 100 && rnum < 100`.
    fn merge(&self, l: (&str, &BigInt), r: (&str, &BigInt)) -> (String, BigInt) {
        let (ltext, lnum) = l;
        let (rtext, rnum) = r;
        let hundred = BigInt::from(100);
        let thousand = BigInt::from(1000);
        let million = BigInt::from(1000000);

        if lnum.is_one() && rnum < &hundred {
            // "moja" is absorbed: 1 * anything below 100 is just that thing.
            (rtext.to_string(), rnum.clone())
        } else if &hundred > lnum && lnum > rnum {
            // Tens + units: "ishirini na moja".
            (format!("{} na {}", ltext, rtext), lnum + rnum)
        } else if lnum >= &hundred && &hundred > rnum {
            // Big left, sub-hundred remainder: "mia moja na kumi".
            (format!("{} na {}", ltext, rtext), lnum + rnum)
        } else if rnum >= &million {
            // Millions/billions/trillions: scale word leads — "milioni moja".
            // Bug 1 lives here: this fires even when lnum is the larger,
            // already-merged partial, reversing the phrase and multiplying.
            (format!("{} {}", rtext, ltext), lnum * rnum)
        } else if rnum >= &thousand {
            if lnum < &thousand {
                // "elfu mbili"
                (format!("{} {}", rtext, ltext), lnum * rnum)
            } else {
                (format!("{} na {}", ltext, rtext), lnum + rnum)
            }
        } else if rnum >= &hundred {
            if lnum < &hundred {
                // "mia mbili"
                (format!("{} {}", rtext, ltext), lnum * rnum)
            } else {
                (format!("{} na {}", ltext, rtext), lnum + rnum)
            }
        } else if rnum > lnum {
            (format!("{} {}", ltext, rtext), lnum * rnum)
        } else {
            (format!("{} na {}", ltext, rtext), lnum + rnum)
        }
    }

    /// `wa <cardinal>`, with a suppletive lookup on the *entire* cardinal
    /// string (see bug 3). `verify_ordinal` runs first, so a negative yields
    /// `Type` even when the magnitude would also overflow.
    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        let cardinal_text = self.to_cardinal(value)?;
        match self.ordinal_words.get(cardinal_text.as_str()) {
            Some(word) => Ok(format!("wa {}", word)),
            None => Ok(format!("wa {}", cardinal_text)),
        }
    }

    /// Python: `f"{value}."` — the digits, then a full stop.
    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        Ok(format!("{}.", value))
    }

    /// `to_ordinal(float/Decimal)`: SW's `to_ordinal` opens with
    /// `verify_ordinal(value)`, so a fractional or negative value raises
    /// TypeError; a whole non-negative one rides the base `to_cardinal`
    /// whole-value route into the integer ordinal — `5.0` → "wa tano",
    /// `1.0` → "wa kwanza" (the suppletive lookup on the cardinal), `1e20` →
    /// "wa trilioni mia moja".
    fn ordinal_float_entry(&self, value: &crate::floatpath::FloatValue) -> Result<String> {
        let i = self.verify_ordinal_float(value)?;
        self.to_ordinal(&i)
    }

    /// `to_ordinal_num(float/Decimal)`: `verify_ordinal(value)`, then
    /// `f"{value}."` — the repr verbatim, ".0" tails and all: `5.0` → "5.0.",
    /// `Decimal("5.00")` → "5.00.", `-0.0` → "-0.0."; `0.5`/`-1.0` raise
    /// TypeError from the verify.
    fn ordinal_num_float_entry(
        &self,
        value: &crate::floatpath::FloatValue,
        repr_str: &str,
    ) -> Result<String> {
        self.verify_ordinal_float(value)?;
        Ok(format!("{}.", repr_str))
    }

    /// Python overrides `to_year` but the body is just `to_cardinal` — no
    /// century splitting, no BC/AD suffix, negatives fall through to negword.
    fn to_year(&self, value: &BigInt) -> Result<String> {
        self.to_cardinal(value)
    }

    // ---- currency -------------------------------------------------------
    //
    // `Num2Word_SW` overrides `to_currency` and `pluralize`, and carries its
    // own `CURRENCY_FORMS`. Everything else stays at its trait default, which
    // already matches:
    //
    // * `to_cheque` is `Num2Word_Base.to_cheque` (verified by introspection),
    //   so `currency::default_to_cheque` is exactly right — it needs only
    //   `currency_forms` + `money_verbose` from below.
    // * `_money_verbose`/`_cents_verbose` *are* defined by SW, but both bodies
    //   are `return self.to_cardinal(number)` — byte-identical to Base's and to
    //   the trait default. Overriding them here would add noise, not fidelity.
    //   (SW's own `to_currency` never calls them anyway: it calls
    //   `self.to_cardinal` directly. Only `to_cheque` reaches `_money_verbose`.)
    // * `CURRENCY_PRECISION` and `CURRENCY_ADJECTIVES` are both `{}` at runtime
    //   (SW defines neither, and EN *rebinds* rather than mutates precision, so
    //   nothing leaks in). `.get(code, 100)` is therefore always 100 and the
    //   adjective lookup always misses — the trait defaults for both.
    // * `_cents_terse` is never reached: SW's `to_currency` inlines its own
    //   `"%02d" % right` instead of calling it.

    fn lang_name(&self) -> &str {
        "Num2Word_SW"
    }

    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.currency_forms.get(code)
    }

    /// `Num2Word_SW.pluralize`: `forms[0] if len(forms) > 0 else forms`.
    ///
    /// The count is ignored outright — the docstring's reasoning is that
    /// Swahili "typically doesn't change the noun form for plurals". So this is
    /// a constant function of `forms`, and every entry in SW's table has
    /// matching singular/plural anyway.
    ///
    /// The empty-`forms` arm returns the empty *tuple* in Python, not a string;
    /// it then lands in a `"%s"` slot and renders as `"()"`. Reproduced
    /// literally rather than mapped to an exception, because Python raises
    /// nothing here. Unreachable in practice: `forms` only ever comes from
    /// `CURRENCY_FORMS`, whose every entry holds two forms.
    fn pluralize(&self, _n: &BigInt, forms: &[String]) -> Result<String> {
        Ok(forms.first().cloned().unwrap_or_else(|| "()".to_string()))
    }

    /// Port of `Num2Word_SW.to_currency`.
    ///
    /// A wholesale override that shares nothing with
    /// `Num2Word_Base.to_currency`, so `currency::default_to_currency` is
    /// deliberately not delegated to. What differs from Base, and is
    /// load-bearing:
    ///
    /// 1. **`is_int_with_cents=False`**, so a plain `int` is a count of whole
    ///    shillings, never of cents: `to_currency(100, "USD")` is
    ///    `"mia moja dola"`, not one dollar. Base would have split it.
    /// 2. **The divisor is a hardcoded 100 throughout.** SW never passes
    ///    `divisor=` to `parse_currency_parts` and has no `CURRENCY_PRECISION`,
    ///    so neither the 3-decimal (KWD/BHD) nor the 0-decimal (JPY) convention
    ///    exists here. Moot in practice — none of those codes is in SW's table,
    ///    so they raise before the divisor could matter.
    /// 3. **`adjective` is accepted and never read.** Base prefixes `cr1` with
    ///    `CURRENCY_ADJECTIVES[currency]`; SW drops the parameter on the floor.
    ///    Unobservable, since SW's `CURRENCY_ADJECTIVES` is empty and Base's
    ///    branch would miss too — but it is a real divergence in the code.
    /// 4. **`cents=False` yields `"%02d"`, not `_cents_terse`.** Same result at
    ///    divisor 100, and SW has no other divisor, so this too is unobservable.
    ///
    /// The `has_decimal or right > 0` guard is Base's and is kept: it is what
    /// makes `1.0` print `"moja yuro na sifuri senti"` while the int `1` prints
    /// `"moja yuro"`.
    fn to_currency(
        &self,
        val: &CurrencyValue,
        currency: &str,
        cents: bool,
        separator: Option<&str>,
        _adjective: bool,
    ) -> Result<String> {
        // Trait hands us None when the caller omitted separator=; resolve it to
        // this language's own default (" na") before the ported body runs.
        let separator = separator.unwrap_or(self.default_separator());

        // decimal_val = Decimal(str(val))
        // has_fractional_cents = (decimal_val * 100) % 1 != 0
        //
        // Hardcoded 100, not currency_precision() — see the doc comment. An
        // int's `str()` can never carry a remainder, so ints are always False.
        let has_fractional_cents = match val {
            CurrencyValue::Int(_) => false,
            CurrencyValue::Decimal { value, .. } => {
                // Decimal's `%` truncates toward zero, as with_scale(0) does;
                // the `!= 0` test is insensitive to the tie rule either way.
                let scaled = value * BigDecimal::from(100);
                &scaled - scaled.with_scale(0) != BigDecimal::zero()
            }
        };

        // parse_currency_parts(val, is_int_with_cents=False,
        //                      keep_precision=has_fractional_cents)
        // — divisor defaults to 100 on the Python side.
        let (left, right, is_negative) =
            parse_currency_parts(val, false, has_fractional_cents, 100);

        // Python looks the currency up *after* parsing but *before* any
        // to_cardinal call, so NotImplementedError beats an OverflowError that
        // a huge `left` would otherwise raise. Order preserved.
        let forms = self.currency_forms(currency).ok_or_else(|| {
            N2WError::NotImplemented(format!(
                "Currency code \"{}\" not implemented for \"{}\"",
                currency,
                self.lang_name()
            ))
        })?;
        let cr1 = &forms.unit;
        let cr2 = &forms.subunit;

        // negword is "hasi ": strip, then re-add one space -> "hasi ".
        let minus_str = if is_negative {
            format!("{} ", self.negword().trim())
        } else {
            String::new()
        };
        let money_str = self.to_cardinal(&left)?;

        // has_decimal = isinstance(val, float) or str(val).find(".") != -1.
        // Computed Python-side; an int can never satisfy either disjunct.
        let has_decimal = match val {
            CurrencyValue::Int(_) => false,
            CurrencyValue::Decimal { has_decimal, .. } => *has_decimal,
        };

        // Python's `int(right)`. In the whole-cents case `right` already has
        // scale 0 and this is exact; in the fractional case it is only ever fed
        // to `pluralize`, which ignores its argument.
        let right_int = right.with_scale(0).as_bigint_and_exponent().0;

        // `if has_decimal or right > 0:` — compared on the Decimal, since a
        // fractional `right` such as 1.1 must count as > 0.
        if !has_decimal && !right.is_positive() {
            return Ok(format!(
                "{}{} {}",
                minus_str,
                money_str,
                self.pluralize(&left, cr1)?
            ));
        }

        // Python: `if isinstance(right, Decimal)` — true exactly when
        // parse_currency_parts kept precision, i.e. when has_fractional_cents.
        let cents_str = if has_fractional_cents {
            // `self.to_cardinal_float(float(right)) if cents else str(float(right))`
            if cents {
                // cardinal_from_decimal's default is float-cast +
                // Num2Word_Base.to_cardinal_float — precisely this call. SW
                // inherits to_cardinal_float unchanged, so the default stands.
                self.cardinal_from_decimal(&right)?
            } else {
                let f = right
                    .to_f64()
                    .ok_or_else(|| N2WError::Value(format!("cannot represent {} as f64", right)))?;
                py_repr_float(f)
            }
        } else {
            // `self.to_cardinal(right) if cents else "%02d" % right`
            if cents {
                self.to_cardinal(&right_int)?
            } else {
                format!("{:0>2}", right_int.to_string())
            }
        };

        // "%s%s %s%s %s %s" % (minus_str, money_str, cr1_form, separator,
        //                      cents_str, cr2_form)
        // The separator abuts the unit with no space of its own, so the default
        // " na" reads "... yuro na thelathini ...".
        Ok(format!(
            "{}{} {}{} {} {}",
            minus_str,
            money_str,
            self.pluralize(&left, cr1)?,
            separator,
            cents_str,
            self.pluralize(&right_int, cr2)?
        ))
    }
}
