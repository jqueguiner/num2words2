//! Port of `lang_HI.py` (Hindi).
//!
//! Shape: **engine**. `Num2Word_HI` subclasses `Num2Word_Base` directly and
//! supplies `low_numwords` / `mid_numwords` / `high_numwords` + an overridden
//! `set_high_numwords` + `merge`, letting `Num2Word_Base.to_cardinal` drive
//! `splitnum`/`clean`. So `cards` / `maxval` / `merge` are all live here and
//! the default `to_cardinal` in `base.rs` does the work unchanged.
//!
//! Hindi uses the **Indian numbering system**: after सौ (100) the grouping
//! steps by two decimal places, not three — हज़ार 10^3, लाख 10^5, करोड़ 10^7,
//! अरब 10^9, खरब 10^11, … up to महागण 10^41 (PR #662 extended the ladder).
//! `MAXVAL` is `1000 * 10^41` = **10^44**, so `to_cardinal`/`to_ordinal` raise
//! `OverflowError` at 10^44 and above.
//!
//! Inherited from `Num2Word_Base` and deliberately left at the trait default:
//!   * `to_year(value) -> self.to_cardinal(value)` — HI does not override it,
//!     so years get no century treatment: `to_year(1999)` is just the plain
//!     cardinal "एक हज़ार नौ सौ निन्यानवे", and `to_year(-500)` is
//!     "माइनस पाँच सौ" (no "BC"-style suffix).
//!   * `is_title` stays `false`, so `title()` is the identity.
//!
//! # Faithfully reproduced Python quirks
//!
//! These all look wrong but are exactly what Python emits (each is pinned by a
//! row in the frozen corpus):
//!
//! 1. **`merge` drops the leading "एक" for सौ / लाख / करोड़ but not for
//!    हज़ार / अरब / ख़रब.** The `rnum in [100, 100000, 10000000]` list simply
//!    omits 10^3, 10^9 and 10^11. The result is a table that reads
//!    inconsistently: `to_cardinal(100)` == "सौ" and `to_cardinal(100000)` ==
//!    "लाख" (no "एक"), yet `to_cardinal(1000)` == "एक हज़ार" and
//!    `to_cardinal(10**9)` == "एक अरब" (with "एक"). It propagates into
//!    compounds too: `to_cardinal(123456)` == "लाख तेईस हज़ार चार सौ छप्पन",
//!    which is missing the "एक" a reader would expect. See [`LangHi::merge`].
//! 2. **`to_ordinal` never calls `verify_ordinal`.** `Num2Word_Base` defines
//!    `verify_ordinal` to reject negatives with a `TypeError`, but HI's
//!    override does not call it, so negative ordinals sail straight through:
//!    `to_ordinal(-1)` == "माइनस एकवाँ", `to_ordinal(-999)` ==
//!    "माइनस नौ सौ निन्यानवेवाँ". This is a plain cardinal with the ordinal
//!    suffix glued on — not a real Hindi ordinal.
//! 3. **`to_ordinal_num` raises `KeyError` on every negative.**
//!    `_convert_to_hindi_numerals` maps each character of `str(value)` through
//!    `_digits_to_hindi_digits`, which only holds "0".."9". The "-" of a
//!    negative is not a key, so `dict.__getitem__("-")` raises `KeyError: '-'`
//!    — e.g. `to_ordinal_num(-1)`. Modelled by [`convert_to_hindi_numerals`].
//! 4. **`to_ordinal_num` has no overflow ceiling**, because it never touches
//!    `to_cardinal`. `to_ordinal_num(10**15)` happily returns
//!    "१०००००००००००००००वाँ" while `to_cardinal(10**15)` and
//!    `to_ordinal(10**15)` both raise `OverflowError`. The asymmetry is real
//!    and corpus-pinned — do not add a bounds check here.
//! 5. The irregular-ordinal tables cover 0,1,2,3,4,6 but **skip 5**, so
//!    `to_ordinal(5)` falls through to the regular suffix rule and yields
//!    "पाँचवाँ" rather than a suppletive form.
//! 6. **`to_currency` emits a double space after the negword — but only for
//!    ints.** HI's integer branch builds `"%s %s %s" % (minus_str, money_str,
//!    currency_str)` where `minus_str` is the *raw* `negword` — "माइनस " with
//!    its trailing space already attached — so the format's own space lands on
//!    top of it: `to_currency(-1, "INR")` == "माइनस  एक रुपया", two spaces.
//!    The float half delegates to `Num2Word_Base`, which instead builds
//!    `"%s " % self.negword.strip()` and so emits **one**:
//!    `to_currency(-12.34, "INR")` == "माइनस बारह रुपये, चौंतीस पैसे". Base's
//!    own int branch would have agreed with the float one; HI's override is
//!    what splits them. The trailing `.strip()` cannot help — the extra space
//!    is interior. Only the single-space float form is corpus-pinned (there is
//!    no negative-int currency row), so this was read off the live interpreter.
//! 7. **The integer branch silently ignores `cents`, `separator` and
//!    `adjective`.** All three are accepted, then never read before the early
//!    return. `separator`/`cents` are genuinely meaningless without a cents
//!    segment, but `adjective` is a real drop: Base's int branch *does* apply
//!    `prefix_currency`. It happens to be unobservable for HI because
//!    `CURRENCY_ADJECTIVES` is empty, so the two agree by luck rather than by
//!    design.
//! 8. **The integer branch re-implements `pluralize` inline instead of calling
//!    it.** `abs_val == 1 → cr1[0]`, else `cr1[1]`. That is the same rule
//!    `Num2Word_HI.pluralize` encodes, so the duplication is currently
//!    harmless — but it means the float and int paths would drift if either
//!    were ever changed alone. Note the consequence at zero:
//!    `to_currency(0, "INR")` == "शून्य रुपये" (plural), because 0 != 1.

