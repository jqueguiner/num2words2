//! Port of `lang_EO.py` (Esperanto).
//!
//! Shape: **engine**. `Num2Word_EO` subclasses `Num2Word_Base` directly and
//! supplies `high_numwords`/`mid_numwords`/`low_numwords` + `merge`, letting
//! the base `to_cardinal` drive `splitnum`/`clean`. So `cards`/`maxval`/`merge`
//! are all live here and the heavy lifting happens in `base.rs`.
//!
//! Inherited from `Num2Word_Base` unchanged (trait defaults do the right
//! thing):
//!   * `to_year(value) -> self.to_cardinal(value)` — EO does **not** override
//!     `to_year`, so years are plain cardinals: 1100 -> "milcent",
//!     2100 -> "du milcent", -500 -> "minus kvincent". No "BC"/"AD" suffix,
//!     no century splitting. Verified against the corpus's 36 year rows.
//!   * `title()` — `is_title` is False, so it is the identity. `exclude_title`
//!     is populated for fidelity with `setup()` but is never consulted.
//!
//! # Scale
//!
//! EO is **long scale**, built from `GIGA_SUFFIX = "iliardo"` /
//! `MEGA_SUFFIX = "iliono"`: 10^6 "miliono", 10^9 "miliardo", 10^12 "biliono",
//! 10^15 "biliardo", 10^18 "triliono", 10^21 "triliardo", ... up to
//! 10^600 "centiliono" / 10^603 "centiliardo". `MAXVAL` is
//! `1000 * 10^603 == 10^606`, hence `BigInt` throughout — this language is a
//! concrete reason `u64`/`i128` are not sufficient.
//!
//! # Faithfully reproduced Python bugs
//!
//! This is a port, not a rewrite. Both of the following look wrong and are
//! exactly what Python emits:
//!
//! 1. **`merge` adds where it should multiply.** Every arm returns
//!    `cnum + nnum`, including the `nnum >= 10**6` arm that in every sibling
//!    language (EN/EUR) returns `cnum * nnum`. So the running `num` is
//!    nonsense — `merge(("du",2), ("miliono",10^6))` yields num `1000002`,
//!    not `2000000`, and `merge(("du",2), ("cent",100))` yields `102`, not
//!    `200`. The *text* is right, but the corrupted num feeds the next
//!    `merge`'s `cnum == 1` / `cnum > 1` / `nnum >= 10**6` tests, which is
//!    how bug 2 below detonates. Do not "fix" this to `*`: it would change
//!    output.
//!
//! 2. **Spurious plural "j" mid-number**, a direct consequence of 1. The arm
//!    `nnum >= 10**6 and cnum > 1 -> "%s %sj"` is meant to pluralize an
//!    illion ("du milionoj"). But because bug 1 lets `nnum` accumulate past
//!    10^6 for a *non*-illion right operand, the "j" gets stapled onto
//!    whatever word happens to end the right fragment. Corpus proof:
//!
//!    ```text
//!    to_cardinal(1234567890)
//!      == "unu miliardo ducent tridek kvar milionoj kvincent sesdek sep mil okcent naŭdekj"
//!    ```
//!
//!    The final merge is `("unu miliardo", 1000000001)` + `("ducent ... naŭdek",
//!    1001506)`; the right num crossed 10^6 purely by accumulation, so the arm
//!    fires and appends "j" to "naŭdek" (90). The corpus also records
//!    `98746251323029.99` -> "... dudek naŭjj komo naŭ naŭ" — a *double* "j"
//!    from the same mechanism firing twice. (That row is a float and out of
//!    scope here, but it confirms the mechanism.)
//!
//! 3. `gen_high_numwords` is overridden to **drop** the Latin-elision
//!    replacement table that `lang_EUR`/`lang_EN` apply. EO therefore ships the
//!    raw concatenations: "unnonagint", "seksnonagint", "novemdek",
//!    "tredek", ... rather than the elided "unnonagint"->"unonagint" style
//!    forms. Kept verbatim — these only surface above 10^60 anyway.
//!
//! # Ordinals
//!
//! `to_ordinal` scans `self.ords` **in Python dict insertion order** and
//! returns on the first `endswith` hit. The order is load-bearing: "du"
//! precedes "dek", so "dek du" -> "dek dua" (matching "du"), while "dudek"
//! -> "dudeka" (falls through to "dek"). `ORDS` below is a `Vec`, not a
//! `HashMap`, precisely to preserve that order.
//!
//! Falling off the table appends "a", with an "o"/"oj" strip first — so
//! "unu miliono" -> "unu miliona", "dek milionoj" -> "dek miliona", and the
//! bug-2 output "...naŭdekj" -> "...naŭdekja" (ends in "j", matches neither
//! "o" nor "oj", so it just gains an "a").

