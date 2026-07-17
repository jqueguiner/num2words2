//! Port of `lang_TG.py` (Tajik), via its `lang_EUR` → `Num2Word_Base` ancestry.
//!
//! Shape: **engine**. `Num2Word_TG` supplies `high_numwords`/`mid_numwords`/
//! `low_numwords` + `merge`, so Python builds `self.cards` and `MAXVAL` in
//! `Num2Word_Base.__init__` and folds via `splitnum`/`clean`. `to_cardinal` is
//! overridden, but only to bolt a `value == 100` special case onto the base
//! algorithm — the tree walk itself is still `base.py`'s, so `splitnum`/`clean`
//! from `base.rs` are reused verbatim.
//!
//! # Inheritance notes (chased through the chain)
//!
//! * `TG.setup()` calls `super().setup()` (= `Num2Word_EUR.setup()`), which
//!   assigns the full Latin-prefix `high_numwords` list — and then TG
//!   **immediately overwrites it** with `gen_high_numwords([], [], lows)`.
//!   With `units` and `tens` both empty, the `[u + t for t in tens for u in
//!   units]` comprehension yields `[]`, the reverse and the 18 elision
//!   replacements are no-ops, and the result is just `lows` verbatim:
//!   `["квинт", "квадр", "тр", "м", "м"]`. So EUR's expensive name generation
//!   is dead code for Tajik and is not reproduced here.
//! * `TG.set_high_numwords` overrides `EUR`'s (step -3 with a `n == 9` giga
//!   check, not EUR's -6 illiard/illion pairing). `cap = 3 * (len(high) + 1)`
//!   = 18, and `zip(high, range(18, 5, -3))` pairs the 5 stems with
//!   `[18, 15, 12, 9, 6]` exactly — neither sequence is truncated.
//! * `MAXVAL = 1000 * list(self.cards.keys())[0]`. The first key inserted is
//!   `10**18`, which is also the largest, so `Cards::highest()` agrees with
//!   Python's insertion-order lookup. MAXVAL = `10**21`.
//! * `is_title` stays `False` (base default), so `title()` is the identity.
//!   `exclude_title` is carried anyway for faithfulness.
//! * `to_year` is **not** overridden anywhere in the chain, so it stays
//!   `Num2Word_Base.to_year(value) -> self.to_cardinal(value)`. The trait
//!   default does exactly that and picks up the `to_cardinal` override below,
//!   so it is deliberately left alone.
//! * `verify_ordinal` is `Num2Word_Base`'s: negatives raise `TypeError`
//!   ("Cannot treat negative num %s as ordinal."). Integer input can never
//!   trip the float branch.
//!
//! # Quirks reproduced verbatim
//!
//! 1. `to_cardinal` special-cases `value == 100` → "сад" *after* stripping the
//!    sign, so `to_cardinal(-100)` == "минус сад". Without that early return
//!    `splitnum(100)`/`merge` would have produced "яксад" (as it still does
//!    inside larger numbers: 1100 → "як ҳазору яксад"). The bare "сад" form
//!    therefore only ever appears at top level.
//! 2. `TG.to_cardinal` writes `out = self.negword` where `Num2Word_Base` writes
//!    `out = "%s " % self.negword.strip()`. Because `negword` is "минус " —
//!    already trailing-space — both spellings produce the identical "минус ".
//!    Kept as the raw `negword` to mirror the source.
//! 3. `merge`'s "яксад" arm (`ltext == "яксад" and rtext not in
//!    self.low_numwords` → "сад %s") is what makes 100_000 render "сад ҳазор"
//!    rather than "яксад ҳазор". The `rtext not in low_numwords` guard is
//!    effectively dead: it is only consulted on the `rnum > lnum` arm, where
//!    `lnum == 100` forces `rnum > 100`, while every `low_numwords` entry maps
//!    to a value ≤ 20. It is preserved regardless.
//! 4. `merge` hard-codes the joiners by *text*, not by value: "си" takes "ю "
//!    (30 → "сию як") and "панҷоҳ" is rewritten wholesale to "панҷову"
//!    (50 → "панҷову панҷ"), while every other ten takes "у " (20 → "бисту
//!    як"). String comparison, not arithmetic — ported as such.
//! 5. `to_ordinal_num` slices `self.to_ordinal(value)[-2:]` — the last two
//!    *characters* of a Cyrillic string. Sliced via `chars()`, never bytes.
//! 6. `to_currency(..., adjective=True)` prefixes USD/RUB with the *English*
//!    adjectives inherited from `lang_EUR` ("ду US доллар"). See
//!    `build_currency_adjectives`.
//! 7. The `value == 100` cardinal special case reaches the currency surface
//!    through `_money_verbose`, so `to_currency(100, "EUR")` is "сад евро" —
//!    not the "яксад евро" that `splitnum`/`merge` alone would give.
//!
//! No cross-call mutable state: every method here is a pure function of its
//! argument plus the immutable tables built in `new()`.