use crate::base::{set_low_numwords, set_mid_numwords, Cards, Lang, N2WError, Result};
use crate::currency::{default_to_currency, CurrencyForms, CurrencyValue};
use crate::floatpath::FloatValue;
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use std::collections::HashMap;

/// `_regular_ordinal_suffix`.
const REGULAR_ORDINAL_SUFFIX: &str = "वाँ";

/// `_irregular_ordinals`. Note 5 is absent — see module docs, quirk 5.
const IRREGULAR_ORDINALS: [(u8, &str); 6] = [
    (0, "शून्य"),
    (1, "पहला"),
    (2, "दूसरा"),
    (3, "तीसरा"),
    (4, "चौथा"),
    (6, "छठा"),
];

/// `_irregular_ordinals_nums`. Same keys as `_irregular_ordinals`.
const IRREGULAR_ORDINALS_NUMS: [(u8, &str); 6] = [
    (0, "०"),
    (1, "१ला"),
    (2, "२रा"),
    (3, "३रा"),
    (4, "४था"),
    (6, "६ठा"),
];

/// `_hindi_digits` = "०१२३४५६७८९", indexed by the ASCII digit's value.
///
/// Python builds `_digits_to_hindi_digits = dict(zip(string.digits,
/// _hindi_digits))`, i.e. "0"→"०" .. "9"→"९". A positional array is the same
/// map. Each Devanagari digit is one `char` (U+0966..U+096F).
const HINDI_DIGITS: [char; 10] = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'];

/// `high_numwords`: `(exponent, word)`, inserted as `cards[10**n] = word`.
///
/// The Indian system's two-place grouping above सौ lives here. PR
/// savoirfairelinux/num2words#662 extends the ladder from 10^11 up to 10^41
/// (महागण) and respells ख़रब → खरब (nukta dropped). Note the gap 37→41 (no
/// 10^39), matching the traditional Sanskrit scale. MAXVAL is now 10^44.
const HIGH_NUMWORDS: [(u32, &str); 19] = [
    (41, "महागण"),
    (37, "गण"),
    (35, "महाओम"),
    (33, "ओम"),
    (31, "महा अशोहिणी"),
    (29, "अशोहिणी"),
    (27, "महामध्या"),
    (25, "मध्या"),
    (23, "महाअंत्या"),
    (21, "अंत्या"),
    (19, "महाशंख"),
    (17, "शंख"),
    (15, "पद्म"),
    (13, "नील"),
    (11, "खरब"),
    (9, "अरब"),
    (7, "करोड़"),
    (5, "लाख"),
    (3, "हज़ार"),
];