use crate::base::{set_low_numwords, set_mid_numwords, Cards, Lang, N2WError, Result};
use crate::currency::CurrencyForms;
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use std::collections::HashMap;

/// `Num2Word_EO.CURRENCY_FORMS`, verbatim.
///
/// EO subclasses `Num2Word_Base` **directly**, not `Num2Word_EUR`, and declares
/// its own `CURRENCY_FORMS` class attribute. So the famous mutation trap does
/// not apply here: `Num2Word_EN.__init__` rewrites `Num2Word_EUR`'s shared class
/// dict in place, but EO never reads that dict — confirmed against the live
/// interpreter, which shows exactly these five codes and
/// `CURRENCY_FORMS is not Num2Word_Base.CURRENCY_FORMS`.
///
/// The corollary is the corpus's long tail of NotImplementedError: EO gets none
/// of the ~24 codes EN grafts on, so JPY/KWD/BHD/INR/CHF all raise. That is the
/// expected behaviour, not a gap in this table — do not "helpfully" add them.
fn build_currency_forms() -> HashMap<&'static str, CurrencyForms> {
    const CENTIMO: [&str; 2] = ["centimo", "centimoj"];

    let mut m: HashMap<&'static str, CurrencyForms> = HashMap::new();
    m.insert("EUR", CurrencyForms::new(&["eŭro", "eŭroj"], &CENTIMO));
    m.insert("USD", CurrencyForms::new(&["dolaro", "dolaroj"], &["cendo", "cendoj"]));
    m.insert("FRF", CurrencyForms::new(&["franko", "frankoj"], &CENTIMO));
    m.insert("GBP", CurrencyForms::new(&["pundo", "pundoj"], &["penco", "pencoj"]));
    m.insert("CNY", CurrencyForms::new(&["juano", "juanoj"], &["feno", "fenoj"]));
    m
}

/// Port of `Num2Word_EO.gen_high_numwords`.
///
/// Unlike `lang_EUR`'s version, EO applies **no** elision replacements — it is
/// a bare cross product, reversed, with `lows` appended. See module bug 3.
fn gen_high_numwords(units: &[&str], tens: &[&str], lows: &[&str]) -> Vec<String> {
    // Python: [u + t for t in tens for u in units] — `tens` is the OUTER loop.
    let mut out: Vec<String> = Vec::new();
    for t in tens {
        for u in units {
            out.push(format!("{}{}", u, t));
        }
    }
    out.reverse();
    out.extend(lows.iter().map(|s| s.to_string()));
    out
}

/// `self.ords`, in Python dict **insertion order**. The order decides which
/// `endswith` wins; see the module docs.
const ORDS: &[(&str, &str)] = &[
    ("unu", "unua"),
    ("du", "dua"),
    ("tri", "tria"),
    ("kvar", "kvara"),
    ("kvin", "kvina"),
    ("ses", "sesa"),
    ("sep", "sepa"),
    ("ok", "oka"),
    ("naŭ", "naŭa"),
    ("dek", "deka"),
];

pub struct LangEo {
    cards: Cards,
    maxval: BigInt,
    exclude_title: Vec<String>,
    currency_forms: HashMap<&'static str, CurrencyForms>,
}

impl Default for LangEo {
    fn default() -> Self {
        Self::new()
    }
}