use crate::base::{
    clean, set_low_numwords, set_mid_numwords, splitnum, Cards, Lang, N2WError, Node, Result,
};
use crate::currency::CurrencyForms;
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use std::collections::HashMap;

/// `Num2Word_TG.GIGA_SUFFIX`.
const GIGA_SUFFIX: &str = "иллиард";
/// `Num2Word_TG.MEGA_SUFFIX`.
const MEGA_SUFFIX: &str = "иллион";

/// `self.low_numwords`, in source order (index 0 → 20, index 20 → 0).
///
/// Kept as a standalone table because `merge` tests membership against the
/// *list* (`rtext not in self.low_numwords`), independently of `cards`.
const LOW_NUMWORDS: [&str; 21] = [
    "бист",
    "нуздаҳ",
    "ҳаждаҳ",
    "ҳабдаҳ",
    "шонздаҳ",
    "понздаҳ",
    "чордаҳ",
    "сенздаҳ",
    "дувоздаҳ",
    "ёздаҳ",
    "даҳ",
    "нӯҳ",
    "ҳашт",
    "ҳафт",
    "шаш",
    "панҷ",
    "чор",
    "се",
    "ду",
    "як",
    "сифр",
];

/// `Num2Word_TG.CURRENCY_FORMS`, verbatim from the class body.
///
/// **This table is TG's own class attribute, so the `lang_EUR` mutation trap
/// does not apply here.** `Num2Word_EN.__init__` rewrites
/// `Num2Word_EUR.CURRENCY_FORMS` in place (`self.CURRENCY_FORMS["EUR"] = ...`)
/// and adds ~24 codes to it, which leaks into every subclass that *inherits*
/// the dict. TG rebinds `CURRENCY_FORMS` in its own class body, so it shadows
/// EUR's attribute entirely: EN's writes land on the ancestor and are never
/// seen. Four codes is all Tajik has, and the corpus agrees — GBP, JPY, KWD,
/// BHD, INR, CNY and CHF all raise NotImplementedError for `tg` even though
/// English-inheriting languages resolve them.
///
/// Both forms of every entry are identical: Tajik does not inflect these nouns
/// for number, so `pluralize`'s index choice is unobservable. The two-element
/// arity is kept exactly as Python has it — `pluralize` indexes `forms[1]` for
/// every `n != 1`, and collapsing to one form would turn that into an
/// IndexError.
fn build_currency_forms() -> HashMap<&'static str, CurrencyForms> {
    // lang_TG.GENERIC_DOLLARS / GENERIC_CENTS — note both are singular-shaped,
    // unlike lang_EUR's ("dollar", "dollars").
    const GENERIC_DOLLARS: [&str; 2] = ["доллар", "доллар"];
    const GENERIC_CENTS: [&str; 2] = ["сент", "сент"];

    let mut m: HashMap<&'static str, CurrencyForms> = HashMap::new();
    // "repalced by EUR" [sic — the typo is in the Python source]
    m.insert("EUR", CurrencyForms::new(&["евро", "евро"], &GENERIC_CENTS));
    // "replaced by EUR"
    m.insert("USD", CurrencyForms::new(&GENERIC_DOLLARS, &GENERIC_CENTS));
    m.insert("RUB", CurrencyForms::new(&["рубл", "рубл"], &["копейк", "копейк"]));
    m.insert("TJS", CurrencyForms::new(&["сомонӣ", "сомонӣ"], &["дирам", "дирам"]));
    m
}