/// `low_numwords`, mapping to 99 down to 0 via `set_low_numwords`.
///
/// Transcribed verbatim from the Python source (which carries `# alternative`
/// comments naming informal variants — those are comments only and never
/// reachable, so only the live forms appear here).
const LOW_NUMWORDS: [&str; 100] = [
    "निन्यानवे", "अट्ठानवे", "सत्तानवे", "छियानवे",
    "पचानवे", "चौरानवे", "तिरानवे", "बानवे",
    "इक्यानवे", "नब्बे", "नवासी", "अट्ठासी",
    "सतासी", "छियासी", "पचासी", "चौरासी",
    "तिरासी", "बयासी", "इक्यासी", "अस्सी",
    "उनासी", "अठहत्तर", "सतहत्तर", "छिहत्तर",
    "पचहत्तर", "चौहत्तर", "तिहत्तर", "बहत्तर",
    "इकहत्तर", "सत्तर", "उनहत्तर", "अड़सठ",
    "सड़सठ", "छियासठ", "पैंसठ", "चौंसठ",
    "तिरसठ", "बासठ", "इकसठ", "साठ",
    "उनसठ", "अट्ठावन", "सत्तावन", "छप्पन",
    "पचपन", "चौवन", "तिरेपन", "बावन",
    "इक्यावन", "पचास", "उनचास", "अड़तालीस",
    "सैंतालीस", "छियालीस", "पैंतालीस", "चौवालीस",
    "तैंतालीस", "बयालीस", "इकतालीस", "चालीस",
    "उनतालीस", "अड़तीस", "सैंतीस", "छत्तीस",
    "पैंतीस", "चौंतीस", "तैंतीस", "बत्तीस",
    "इकत्तीस", "तीस", "उनतीस", "अट्ठाईस",
    "सत्ताईस", "छब्बीस", "पच्चीस", "चौबीस",
    "तेईस", "बाईस", "इक्कीस", "बीस",
    "उन्नीस", "अट्ठारह", "सत्रह", "सोलह",
    "पंद्रह", "चौदह", "तेरह", "बारह",
    "ग्यारह", "दस", "नौ", "आठ",
    "सात", "छः", "पाँच", "चार",
    "तीन", "दो", "एक", "शून्य",
];

/// `Num2Word_HI.CURRENCY_FORMS`, verbatim — all three entries.
///
/// HI declares its **own** class-level `CURRENCY_FORMS`, so the `lang_EUR`
/// shared-dict trap does not apply here: `Num2Word_EN.__init__` mutates
/// `Num2Word_EUR.CURRENCY_FORMS` in place, but `Num2Word_HI` subclasses
/// `Num2Word_Base` directly (MRO: HI → Base → object) and shadows the
/// attribute outright. The live interpreter confirms exactly three codes
/// survive to runtime, so EN's ~24 extra codes (AUD/JPY/KWD/...) must **not**
/// be added — every one of them is a corpus-pinned NotImplementedError row.
///
/// Note USD and EUR carry two *identical* unit forms — `("डॉलर", "डॉलर")` and
/// `("यूरो", "यूरो")` — so their pluralization is a no-op. Only INR actually
/// inflects (रुपया/रुपये, पैसा/पैसे). The arity is kept at 2 regardless
/// because `pluralize` indexes into it.
fn build_currency_forms() -> HashMap<&'static str, CurrencyForms> {
    let mut m: HashMap<&'static str, CurrencyForms> = HashMap::new();
    m.insert("INR", CurrencyForms::new(&["रुपया", "रुपये"], &["पैसा", "पैसे"]));
    m.insert("USD", CurrencyForms::new(&["डॉलर", "डॉलर"], &["सेंट", "सेंट"]));
    m.insert("EUR", CurrencyForms::new(&["यूरो", "यूरो"], &["सेंट", "सेंट"]));
    m
}

/// Python's `_convert_to_hindi_numerals`.
///
/// ```python
/// return "".join(map(self._digits_to_hindi_digits.__getitem__, str(value)))
/// ```
///
/// `map` is lazy but `"".join` drains it left to right, so the **first**
/// non-digit character is the one that raises. For a negative that is the
/// leading "-", giving `KeyError: '-'` before any digit is converted. The
/// `Err` payload mirrors Python's `KeyError` repr, which quotes the key.
fn convert_to_hindi_numerals(value: &BigInt) -> Result<String> {
    let mut out = String::new();
    for ch in value.to_string().chars() {
        match ch.to_digit(10) {
            Some(d) => out.push(HINDI_DIGITS[d as usize]),
            // Only reachable for the "-" of a negative: BigInt's Display
            // emits nothing else outside 0-9.
            None => return Err(N2WError::Key(format!("'{}'", ch))),
        }
    }
    Ok(out)
}