impl LangEo {
    pub fn new() -> Self {
        // setup()
        let lows = ["naŭ", "ok", "sep", "ses", "kvin", "kvar", "tr", "b", "m"];
        let units = [
            "", "un", "duo", "tre", "kvatuor", "kvin", "seks", "septen", "okto", "novem",
        ];
        let tens = [
            "dek",
            "vigint",
            "trigint",
            "kvadragint",
            "kvinkvagint",
            "seksagint",
            "septuagint",
            "oktogint",
            "nonagint",
        ];

        // high_numwords = ["cent"] + gen_high_numwords(...) -> 1 + 90 + 9 = 100
        let mut high = vec!["cent".to_string()];
        high.extend(gen_high_numwords(&units, &tens, &lows));

        let mut cards = Cards::new();

        // set_high_numwords: cap = 3 + 6*len(high); zip(high, range(cap, 3, -6)).
        // Both sides are length 100, but `zip` stops at the shorter, so the
        // `n <= 3` break reproduces the range exhausting first if `high` ever
        // grew. GIGA/MEGA suffixes are both non-empty, so both arms always run.
        const GIGA_SUFFIX: &str = "iliardo";
        const MEGA_SUFFIX: &str = "iliono";
        let cap = 3 + 6 * high.len() as u32;
        let ten = BigInt::from(10u8);
        let mut n = cap;
        for word in high.iter() {
            if n <= 3 {
                break;
            }
            cards.insert(ten.pow(n), format!("{}{}", word, GIGA_SUFFIX));
            cards.insert(ten.pow(n - 3), format!("{}{}", word, MEGA_SUFFIX));
            n -= 6;
        }

        set_mid_numwords(
            &mut cards,
            &[
                (1000, "mil"),
                (100, "cent"),
                (90, "naŭdek"),
                (80, "okdek"),
                (70, "sepdek"),
                (60, "sesdek"),
                (50, "kvindek"),
                (40, "kvardek"),
                (30, "tridek"),
            ],
        );
        set_low_numwords(
            &mut cards,
            &[
                "dudek", "dek naŭ", "dek ok", "dek sep", "dek ses", "dek kvin", "dek kvar",
                "dek tri", "dek du", "dek unu", "dek", "naŭ", "ok", "sep", "ses", "kvin", "kvar",
                "tri", "du", "unu", "nul",
            ],
        );

        // MAXVAL = 1000 * list(self.cards.keys())[0] — the first-inserted key is
        // the largest (10^603), and Cards is sorted descending, so `highest()`
        // is the same element. MAXVAL == 10^606.
        let maxval = cards.highest().cloned().unwrap_or_else(BigInt::zero) * BigInt::from(1000);

        LangEo {
            cards,
            maxval,
            exclude_title: vec!["kaj".into(), "komo".into(), "minus".into()],
            // Built once here, never per call: `to_currency` only reads it, and
            // rebuilding the table on every call is what made an earlier
            // revision of this port slower than the Python it replaces.
            currency_forms: build_currency_forms(),
        }
    }

    /// `Num2Word_Base.verify_ordinal`. Integral input clears the first check
    /// (`value == int(value)`) unconditionally; only the negative check can fire.
    fn verify_ordinal(&self, value: &BigInt) -> Result<()> {
        if value.is_negative() {
            return Err(N2WError::Type(format!(
                "Cannot treat negative num {} as ordinal.",
                value
            )));
        }
        Ok(())
    }

    /// `Num2Word_Base.verify_ordinal` over the float/Decimal entry, plus the
    /// truncating `int(value)` the two checks perform first. Rules, in
    /// Python's order:
    ///
    /// * `int(nan)` raises ValueError and `int(±inf)` OverflowError *inside*
    ///   the first comparison, before either TypeError arm can fire;
    /// * a fractional value (`value != int(value)`) is `errmsg_floatord` —
    ///   EO inherits base's English message;
    /// * a negative whole value (`abs(value) != value`) is `errmsg_negord`.
    ///   `-0.0` passes both checks (`abs(-0.0) == -0.0`) and ordinalises as
    ///   zero → "nula".
    ///
    /// Returns the whole value as the integer the ordinal path then renders.
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
            Some(i) if i.is_negative() => Err(N2WError::Type(format!(
                "Cannot treat negative num {} as ordinal.",
                i
            ))),
            Some(i) => Ok(i),
        }
    }
}

impl Lang for LangEo {
    /// This language's own `to_currency(currency=...)` default,
    /// read from the live Python signature. Only 44 of 156 use EUR.
    fn default_currency(&self) -> &str {
        "EUR"
    }

    /// This language's own `to_currency(separator=...)` default,
    /// read from the live Python signature. Base's is ",", but only
    /// 36 of 149 languages actually use it — most default to " " or a
    /// conjunction, so inheriting Base's comma silently corrupts them.
    fn default_separator(&self) -> &str {
        " kaj"
    }

    fn cards(&self) -> &Cards {
        &self.cards
    }
    fn maxval(&self) -> &BigInt {
        &self.maxval
    }
    fn negword(&self) -> &str {
        "minus "
    }
    fn pointword(&self) -> &str {
        "komo"
    }
    fn exclude_title(&self) -> &[String] {
        &self.exclude_title
    }

    /// Port of `Num2Word_EO.merge`. Note every arm returns `cnum + nnum` —
    /// never a product. That is the Python source's behaviour and it is
    /// load-bearing; see module bugs 1 and 2.
    fn merge(&self, l: (&str, &BigInt), r: (&str, &BigInt)) -> (String, BigInt) {
        let (ctext, cnum) = l;
        let (ntext, nnum) = r;
        let million = BigInt::from(1_000_000u32);
        let hundred = BigInt::from(100u8);
        let one = BigInt::one();

        if cnum == &one && nnum < &million {
            return (ntext.to_string(), nnum.clone());
        }
        if nnum >= &million && cnum > &one {
            return (format!("{} {}j", ctext, ntext), cnum + nnum);
        }
        if nnum == &hundred {
            return (format!("{}{}", ctext, ntext), cnum + nnum);
        }
        (format!("{} {}", ctext, ntext), cnum + nnum)
    }

    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        let word = self.to_cardinal(value)?;