/// `Num2Word_EUR.CURRENCY_ADJECTIVES`, inherited unchanged.
///
/// TG defines no `CURRENCY_ADJECTIVES` of its own, so it reads EUR's — and
/// unlike `CURRENCY_FORMS`, EN never mutates this dict, so what EUR's class
/// body declares is what TG sees. The list is therefore transcribed in full
/// rather than trimmed to TG's four codes, because that is literally the
/// object Python hands to `currency in self.CURRENCY_ADJECTIVES`.
///
/// **Quirk reproduced**: only USD and RUB intersect TG's `CURRENCY_FORMS`, and
/// their adjectives are the inherited *English* ones. So
/// `to_currency(2, "USD", adjective=True)` is "ду US доллар" and RUB is
/// "ду Russian рубл" — English adjectives glued onto Tajik nouns. The other 14
/// entries are unreachable: `to_currency` looks `CURRENCY_FORMS` up first and
/// raises NotImplementedError before the adjective branch can fire.
fn build_currency_adjectives() -> HashMap<&'static str, &'static str> {
    [
        ("AUD", "Australian"),
        ("BYN", "Belarusian"),
        ("CAD", "Canadian"),
        ("EEK", "Estonian"),
        ("USD", "US"),
        ("RUB", "Russian"),
        ("NOK", "Norwegian"),
        ("MXN", "Mexican"),
        ("RON", "Romanian"),
        ("INR", "Indian"),
        ("HUF", "Hungarian"),
        ("ISK", "íslenskar"),
        ("UZS", "Uzbekistan"),
        ("SAR", "Saudi"),
        ("JPY", "Japanese"),
        ("KRW", "Korean"),
    ]
    .into_iter()
    .collect()
}

pub struct LangTg {
    cards: Cards,
    maxval: BigInt,
    exclude_title: Vec<String>,
    hundred: BigInt,
    currency_forms: HashMap<&'static str, CurrencyForms>,
    currency_adjectives: HashMap<&'static str, &'static str>,
}

impl Default for LangTg {
    fn default() -> Self {
        Self::new()
    }
}

impl LangTg {
    pub fn new() -> Self {
        let mut cards = Cards::new();

        // TG.set_high_numwords(high), high = gen_high_numwords([], [], lows) = lows.
        // cap = 3 * (len(high) + 1) = 18; zip(high, range(cap, 5, -3)).
        let high = ["квинт", "квадр", "тр", "м", "м"];
        let cap = 3 * (high.len() as i64 + 1);
        let mut n = cap;
        for word in high.iter() {
            // range(cap, 5, -3) is exhausted at n <= 5; zip() stops with it.
            if n <= 5 {
                break;
            }
            let suffix = if n == 9 { GIGA_SUFFIX } else { MEGA_SUFFIX };
            cards.insert(BigInt::from(10u8).pow(n as u32), format!("{}{}", word, suffix));
            n -= 3;
        }

        set_mid_numwords(
            &mut cards,
            &[
                (1000, "ҳазор"),
                (100, "сад"),
                (90, "навад"),
                (80, "ҳаштод"),
                (70, "ҳафтод"),
                (60, "шаст"),
                (50, "панҷоҳ"),
                (40, "чил"),
                (30, "си"),
            ],
        );
        set_low_numwords(&mut cards, &LOW_NUMWORDS);

        // MAXVAL = 1000 * list(self.cards.keys())[0]. First-inserted key is
        // 10**18, which is also the maximum → 10**21.
        let maxval = cards.highest().cloned().unwrap_or_else(BigInt::zero) * BigInt::from(1000);

        LangTg {
            cards,
            maxval,
            exclude_title: vec!["ва".into(), "минус".into(), "нуқта".into()],
            hundred: BigInt::from(100),
            // Built once here, never per call. `to_currency`/`to_cheque` only
            // ever read these tables, so rebuilding them per invocation would
            // be pure overhead on the hot path.
            currency_forms: build_currency_forms(),
            currency_adjectives: build_currency_adjectives(),
        }
    }