/// Look a small key up in one of the irregular-ordinal tables.
///
/// Python does `value in self._irregular_ordinals`, an exact dict lookup on an
/// int key. Comparing against `BigInt::from(k)` reproduces that for arbitrarily
/// large / negative values without narrowing the input.
fn irregular_lookup(table: &[(u8, &'static str)], value: &BigInt) -> Option<&'static str> {
    table
        .iter()
        .find(|(k, _)| value == &BigInt::from(*k))
        .map(|(_, w)| *w)
}

pub struct LangHi {
    cards: Cards,
    maxval: BigInt,
    currency_forms: HashMap<&'static str, CurrencyForms>,
}

impl Default for LangHi {
    fn default() -> Self {
        Self::new()
    }
}

impl LangHi {
    pub fn new() -> Self {
        let mut cards = Cards::new();

        // HI's `set_high_numwords` ignores its argument and walks
        // `self.high_numwords`, setting `cards[10**n] = word`.
        for (n, word) in HIGH_NUMWORDS.iter() {
            cards.insert(BigInt::from(10u8).pow(*n), *word);
        }

        // `mid_numwords = [(100, "सौ")]`
        set_mid_numwords(&mut cards, &[(100, "सौ")]);

        // `set_low_numwords` zips the words against range(len-1, -1, -1),
        // so LOW_NUMWORDS[0] -> 99 and LOW_NUMWORDS[99] -> 0.
        set_low_numwords(&mut cards, &LOW_NUMWORDS);

        // `MAXVAL = 1000 * list(self.cards.keys())[0]`. Python's OrderedDict
        // preserves insertion order, and high-then-mid-then-low happens to be
        // strictly descending here (verified against the interpreter), so
        // `keys()[0]` is the largest card. After PR #662 the top card is
        // 10^41 (महागण), so MAXVAL is 10^44.
        let maxval = cards.highest().cloned().unwrap_or_else(BigInt::zero) * BigInt::from(1000);

        LangHi {
            cards,
            maxval,
            // Built once here, never per call: `to_currency` and `to_cheque`
            // only ever read this table, and rebuilding it on each call is what
            // made an earlier revision of this port slower than the Python it
            // replaces.
            currency_forms: build_currency_forms(),
        }
    }
}

impl Lang for LangHi {
    /// This language's own `to_currency(currency=...)` default,
    /// read from the live Python signature. Only 44 of 156 use EUR.
    fn default_currency(&self) -> &str {
        "INR"
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
        "माइनस "
    }

    fn pointword(&self) -> &str {
        "दशमलव"
    }

    /// Port of `Num2Word_HI.merge`.
    ///
    /// ```python
    /// if lnum == 1 and rnum in [100, 100000, 10000000]:
    ///     return rtext, rnum
    /// elif lnum == 1 and rnum < 100:
    ///     return rtext, rnum
    /// elif lnum >= 100 > rnum:
    ///     return "%s %s" % (ltext, rtext), lnum + rnum
    /// elif rnum > lnum:
    ///     return "%s %s" % (ltext, rtext), lnum * rnum
    /// return "%s %s" % (ltext, rtext), lnum + rnum
    /// ```
    ///
    /// The first arm is the "एक"-dropping quirk (module docs, quirk 1): the
    /// literal list holds सौ/लाख/करोड़ but *not* हज़ार/अरब/ख़रब, so 1000 and
    /// 10^9 keep their "एक" while 100 and 10^5 lose it.
    ///
    /// `lnum >= 100 > rnum` is a Python chained comparison, i.e.
    /// `lnum >= 100 and 100 > rnum` — both bounds test against the literal,
    /// which is why it is written out longhand below.
    fn merge(&self, l: (&str, &BigInt), r: (&str, &BigInt)) -> (String, BigInt) {
        let (ltext, lnum) = l;
        let (rtext, rnum) = r;
        let hundred = BigInt::from(100);

        // The `rnum in [...]` list, verbatim: सौ, लाख, करोड़ — no हज़ार.
        let drops_ek = rnum == &hundred
            || rnum == &BigInt::from(100_000u32)
            || rnum == &BigInt::from(10_000_000u32);

        if lnum.is_one() && drops_ek {
            (rtext.to_string(), rnum.clone())
        } else if lnum.is_one() && rnum < &hundred {
            (rtext.to_string(), rnum.clone())
        } else if lnum >= &hundred && &hundred > rnum {
            (format!("{} {}", ltext, rtext), lnum + rnum)
        } else if rnum > lnum {
            (format!("{} {}", ltext, rtext), lnum * rnum)
        } else {
            (format!("{} {}", ltext, rtext), lnum + rnum)
        }
    }

    /// Port of `Num2Word_HI.to_ordinal`.
    ///
    /// No `verify_ordinal` call — see module docs, quirk 2. Negatives produce
    /// "माइनस <cardinal>वाँ" rather than raising `TypeError`, and values at or
    /// above `MAXVAL` propagate the `OverflowError` from `to_cardinal`.
    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        if let Some(word) = irregular_lookup(&IRREGULAR_ORDINALS, value) {
            return Ok(word.to_string());
        }
        let cardinal = self.to_cardinal(value)?;
        Ok(format!("{}{}", cardinal, REGULAR_ORDINAL_SUFFIX))
    }

    /// Port of `Num2Word_HI.to_ordinal_num`.
    ///
    /// Deliberately never calls `to_cardinal`, so there is **no** overflow
    /// check (module docs, quirk 4) — and negatives raise `KeyError` from the
    /// digit map rather than being rejected up front (quirk 3).
    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        if let Some(word) = irregular_lookup(&IRREGULAR_ORDINALS_NUMS, value) {
            return Ok(word.to_string());
        }
        Ok(format!(
            "{}{}",
            convert_to_hindi_numerals(value)?,
            REGULAR_ORDINAL_SUFFIX
        ))
    }

    /// `to_ordinal(float/Decimal)`.
    ///
    /// Python's `value in self._irregular_ordinals` is a *numeric* dict
    /// lookup, so a whole float hits the same irregular entry as its int
    /// (`1.0` → "पहला", `-0.0` → "शून्य"). Everything else is
    /// `self.to_cardinal(value) + "वाँ"`, where HI's cardinal is the *base
    /// engine's* — whole values take the int path (`5.0` → "पाँचवाँ",
    /// `-3.0` → "माइनस तीनवाँ") and fractional values the base float grammar
    /// (`0.5` → "शून्य दशमलव पाँचवाँ"). A whole value at or above `MAXVAL`
    /// propagates the cardinal's OverflowError, exactly as in Python.
    fn ordinal_float_entry(&self, value: &FloatValue) -> Result<String> {
        if let Some(i) = value.as_whole_int() {
            // Whole values reduce to the integer path verbatim — irregular
            // table, cardinal words and overflow behaviour all included.
            return self.to_ordinal(&i);
        }
        Ok(format!(
            "{}{}",
            self.cardinal_float_entry(value, None)?,
            REGULAR_ORDINAL_SUFFIX
        ))
    }

    /// `to_ordinal_num(float/Decimal)`.
    ///
    /// Same numeric dict lookup for the irregulars (`0.0`/`-0.0` → "०",
    /// `1.0` → "१ला"), then `_convert_to_hindi_numerals(value)` maps every
    /// character of `str(value)` through the Devanagari digit table — and
    /// raises **KeyError** on the first non-digit, which for any non-irregular
    /// float repr is the "." (or the "-"/"e"/"E" before it): `5.0` →
    /// KeyError('.'), `-1.0` → KeyError('-'), `Decimal("1E+2")` →
    /// KeyError('E'). Only point-free whole Decimals survive:
    /// `Decimal("100")` → "१००वाँ".
    fn ordinal_num_float_entry(&self, value: &FloatValue, repr_str: &str) -> Result<String> {
        if let Some(i) = value.as_whole_int() {
            if let Some(word) = irregular_lookup(&IRREGULAR_ORDINALS_NUMS, &i) {
                return Ok(word.to_string());
            }
        }
        // "".join(map(digit_table.__getitem__, str(value))) — first miss raises.
        let mut out = String::new();
        for ch in repr_str.chars() {
            match ch.to_digit(10) {
                Some(d) => out.push(HINDI_DIGITS[d as usize]),
                None => return Err(N2WError::Key(format!("'{}'", ch))),
            }
        }
        Ok(format!("{}{}", out, REGULAR_ORDINAL_SUFFIX))
    }

    // `to_year` is intentionally not overridden: `Num2Word_Base.to_year`
    // simply delegates to `to_cardinal`, which the trait default already does.

    // ---- currency -------------------------------------------------------
    //
    // HI overrides only `to_currency` (and only its integer half) plus
    // `pluralize`. `to_cheque`, `_money_verbose`, `_cents_verbose` and
    // `_cents_terse` all come straight from `Num2Word_Base`, so the trait
    // defaults already mirror them exactly.
    //
    // `currency_adjective` is deliberately NOT overridden: HI never defines
    // `CURRENCY_ADJECTIVES`, and nothing mutates Base's empty class dict in
    // place (EN *rebinds* its own on the instance), so the live interpreter
    // still reports `{}`. Every code therefore misses the `adjective` prefix
    // and the kwarg is inert — see quirk 7.
    //
    // `currency_precision` is likewise NOT overridden: HI never defines
    // `CURRENCY_PRECISION` either, so `.get(code, 100)` is 100 for *every*
    // code. HI has no 3-decimal or 0-decimal currency — KWD/BHD/JPY are not in
    // its table at all and raise NotImplementedError — which makes both
    // `default_to_currency`'s `divisor == 1` branch and `_cents_terse`'s
    // 3-digit width unreachable for Hindi.

    fn lang_name(&self) -> &str {
        "Num2Word_HI"
    }

    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.currency_forms.get(code)
    }

    /// Port of `Num2Word_HI.pluralize`.
    ///
    /// ```python
    /// if count == 1:
    ///     return forms[0]
    /// return forms[1] if len(forms) > 1 else forms[0]
    /// ```
    ///
    /// Unlike `Num2Word_EUR.pluralize` (a bare `forms[0 if n == 1 else 1]`),
    /// HI's guards the second index, so a one-form entry degrades to `forms[0]`
    /// instead of raising IndexError. `forms[0]` on an *empty* tuple would
    /// still raise; every HI entry has two forms, so that stays unreachable —
    /// mapped to `Index` rather than panicking so the exception type survives
    /// if the table ever changes.
    ///
    /// Reached only from the float path: HI's own `to_currency` integer branch
    /// inlines an equivalent rule instead of calling this (quirk 8).
    fn pluralize(&self, n: &BigInt, forms: &[String]) -> Result<String> {
        if n.is_one() {
            return forms
                .first()
                .cloned()
                .ok_or_else(|| N2WError::Index("tuple index out of range".into()));
        }
        forms
            .get(1)
            .or_else(|| forms.first())
            .cloned()
            .ok_or_else(|| N2WError::Index("tuple index out of range".into()))
    }

    /// Port of `Num2Word_HI.to_currency`.
    ///
    /// Only the `isinstance(val, int)` branch is HI's own; floats hand off to
    /// `super()`, i.e. `Num2Word_Base.to_currency`. The two halves disagree in
    /// ways that look like oversights and are ported verbatim — see quirks 6-8
    /// in the module docs.
    fn to_currency(
        &self,
        val: &CurrencyValue,
        currency: &str,
        cents: bool,
        separator: Option<&str>,
        adjective: bool,
    ) -> Result<String> {
        let separator = separator.unwrap_or(self.default_separator());

        if let CurrencyValue::Int(v) = val {
            // Python catches `(KeyError, AttributeError)` around the forms
            // lookup and hands the whole call to `super()`, which repeats the
            // lookup and turns the KeyError into NotImplementedError. Delegating
            // reproduces that rather than raising here, so the message and its
            // wording keep coming from one place. (The AttributeError arm is
            // dead: `CURRENCY_FORMS` always exists on the class.)
            let forms = match self.currency_forms.get(currency) {
                Some(f) => f,
                None => {
                    return default_to_currency(self, val, currency, cents, separator, adjective)
                }
            };

            // `minus_str = self.negword if val < 0 else ""` — HI takes the raw
            // negword with its trailing space *intact*, where Base uses
            // `"%s " % self.negword.strip()`. Combined with the format string
            // below this is quirk 6: the double space.
            let minus_str = if v.is_negative() { self.negword() } else { "" };
            let abs_val = v.abs();
            // Bypasses `_money_verbose` and calls `to_cardinal` directly.
            // Identical for HI, which overrides neither.
            let money_str = self.to_cardinal(&abs_val)?;

            // `cr1[0]` when abs_val == 1, else `cr1[1] if len(cr1) > 1 else cr1[0]`.
            let unit = &forms.unit;
            let currency_str = if abs_val.is_one() {
                unit.first()
            } else {
                unit.get(1).or_else(|| unit.first())
            }
            .ok_or_else(|| N2WError::Index("tuple index out of range".into()))?;

            // Python: `("%s %s %s" % (minus_str, money_str, currency_str)).strip()`
            // — note the space *between* the first two placeholders, which Base's
            // `"%s%s %s"` does not have. That is the whole of quirk 6.
            return Ok(format!("{} {} {}", minus_str, money_str, currency_str)
                .trim()
                .to_string());
        }

        default_to_currency(self, val, currency, cents, separator, adjective)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use bigdecimal::BigDecimal;
    use std::str::FromStr;

    /// A currency call shaped like the binding's: `separator: None` means the
    /// kwarg was omitted, so `default_separator()` (",") applies. `arg` is the
    /// corpus's `repr(value)`, and the int/float split is read off it exactly
    /// as the Python shim does.
    fn cur(arg: &str, code: &str) -> Result<String> {
        let is_int = !arg.contains('.');
        let v = CurrencyValue::parse(arg, is_int, !is_int, !is_int).unwrap();
        LangHi::new().to_currency(&v, code, true, None, false)
    }

    fn cheque(arg: &str, code: &str) -> Result<String> {
        LangHi::new().to_cheque(&BigDecimal::from_str(arg).unwrap(), code)
    }

    /// The three codes HI actually implements. Every `"lang": "hi",
    /// "to": "currency:{INR,USD,EUR}"` row in `bench/corpus.jsonl`.
    ///
    /// `unit1`/`unit2` differ only for INR — USD and EUR carry two identical
    /// forms — which is what makes INR the row that proves `pluralize` is
    /// wired at all.
    #[test]
    fn corpus_currency_implemented() {
        for (code, unit1, unit2, sub1, sub2) in [
            ("INR", "रुपया", "रुपये", "पैसा", "पैसे"),
            ("USD", "डॉलर", "डॉलर", "सेंट", "सेंट"),
            ("EUR", "यूरो", "यूरो", "सेंट", "सेंट"),
        ] {
            // Ints: no cents segment at all. 0 takes the *plural* (quirk 8).
            assert_eq!(cur("0", code).unwrap(), format!("शून्य {unit2}"));
            assert_eq!(cur("1", code).unwrap(), format!("एक {unit1}"));
            assert_eq!(cur("2", code).unwrap(), format!("दो {unit2}"));
            // "सौ", not "एक सौ" — merge drops the एक for 100 (quirk 1).
            assert_eq!(cur("100", code).unwrap(), format!("सौ {unit2}"));
            assert_eq!(cur("1000000", code).unwrap(), format!("दस लाख {unit2}"));

            // Floats: Base's path, so the cents segment appears.
            assert_eq!(cur("12.34", code).unwrap(), format!("बारह {unit2}, चौंतीस {sub2}"));
            assert_eq!(cur("0.01", code).unwrap(), format!("शून्य {unit2}, एक {sub1}"));
            // 1.0 is a float, so cents still print — the has_decimal guard.
            assert_eq!(cur("1.0", code).unwrap(), format!("एक {unit1}, शून्य {sub2}"));
            assert_eq!(
                cur("99.99", code).unwrap(),
                format!("निन्यानवे {unit2}, निन्यानवे {sub2}")
            );
            assert_eq!(
                cur("1234.56", code).unwrap(),
                format!("एक हज़ार दो सौ चौंतीस {unit2}, छप्पन {sub2}")
            );
            // Single space after the negword — the float half uses Base's
            // `negword.strip()` (quirk 6).
            assert_eq!(
                cur("-12.34", code).unwrap(),
                format!("माइनस बारह {unit2}, चौंतीस {sub2}")
            );
            assert_eq!(cur("0.5", code).unwrap(), format!("शून्य {unit2}, पचास {sub2}"));
        }
    }

    /// The six codes HI does *not* implement — every remaining currency row.
    ///
    /// JPY/KWD/BHD are the load-bearing ones: HI declares its own
    /// `CURRENCY_FORMS`, so it never sees the ~24 codes `Num2Word_EN.__init__`
    /// mutates into `Num2Word_EUR`'s shared dict. Adding a 0-decimal JPY or a
    /// 3-decimal KWD here would turn 36 expected raises into wrong output.
    #[test]
    fn corpus_currency_not_implemented() {
        for code in ["GBP", "JPY", "KWD", "BHD", "CNY", "CHF"] {
            for arg in [
                "0", "1", "2", "100", "12.34", "0.01", "1.0", "99.99", "1234.56", "-12.34",
                "1000000", "0.5",
            ] {
                match cur(arg, code) {
                    Err(N2WError::NotImplemented(m)) => assert_eq!(
                        m,
                        format!("Currency code \"{code}\" not implemented for \"Num2Word_HI\"")
                    ),
                    other => panic!("{code} {arg}: expected NotImplementedError, got {other:?}"),
                }
            }
        }
    }

    /// Every `"lang": "hi", "to": "cheque:*"` row.
    ///
    /// `to_cheque` is Base's, unmodified. It always takes the *last* unit form
    /// (`cr1[-1]`), so INR cheques read रुपये even at 1. `.upper()` is a no-op
    /// on Devanagari — only the literal "AND" is uppercase.
    #[test]
    fn corpus_cheque() {
        assert_eq!(
            cheque("1234.56", "INR").unwrap(),
            "एक हज़ार दो सौ चौंतीस AND 56/100 रुपये"
        );
        assert_eq!(
            cheque("1234.56", "USD").unwrap(),
            "एक हज़ार दो सौ चौंतीस AND 56/100 डॉलर"
        );
        assert_eq!(
            cheque("1234.56", "EUR").unwrap(),
            "एक हज़ार दो सौ चौंतीस AND 56/100 यूरो"
        );
        for code in ["GBP", "JPY", "KWD", "BHD", "CNY", "CHF"] {
            match cheque("1234.56", code) {
                Err(N2WError::NotImplemented(m)) => assert_eq!(
                    m,
                    format!("Currency code \"{code}\" not implemented for \"Num2Word_HI\"")
                ),
                other => panic!("{code}: expected NotImplementedError, got {other:?}"),
            }
        }
    }

    /// Off-corpus checks against the live interpreter, covering the paths the
    /// corpus leaves untested. Every expectation here was read out of Python.
    #[test]
    fn quirks_match_python() {
        // Quirk 6: negative *ints* get two spaces, negative floats one.
        assert_eq!(cur("-1", "INR").unwrap(), "माइनस  एक रुपया");
        assert_eq!(cur("-2", "INR").unwrap(), "माइनस  दो रुपये");
        assert_eq!(cur("-100", "INR").unwrap(), "माइनस  सौ रुपये");
        assert_eq!(cur("-12", "INR").unwrap(), "माइनस  बारह रुपये");

        // The has_decimal guard: Decimal("5") prints no paise, Decimal("5.00")
        // does, though the two are numerically equal.
        let plain = CurrencyValue::Decimal {
            value: BigDecimal::from_str("5").unwrap(),
            has_decimal: false,
            is_float: false,
        };
        assert_eq!(
            LangHi::new().to_currency(&plain, "INR", true, None, false).unwrap(),
            "पाँच रुपये"
        );
        let scaled = CurrencyValue::Decimal {
            value: BigDecimal::from_str("5.00").unwrap(),
            has_decimal: true,
            is_float: false,
        };
        assert_eq!(
            LangHi::new().to_currency(&scaled, "INR", true, None, false).unwrap(),
            "पाँच रुपये, शून्य पैसे"
        );

        // cents=False takes the terse branch, zero-padded to 2 (divisor 100).
        let v = CurrencyValue::parse("12.34", false, true, true).unwrap();
        assert_eq!(
            LangHi::new().to_currency(&v, "INR", false, None, false).unwrap(),
            "बारह रुपये, 34 पैसे"
        );
        let v = CurrencyValue::parse("12.04", false, true, true).unwrap();
        assert_eq!(
            LangHi::new().to_currency(&v, "INR", false, None, false).unwrap(),
            "बारह रुपये, 04 पैसे"
        );
        // ...but the int branch ignores `cents` entirely (quirk 7).
        let v = CurrencyValue::parse("2", true, false, false).unwrap();
        assert_eq!(
            LangHi::new().to_currency(&v, "INR", false, None, false).unwrap(),
            "दो रुपये"
        );

        // An explicit separator replaces the "," default on the float path,
        // and is ignored on the int path (quirk 7).
        let v = CurrencyValue::parse("12.34", false, true, true).unwrap();
        assert_eq!(
            LangHi::new().to_currency(&v, "INR", true, Some(" और"), false).unwrap(),
            "बारह रुपये और चौंतीस पैसे"
        );
        let v = CurrencyValue::parse("2", true, false, false).unwrap();
        assert_eq!(
            LangHi::new().to_currency(&v, "INR", true, Some(" और"), false).unwrap(),
            "दो रुपये"
        );

        // `adjective` is inert: CURRENCY_ADJECTIVES is empty (quirk 7).
        let v = CurrencyValue::parse("12.34", false, true, true).unwrap();
        assert_eq!(
            LangHi::new().to_currency(&v, "INR", true, None, true).unwrap(),
            "बारह रुपये, चौंतीस पैसे"
        );

        // PR #662 extended the ladder to महागण (10^41), so MAXVAL is 10^44;
        // to_currency inherits that ceiling via to_cardinal. 10^13 is नील.
        assert_eq!(cur("10000000000000", "INR").unwrap(), "एक नील रुपये");
        assert!(matches!(
            cur("100000000000000000000000000000000000000000000", "INR"),
            Err(N2WError::Overflow(_))
        ));
    }

    /// The fractional-cents branch — `(value * 100) % 1 != 0`, so `right` stays
    /// a Decimal and Base renders it through the *float* path
    /// (`self.to_cardinal(float(right))`), picking up HI's pointword दशमलव.
    ///
    /// No corpus row reaches this, and the subunit word is taken as `cr2[1]`
    /// unconditionally rather than via `pluralize` — hence "एक दशमलव एक पैसे"
    /// (plural) at 1.011. Expectations read off the live interpreter.
    #[test]
    fn fractional_cents_match_python() {
        assert_eq!(cur("2.675", "INR").unwrap(), "दो रुपये, सड़सठ दशमलव पाँच पैसे");
        assert_eq!(cur("1.005", "INR").unwrap(), "एक रुपया, शून्य दशमलव पाँच पैसे");
        assert_eq!(cur("12.999", "INR").unwrap(), "बारह रुपये, निन्यानवे दशमलव नौ पैसे");
        assert_eq!(cur("1.011", "INR").unwrap(), "एक रुपया, एक दशमलव एक पैसे");
        assert_eq!(cur("0.001", "INR").unwrap(), "शून्य रुपये, शून्य दशमलव एक पैसे");
        assert_eq!(
            cur("-0.001", "INR").unwrap(),
            "माइनस शून्य रुपये, शून्य दशमलव एक पैसे"
        );
    }
}