        // Python: `for src, repl in self.ords.items(): if word.endswith(src):
        //          return word[:-len(src)] + repl`
        // `len(src)` is a CHAR count, but since `src` matched as a suffix the
        // last `len(src)` chars are exactly `src` — so dropping the matched
        // suffix's bytes is provably identical, and `strip_suffix` is safe on
        // the multi-byte "naŭ" (3 chars / 4 bytes).
        for &(src, repl) in ORDS {
            if let Some(head) = word.strip_suffix(src) {
                return Ok(format!("{}{}", head, repl));
            }
        }

        // The "o"/"oj" arms are mutually exclusive and both reachable: a word
        // ending "oj" does not end "o", so the elif is live (e.g.
        // "dek milionoj" -> "dek miliona").
        if let Some(head) = word.strip_suffix('o') {
            Ok(format!("{}a", head))
        } else if let Some(head) = word.strip_suffix("oj") {
            Ok(format!("{}a", head))
        } else {
            Ok(format!("{}a", word))
        }
    }

    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        Ok(format!("{}a", value))
    }

    /// `to_ordinal(float/Decimal)`: EO's `to_ordinal` opens with
    /// `verify_ordinal(value)`, so a fractional or negative value raises
    /// TypeError; a whole non-negative one then rides the base `to_cardinal`
    /// whole-value route into the integer ordinal — `5.0` → "kvina",
    /// `Decimal("1E+2")` → "centa", `1e16` → "dek biliarda".
    fn ordinal_float_entry(&self, value: &crate::floatpath::FloatValue) -> Result<String> {
        let i = self.verify_ordinal_float(value)?;
        self.to_ordinal(&i)
    }

    /// `to_ordinal_num(float/Decimal)`: `verify_ordinal(value)`, then
    /// `str(value) + "a"` — the repr verbatim, ".0" tails and all: `5.0` →
    /// "5.0a", `Decimal("5.00")` → "5.00a", `-0.0` → "-0.0a"; `0.5`/`-1.0`
    /// raise TypeError from the verify.
    fn ordinal_num_float_entry(
        &self,
        value: &crate::floatpath::FloatValue,
        repr_str: &str,
    ) -> Result<String> {
        self.verify_ordinal_float(value)?;
        Ok(format!("{}a", repr_str))
    }

    // to_year is NOT overridden in Python; the trait default delegates to
    // to_cardinal through &self, which is exactly right.

    // ---- currency -------------------------------------------------------
    //
    // `Num2Word_EO` overrides only `CURRENCY_FORMS` and `pluralize`. Its
    // `to_currency` override is a pure pass-through — it re-declares the
    // signature to change `separator`'s default to " kaj", then calls
    // `super().to_currency(...)` and returns the result untouched. That default
    // already lives in `default_separator()` above and the trait resolves it
    // before the body runs, so there is nothing left for a `to_currency`
    // override to do here.
    //
    // Everything else comes from `Num2Word_Base` unchanged, and the trait
    // defaults already mirror it:
    //   * `to_cheque`, `_money_verbose`, `_cents_verbose`, `_cents_terse`.
    //   * `CURRENCY_ADJECTIVES` is `{}` — the default `currency_adjective()`
    //     returns None, so `adjective=True` is a no-op for every code.
    //   * `CURRENCY_PRECISION` is `{}` — every code divides by 100. This is
    //     load-bearing for the corpus's JPY rows: with no precision entry the
    //     `divisor == 1` pre-rounding branch never fires, so JPY falls straight
    //     through to the forms lookup and raises NotImplementedError like any
    //     other unknown code.

    fn lang_name(&self) -> &str {
        "Num2Word_EO"
    }

    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.currency_forms.get(code)
    }

    /// `Num2Word_EO.pluralize`: `forms[0 if n <= 1 else 1]`.
    ///
    /// Note `n <= 1`, **not** EUR/EN's `n == 1`. The difference is observable at
    /// zero and drives four corpus rows: `to_currency(0)` is "nul eŭro" (not
    /// "nul eŭroj"), and `1.0` renders "unu eŭro kaj nul centimo" — a singular
    /// subunit after "nul". Esperanto actually wants the plural after zero, so
    /// this is a genuine Python bug; it is reproduced deliberately.
    ///
    /// Python indexes the tuple directly, so a one-form entry with `n > 1` would
    /// raise IndexError. Every EO entry has two forms, making that unreachable —
    /// but it is mapped to `Index` rather than a panic so the exception type
    /// survives if the table ever changes.
    fn pluralize(&self, n: &BigInt, forms: &[String]) -> Result<String> {
        let form = if n <= &BigInt::one() { 0 } else { 1 };
        forms
            .get(form)
            .cloned()
            .ok_or_else(|| N2WError::Index("tuple index out of range".into()))
    }
}