    /// `Num2Word_Base.verify_ordinal`. The float branch is unreachable for
    /// integer input; only the negative branch can fire.
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
    /// truncating `int(value)` the two checks perform first: NaN raises
    /// ValueError and ±inf OverflowError inside the first comparison;
    /// fractional values are `errmsg_floatord`, negative whole ones
    /// `errmsg_negord` (both TypeError). `-0.0` passes both checks and
    /// ordinalises as zero → "сифрум". Returns the whole value as the
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
            Some(i) if i.is_negative() => Err(N2WError::Type(format!(
                "Cannot treat negative num {} as ordinal.",
                i
            ))),
            Some(i) => Ok(i),
        }
    }
}

impl Lang for LangTg {
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
        ","
    }

    fn cards(&self) -> &Cards {
        &self.cards
    }
    fn maxval(&self) -> &BigInt {
        &self.maxval
    }
    fn negword(&self) -> &str {
        "минус "
    }
    fn pointword(&self) -> &str {
        "нуқта"
    }
    fn exclude_title(&self) -> &[String] {
        &self.exclude_title
    }

    fn merge(&self, l: (&str, &BigInt), r: (&str, &BigInt)) -> (String, BigInt) {
        let (ltext, lnum) = l;
        let (rtext, rnum) = r;
        let hundred = &self.hundred;

        if lnum.is_one() && rnum < hundred {
            (rtext.to_string(), rnum.clone())
        } else if hundred > lnum && lnum > rnum {
            if ltext == "си" {
                (format!("{}ю {}", ltext, rtext), lnum + rnum)
            } else if ltext == "панҷоҳ" {
                // Python drops ltext entirely here and hard-codes the stem.
                (format!("панҷову {}", rtext), lnum + rnum)
            } else {
                (format!("{}у {}", ltext, rtext), lnum + rnum)
            }
        } else if lnum >= hundred && hundred > rnum {
            (format!("{}у {}", ltext, rtext), lnum + rnum)
        } else if rnum > lnum {
            if ltext == "яксад" && !LOW_NUMWORDS.contains(&rtext) {
                (format!("сад {}", rtext), lnum * rnum)
            } else if rtext == "сад" {
                // Glued, no space: 2 * 100 → "дусад".
                (format!("{}{}", ltext, rtext), lnum * rnum)
            } else {
                (format!("{} {}", ltext, rtext), lnum * rnum)
            }
        } else {
            (format!("{}у {}", ltext, rtext), lnum + rnum)
        }
    }

    fn to_cardinal(&self, value: &BigInt) -> Result<String> {
        let mut out = String::new();
        let mut v = value.clone();
        if v.is_negative() {
            v = v.abs();
            // TG uses `self.negword` raw (base uses "%s " % negword.strip());
            // identical here because negword already ends in a space.
            out = self.negword().to_string();
        }

        if v >= self.maxval {
            return Err(N2WError::Overflow(format!(
                "abs({}) must be less than {}.",
                v, self.maxval
            )));
        }

        // The 100 special case runs *after* the sign strip, so -100 is
        // "минус сад".
        if v == self.hundred {
            return Ok(self.title(&format!("{}сад", out)));
        }

        // `splitnum` cannot return None here: `cards` contains 0 and `v >= 0`,
        // so the scan always finds a card. (Python would TypeError unpacking
        // None if it ever did.)
        let tree = splitnum(self, &v).ok_or_else(|| {
            N2WError::Type(format!("type({}) not in [long, int, float]", v))
        })?;
        let words = match clean(self, tree) {
            Node::Leaf(t, _) => t,
            Node::List(_) => return Err(N2WError::Type("clean did not reduce".into())),
        };
        Ok(self.title(&format!("{}{}", out, words)))
    }

    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        let cardinal = self.to_cardinal(value)?;
        // Python: cardinal.split(" ") — never empty, so last() always exists.
        let lastword = cardinal.split(' ').next_back().unwrap_or("");
        if lastword == "ду" || lastword == "се" || lastword == "си" {
            Ok(format!("{}юм", cardinal))
        } else {
            Ok(format!("{}ум", cardinal))
        }
    }

    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        let ord = self.to_ordinal(value)?;
        // Python: "%s%s" % (value, self.to_ordinal(value)[-2:]) — last two
        // *characters*, not bytes (every suffix here is Cyrillic).
        let n = ord.chars().count();
        let suffix: String = ord.chars().skip(n.saturating_sub(2)).collect();
        Ok(format!("{}{}", value, suffix))
    }

    /// `to_ordinal(float/Decimal)`: TG's `to_ordinal` opens with
    /// `verify_ordinal(value)`, so a fractional or negative value raises
    /// TypeError; a whole non-negative one rides the base `to_cardinal`
    /// whole-value route into the integer ordinal — `5.0` → "панҷум",
    /// `2.0` → "дуюм" (the last-word "ду"/"се"/"си" rule picks "юм").
    fn ordinal_float_entry(&self, value: &crate::floatpath::FloatValue) -> Result<String> {
        let i = self.verify_ordinal_float(value)?;
        self.to_ordinal(&i)
    }

    /// `to_ordinal_num(float/Decimal)`: `verify_ordinal(value)`, then
    /// `"%s%s" % (value, self.to_ordinal(value)[-2:])` — the repr verbatim
    /// plus the last two *characters* of the spoken ordinal of the same
    /// (whole) value: `5.0` → "5.0ум", `2.0` → "2.0юм",
    /// `Decimal("5.00")` → "5.00ум", `-0.0` → "-0.0ум"; `0.5`/`-1.0` raise
    /// TypeError from the verify.
    fn ordinal_num_float_entry(
        &self,
        value: &crate::floatpath::FloatValue,
        repr_str: &str,
    ) -> Result<String> {
        let i = self.verify_ordinal_float(value)?;
        let ord = self.to_ordinal(&i)?;
        let n = ord.chars().count();
        let suffix: String = ord.chars().skip(n.saturating_sub(2)).collect();
        Ok(format!("{}{}", repr_str, suffix))
    }

    // to_year is intentionally NOT overridden: neither TG, EUR nor Base
    // define anything but `to_year(value) -> self.to_cardinal(value)`, which
    // is exactly the trait default.

    // ---- currency -------------------------------------------------------
    //
    // Verified against the live interpreter: `to_currency`, `to_cheque`,
    // `_money_verbose`, `_cents_verbose` and `_cents_terse` all resolve to
    // `Num2Word_Base` for TG, and `pluralize` to `Num2Word_EUR`. So the only
    // language-specific things are the class name, the two data tables and
    // that one plural rule — the trait defaults already mirror everything
    // else, and are deliberately left alone.
    //
    // `currency_precision` is **not** overridden: TG's `CURRENCY_PRECISION` is
    // Base's empty dict (EN *rebinds* rather than mutates it, in `__init__`,
    // so its 3-decimal entries never leak), which makes
    // `CURRENCY_PRECISION.get(code, 100)` unconditionally 100 — exactly the
    // trait default. TG therefore has no 3-decimal and no 0-decimal currency:
    // KWD/BHD carry divisor 100, not 1000, and JPY 100, not 1. All four are
    // absent from `CURRENCY_FORMS` anyway, so they raise NotImplementedError
    // before precision is ever consulted, and `default_to_currency`'s
    // `divisor == 1` branch is unreachable for Tajik.

    fn lang_name(&self) -> &str {
        "Num2Word_TG"
    }

    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.currency_forms.get(code)
    }

    fn currency_adjective(&self, code: &str) -> Option<&str> {
        self.currency_adjectives.get(code).copied()
    }

    /// `Num2Word_EUR.pluralize`: `forms[0 if n == 1 else 1]`.
    ///
    /// Python indexes the tuple directly, so a one-form entry with `n != 1`
    /// would raise IndexError. Every TG entry has exactly two forms, so this
    /// is unreachable — but it is mapped to `Index` rather than panicking so
    /// the exception *type* survives if the table ever changes.
    ///
    /// Tajik spells both forms identically in all four entries, so the branch
    /// is output-invisible; it is ported faithfully rather than folded away.
    fn pluralize(&self, n: &BigInt, forms: &[String]) -> Result<String> {
        let form = if n.is_one() { 0 } else { 1 };
        forms
            .get(form)
            .cloned()
            .ok_or_else(|| N2WError::Index("tuple index out of range".into()))
    }
}
