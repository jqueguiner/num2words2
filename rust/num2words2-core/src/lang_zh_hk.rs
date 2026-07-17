//! Port of `lang_ZH_HK.py` (Chinese, Hong Kong / Traditional).
//!
//! Registry check: `__init__.py` maps `"zh_HK"` → `lang_ZH_HK.Num2Word_ZH_HK()`,
//! so this file ports that class. `Num2Word_ZH_HK` defines no methods at all:
//! its `__init__` only rebuilds `CURRENCY_FLOATS` (毫/仙), merges five extra
//! `CURRENCY_FORMS` codes, and appends two `CAP_map` rows (毫→角, 仙→分) —
//! every behaviour is inherited from `Num2Word_ZH`. So `to_cardinal` /
//! `to_ordinal` / `to_ordinal_num` / `to_year` are byte-identical to `zh_TW`
//! (and differ from `zh_CN` only by the simplified/traditional numword tables
//! that `Num2Word_ZH_CN` substitutes), while all three of the child's data
//! tweaks land on the currency surface.
//!
//! The one `CAP_map` consumer is `zh_to_cap`'s `capital` branch, reachable
//! only through `reading="capital"` — i.e. through the `*_kw` hooks. The
//! runtime table (parent rows + the child's 毫→角/仙→分) is [`HK_CAP_MAP`].
//!
//! # Currency: ZH replaces the machinery, it does not configure it
//!
//! Most languages inherit `Num2Word_Base.to_currency` and supply data. ZH
//! overrides `to_currency` wholesale with a different algorithm, so almost
//! none of the Base contract applies here:
//!
//! * `CURRENCY_FORMS` values are **bare strings** ("歐羅"), not the
//!   `(singular, plural)` tuples every other language carries. There are no
//!   plural forms to choose between, so `pluralize` is never called and stays
//!   at the trait default that raises — exactly as `Num2Word_Base.pluralize`
//!   does.
//! * The subunit names are **not** per currency: they come from
//!   `CURRENCY_FLOATS`, a flat 2-element list (毫 = 1/10, 仙 = 1/100), so
//!   there is no subunit half of a `CURRENCY_FORMS` entry to store.
//! * `CURRENCY_ADJECTIVES` and `CURRENCY_PRECISION` are both empty
//!   (`# CURRENCY_ADJECTIVES are not implemented` in the source), so
//!   `currency_adjective` and `currency_precision` keep their trait defaults
//!   (`None` / 100).
//! * `cents=`, `separator=` and `adjective=` are accepted by ZH's signature
//!   and then never read — the output is a bare concatenation with no
//!   separator anywhere.
//! * `_money_verbose` / `_cents_verbose` / `_cents_terse` are never reached:
//!   the integer part goes through `to_cardinal` directly and the subunits
//!   through ZH's own `to_currency_float`.
//!
//! `to_cheque`, by contrast, is **not** overridden by ZH, so Base's runs — and
//! Base's assumes the tuple shape that ZH does not have. That mismatch is
//! bug #7 below, and it is the whole story of this file's `to_cheque`.
//!
//! # The `lang_EUR.py` mutation trap does not apply here
//!
//! `Num2Word_EN.__init__` mutates `Num2Word_EUR.CURRENCY_FORMS` in place, so
//! 16 classes read an EN-rewritten table at runtime. `Num2Word_ZH` is not one
//! of them: it subclasses `Num2Word_Base` directly and shadows the inherited
//! `{}` with its own class-body dict, which is a different object from the one
//! EN mutates. Verified against the live interpreter — `Num2Word_ZH_HK()`
//! reports `EUR → 歐羅`, not `("euro", "euros")`.
//!
//! `Num2Word_ZH_HK.__init__` likewise leaks nothing back: it does
//! `self.CURRENCY_FORMS = self.CURRENCY_FORMS.copy()` (and the same for
//! `CAP_map`) *before* mutating, so the copies are instance attributes and
//! `Num2Word_ZH.CURRENCY_FORMS["EUR"]` stays 歐元 for `zh`/`zh_TW`. The tables
//! below are therefore per-instance state modelled as per-struct state, which
//! is what they already are in Python.
//!
//! Shape: **engine**. `Num2Word_ZH` defines `high_numwords`/`mid_numwords`/
//! `low_numwords` + `set_high_numwords` + `merge`, so `Num2Word_Base` builds
//! `self.cards`/`MAXVAL` and drives `splitnum`/`clean`. `to_cardinal` is only
//! *wrapped*, not replaced: it delegates to `super().to_cardinal` and then
//! post-processes. So `cards`/`maxval`/`merge` are all live here and
//! `base::default_to_cardinal` does the real work.
//!
//! # The `reading` / `prefer` axis
//!
//! `Num2Word_ZH` threads a `reading` and a `prefer` argument through every
//! public method, and `select_text` uses them to choose between alternative
//! glyphs. Exactly one card is polymorphic: `low_numwords[-1]` is the tuple
//! `("零", "〇")`, so `cards[0]` is a *tuple*, not a string.
//!
//! The plain (no-kwargs) entry points are always entered at the defaults
//! (`reading=False`, `prefer=None`), and `select_text` under those defaults
//! reduces to "take `text[0]`":
//!
//!   * `all(isinstance(item, tuple) for item in ("零","〇"))` is **False**
//!     (the items are `str`), so the `reading is True` branch is dead;
//!   * `set(text) & set(self.prefer or set())` is empty, so `len(common) == 1`
//!     is False and it falls through to `text = text[0]`.
//!
//! The same holds for `year_prefix = ("公元", "西元")` → "公元". So the plain
//! paths store the already-selected first element ("零", "公元") and skip
//! `select_text`. Note `reading=True` never changes ZH_HK output at all —
//! no table entry is a tuple-of-tuples, so the `text[1]` branch is dead for
//! *every* reading value except `"capital"`.
//!
//! The `*_kw` hooks at the bottom of the `Lang` impl carry the live kwargs:
//! `reading="capital"` activates `zh_to_cap`'s [`HK_CAP_MAP`] arm (and the
//! 公元 prefix on positive years, and the currency path's 整 cheque suffix),
//! `prefer` re-selects the 零/〇 card and the 公元/西元 prefix, `stuff_zero`
//! parameterizes `merge`, and `counter` suffixes the ordinal forms.
//!
//! # Faithfully reproduced Python bugs / oddities
//!
//! 1. **`zh_to_cap`'s leading-一 strip is prefix-anchored, so it misses
//!    negatives.** With `capital` false, `zh_to_cap` does
//!    `elif out.startswith(one + ten): out = out[len(one):]` — i.e. it only
//!    strips the redundant 一 when the string *starts* with "一十". A negative
//!    teen starts with the negword 負, so the strip never fires:
//!    `to_cardinal(12)` == "十二" but `to_cardinal(-12)` == "負一十二", not the
//!    expected "負十二". Confirmed by the frozen corpus via the float path
//!    (`-12.34` → "負一十二點三四" vs `12.34` → "十二點三四"). Reproduced in
//!    [`LangZhHk::zh_to_cap_plain`] — do not "fix" it.
//! 2. **The strip is unconditional on position, not on grammar.** Any result
//!    that merely begins "一十…" loses its 一, which is what makes
//!    `to_cardinal(100000)` == "十萬" (from "一十萬") and
//!    `to_cardinal(1000000000)` == "十億" (from "一十億"). Interior "一十"
//!    survives: `to_cardinal(1010)` == "一千零一十".
//! 3. **`to_ordinal_num` skips `verify_ordinal`.** `to_ordinal` calls it (so
//!    negatives raise `TypeError`), but `to_ordinal_num` just interpolates
//!    the raw value: `to_ordinal_num(-1)` == "第-1". Corpus confirms.
//! 4. **`to_year` never bounds-checks.** It bypasses `to_cardinal` entirely
//!    and spells digits one by one, so it has no `MAXVAL` guard and cannot
//!    overflow — `to_year(10**100)` is fine while `to_cardinal(10**100)`
//!    raises `OverflowError`. No overflow check is added here.
//! 5. **`merge`'s dead `stuff_zero` fallthrough.** The `if len(str(lnum)) -
//!    len(str(rnum)) > 1:` block has arms for `stuff_zero` 1/2/3 and no
//!    `else`, so an out-of-range `stuff_zero` would fall past the whole
//!    `if/elif` chain to the trailing `return no_zero`. Unreachable at the
//!    fixed default of 2; noted rather than modelled.
//! 6. **`merge`'s `stuff_zero == 2` arm re-tests its own guard.** The inner
//!    `if len(str(lnum)) - len(str(rnum)) > 1 and ...` repeats a condition the
//!    outer `if` already proved. Harmless; kept as a comment, not as code.
//! 7. **`to_cheque` unpacks a string as if it were a tuple, and is broken for
//!    15 of ZH_HK's 17 currency codes.** See [`LangZhHk::to_cheque`] — the
//!    single largest quirk in this file.
//! 8. **`to_currency` ignores `has_decimal`, so `1.999` prints no cents.**
//!    Base gates the cents segment on `isinstance(val, float) or "." in
//!    str(val)`; ZH's source says `# has_decimal is not implemented` and gates
//!    on nothing at all, emitting subunits iff the rounded subunit count is
//!    non-zero. So `1.0` → "一元" (agreeing with Base by accident, since Base
//!    would print "one euro, zero cents"-style output) and `1.999` → "二元",
//!    a float input that renders as a bare integer. Corpus pins the `1.0` row.
//! 9. **`to_currency`'s `zh_to_cap` pass over each component is dead code.**
//!    The loop applies `zh_to_cap` to every fragment, but `money_str` has
//!    already been through it inside `to_cardinal` (and its leading-一 strip is
//!    idempotent — the result can never start "一十" again), and no other
//!    fragment is longer than one character. Ported literally anyway, since
//!    the cost is nil and the equivalence is an argument rather than a fact.
//!
//! # Cross-call mutable state (see `concerns`)
//!
//! `Num2Word_ZH` is stateful: `to_cardinal` assigns `self.stuff_zero`, and
//! `set_str_selection` assigns `self.reading` / `self.prefer` / `self.capital`.
//! `merge` then reads `self.stuff_zero`, and `zh_to_cap` / `to_cardinal_float`
//! read `self.capital`. For the four in-scope modes this is *self-consistent*
//! — every entry point assigns before anything reads, and none of them leaves
//! state that changes a later call's result — so the stateless Rust port is
//! faithful. The handshake is real but benign here.

use crate::base::{
    default_to_cardinal, set_low_numwords, set_mid_numwords, Cards, Kwargs, KwVal, Lang, N2WError,
    Result,
};
use crate::currency::{parse_currency_parts, CurrencyForms, CurrencyValue};
use crate::floatpath::{default_to_cardinal_float, FloatValue};
use bigdecimal::BigDecimal;
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};
use std::collections::HashMap;

/// `to_cardinal`'s `stuff_zero` default.
///
/// Python signature: `to_cardinal(self, value, stuff_zero=2, reading=False,
/// prefer=None)`. Nothing in the four in-scope modes passes `stuff_zero`
/// (`to_ordinal` forwards only `reading`/`prefer`), so `merge` always sees 2:
/// "零 between discontinuous *high* numbers only". 1 = always insert 零,
/// 3 = never. Only the value-2 arm is modelled below.
const STUFF_ZERO: u8 = 2;

/// `low_numwords[-1]` after `select_text` at `reading=False`/`prefer=None`.
/// Python holds the tuple `("零", "〇")` here; the default selection is `[0]`.
const ZERO_WORD: &str = "零";

/// `cards[1]` — the 一 that `zh_to_cap` strips off a leading "一十".
const ONE_WORD: &str = "一";
/// `cards[10]`.
const TEN_WORD: &str = "十";

/// `Num2Word_ZH_HK.CURRENCY_FLOATS_CHILD` — the subunit names, indexed by
/// `to_currency_float` as `[0]` (the 1/10 place) and `[1]` (the 1/100 place).
///
/// `__init__` does `self.CURRENCY_FLOATS = self.CURRENCY_FLOATS_CHILD.copy()`,
/// an assignment rather than a merge, so this **replaces** `Num2Word_ZH`'s
/// mainland 角/分 outright. 毫 and 仙 are the Hong Kong names (仙 transliterates
/// English "cent"), which is why 12.34 HKD reads 十二元三毫四仙 here but
/// 十二元三角四分 in `zh`.
const CURRENCY_FLOATS: [&str; 2] = ["毫", "仙"];

/// `CURRENCY_FORMS[code]` for a language whose values are bare strings.
///
/// [`CurrencyForms`] models Python's usual `(unit_forms, subunit_forms)` pair,
/// which ZH simply does not have (see the module docs). The whole Python string
/// goes in as the single `unit` entry and `subunit` is left empty — the shape
/// is inert here because both consumers of the table, `to_currency` and
/// `to_cheque`, are overridden below and read the string through
/// [`LangZhHk::currency_string`] instead. Nothing reaches
/// `currency::default_to_currency`, whose `pluralize`/`cr2` assumptions this
/// entry would not satisfy.
fn bare(s: &str) -> CurrencyForms {
    CurrencyForms::new(&[s], &[])
}

/// `CURRENCY_FORMS` as `Num2Word_ZH_HK` actually sees it at runtime.
///
/// Built in two steps on purpose, mirroring `__init__`: `Num2Word_ZH`'s
/// class-body dict first, then the `CURRENCY_FORMS_CHILD` codes written on
/// top. Pre-merging them would hide which entries are HK's own, and that
/// five-row diff is exactly what a reviewer checks against `lang_ZH_HK.py`.
/// Both halves are verified against a live `Num2Word_ZH_HK()`.
fn build_currency_forms() -> HashMap<&'static str, CurrencyForms> {
    let mut m: HashMap<&'static str, CurrencyForms> = HashMap::new();

    // ---- Num2Word_ZH.CURRENCY_FORMS (class body), inherited ----
    m.insert("XXX", bare("元")); // Generic dollar
    m.insert("CNY", bare("人民幣"));
    m.insert("NTD", bare("新台幣"));
    m.insert("HKD", bare("港幣"));
    m.insert("MOP", bare("澳門幣"));
    m.insert("SGD", bare("新加坡元"));
    m.insert("MYR", bare("馬來西亞令吉"));
    m.insert("USD", bare("美元"));
    m.insert("EUR", bare("歐元"));
    m.insert("GBP", bare("英鎊"));
    m.insert("JPY", bare("日元"));
    m.insert("CHF", bare("瑞士法郎"));
    m.insert("CAD", bare("加元"));
    m.insert("AUD", bare("澳幣"));
    m.insert("NZD", bare("紐西蘭元"));
    m.insert("THB", bare("泰銖"));
    m.insert("KRW", bare("韓元"));

    // ---- Num2Word_ZH_HK.CURRENCY_FORMS_CHILD, merged on top ----
    //     for k, v in self.CURRENCY_FORMS_CHILD.items():
    //         self.CURRENCY_FORMS[k] = v
    // Hong Kong / Taiwan names for five codes. Note CAD restates the parent's
    // 加元 unchanged — a no-op write that the source performs anyway, kept here
    // so the five-row child table matches `lang_ZH_HK.py` line for line.
    m.insert("EUR", bare("歐羅")); // was 歐元
    m.insert("JPY", bare("日圓")); // was 日元
    m.insert("CAD", bare("加元")); // was 加元 — unchanged
    m.insert("AUD", bare("澳元")); // was 澳幣
    m.insert("KRW", bare("韓圜")); // was 韓元

    m
}

pub struct LangZhHk {
    cards: Cards,
    maxval: BigInt,
    currency_forms: HashMap<&'static str, CurrencyForms>,
}

impl Default for LangZhHk {
    fn default() -> Self {
        Self::new()
    }
}

impl LangZhHk {
    pub fn new() -> Self {
        // Num2Word_ZH.setup(): declared low → high, then reversed in place.
        let mut high: Vec<&str> = vec![
            "萬",       // 10 ** 4
            "億",       // 10 ** 8
            "兆",       // 10 ** 12
            "京",       // 10 ** 16
            "垓",       // 10 ** 20
            "秭",       // 10 ** 24
            "穣",       // 10 ** 28
            "溝",       // 10 ** 32
            "澗",       // 10 ** 36
            "正",       // 10 ** 40
            "載",       // 10 ** 44
            "極",       // 10 ** 48
            "恆河沙",   // 10 ** 52
            "阿僧祇",   // 10 ** 56
            "那由他",   // 10 ** 60
            "不可思議", // 10 ** 64
            "無量",     // 10 ** 68
            "不可說",   // 10 ** 72
        ];
        high.reverse();

        let mut cards = Cards::new();

        // Num2Word_ZH.set_high_numwords:
        //     max = 4 * len(high)
        //     for word, n in zip(high, range(max, 0, -4)):
        //         self.cards[10 ** n] = word
        // zip() stops at the shorter sequence; here both are exactly len(high)
        // long (max = 4*18 = 72, so range(72, 0, -4) yields 72..=4 → 18 items),
        // so every word is consumed. 不可說 → 10^72 … 萬 → 10^4.
        let max = 4 * high.len() as u32;
        let mut n = max;
        for word in high.iter() {
            if n == 0 {
                break;
            }
            cards.insert(BigInt::from(10u8).pow(n), *word);
            n -= 4;
        }

        set_mid_numwords(&mut cards, &[(1000, "千"), (100, "百"), (10, "十")]);
        // Python's last entry is the tuple ("零", "〇"); stored pre-selected.
        set_low_numwords(
            &mut cards,
            &[
                "九", "八", "七", "六", "五", "四", "三", "二", "一", ZERO_WORD,
            ],
        );

        // Num2Word_Base.__init__: MAXVAL = 1000 * list(self.cards.keys())[0].
        // The OrderedDict's first *inserted* key is the highest card (10^72),
        // which is also `Cards::highest()`. → 10^75.
        let maxval = cards.highest().cloned().unwrap_or_else(BigInt::zero) * BigInt::from(1000);

        LangZhHk {
            cards,
            maxval,
            // Built once here, never per call. `to_currency` only ever reads
            // this table, and rebuilding a 17-entry HashMap per conversion is
            // how an earlier revision of this port ended up slower than the
            // Python it replaces.
            currency_forms: build_currency_forms(),
        }
    }

    /// `Num2Word_Base.verify_ordinal`, minus the float arm (integer input only).
    fn verify_ordinal(&self, value: &BigInt) -> Result<()> {
        // `if not abs(value) == value: raise TypeError(self.errmsg_negord % value)`
        if value.is_negative() {
            return Err(N2WError::Type(format!(
                "Cannot treat negative num {} as ordinal.",
                value
            )));
        }
        Ok(())
    }

    /// `Num2Word_ZH.zh_to_cap(value, capital=False)`.
    ///
    /// The `capital` arm (CAP_map substitution) is unreachable from the four
    /// in-scope modes — `capital` is `reading == "capital"`, and `reading` is
    /// always `False` here — so only the `elif` arm is ported:
    ///
    /// ```python
    /// elif out.startswith(one + ten):
    ///     out = out[len(one):]
    /// return out
    /// ```
    ///
    /// `len(one)` is 1 in *characters* (Python slices strings by character),
    /// so this drops exactly one char — hence `chars().skip(1)` rather than a
    /// byte slice, since 一 is 3 bytes in UTF-8.
    ///
    /// Bug #1/#2 in the module docs live here: the test is anchored at the
    /// start of the string, so "負一十二" keeps its 一 while "一十萬" loses it.
    fn zh_to_cap_plain(&self, value: &str) -> String {
        let one_ten = format!("{}{}", ONE_WORD, TEN_WORD);
        if value.starts_with(&one_ten) {
            value.chars().skip(1).collect()
        } else {
            value.to_string()
        }
    }

    /// `Num2Word_ZH.to_cardinal(value, stuff_zero, reading, prefer)` with the
    /// kwargs live:
    ///
    /// ```python
    /// self.stuff_zero = stuff_zero
    /// self.set_str_selection(reading, prefer)
    /// out = super().to_cardinal(value).replace(" ", "")
    /// return self.zh_to_cap(out, reading == "capital")
    /// ```
    ///
    /// `prefer` can only re-select the zero card (the sole tuple entry);
    /// `stuff_zero` rides through `merge`; `reading == "capital"` takes
    /// `zh_to_cap`'s CAP_map arm, which performs **no** leading-一 strip
    /// (11 → "壹拾壹").
    fn kw_cardinal(
        &self,
        value: &BigInt,
        stuff_zero: i64,
        reading: Reading,
        prefer: Option<&[String]>,
    ) -> Result<String> {
        let zero = select_alt(&ZERO_ALTS, prefer);
        let mut cards = self.cards.clone();
        if zero != ZERO_WORD {
            cards.insert(BigInt::zero(), zero);
        }
        let eng = HkKwEngine {
            base: self,
            cards,
            stuff_zero,
            zero_word: zero,
        };
        let out = default_to_cardinal(&eng, value)?.replace(' ', "");
        Ok(match reading {
            Reading::Capital => apply_cap_map(&out, &HK_CAP_MAP),
            _ => self.zh_to_cap_plain(&out),
        })
    }

    /// `self.CURRENCY_FORMS[currency]`, with the `KeyError` → `NotImplementedError`
    /// translation both `to_currency` and Base's `to_cheque` spell out
    /// identically:
    ///
    /// ```python
    /// except KeyError:
    ///     raise NotImplementedError(
    ///         'Currency code "%s" not implemented for "%s"'
    ///         % (currency, self.__class__.__name__))
    /// ```
    ///
    /// Returns the *bare string* ("歐羅"), which is what ZH's table holds — the
    /// [`CurrencyForms`] wrapper is only a container, see [`bare`].
    fn currency_string(&self, code: &str) -> Result<&str> {
        self.currency_forms
            .get(code)
            // Indexing is safe: `bare()` always writes exactly one unit form.
            .map(|f| f.unit[0].as_str())
            .ok_or_else(|| {
                N2WError::NotImplemented(format!(
                    "Currency code \"{}\" not implemented for \"{}\"",
                    code,
                    self.lang_name()
                ))
            })
    }

    /// `self.cards[d]` for one digit. A miss is Python's `KeyError`;
    /// unreachable, since `set_low_numwords` fills 0..=9.
    fn card(&self, d: u32) -> Result<&str> {
        self.cards
            .get(&BigInt::from(d))
            .ok_or_else(|| N2WError::Key(format!("{}", d)))
    }

    /// `Num2Word_ZH.to_currency_float(value, reading=False, prefer=None)`.
    ///
    /// ```python
    /// cents = "%02d" % value
    /// out = []
    /// if int(cents) > 0:
    ///     if not (int(cents[0]) == 0 and reading == "capital"):
    ///         out += [self.cards[int(cents[0])]]
    ///     if int(cents[0]) > 0:
    ///         out += [self.CURRENCY_FLOATS[0]]
    ///     if int(cents[1]) > 0:
    ///         out += [self.cards[int(cents[1])], self.CURRENCY_FLOATS[1]]
    /// return out
    /// ```
    ///
    /// `value` is a Python `int`: `to_currency` runs `parse_currency_parts`
    /// with `keep_precision=False`, whose float branch ends
    /// `cents = int(fraction * divisor)`. It is also always in `0..=99`
    /// (`fraction < 1` and `divisor` is 100) and never negative — the parse
    /// `abs()`es first — so `"%02d"` yields exactly two characters and
    /// `int(cents) > 0` reduces to `value > 0`.
    ///
    /// Two asymmetries worth not "tidying":
    ///
    /// * the 毫 unit is emitted only when the 1/10 digit is non-zero, but the
    ///   *digit word* is emitted regardless (the `reading == "capital"` guard
    ///   on it is dead here) — that is what puts the bare 零 in 0.01's
    ///   "零元**零**一仙" while 0.50 gets "五毫" and no 仙 at all;
    /// * the 仙 unit, by contrast, is bound to its own digit, so a trailing
    ///   zero subunit vanishes rather than reading "…零仙".
    fn to_currency_float(&self, value: &BigInt) -> Result<Vec<&str>> {
        let mut out: Vec<&str> = Vec::new();
        if !value.is_positive() {
            return Ok(out);
        }

        // `"%02d" % value`. Zero-padded through the string, as
        // `currency::default_cents_terse` does — `BigInt`'s `Display` routes
        // through `pad_integral` and would not honour a bare `{:02}`.
        let cents = format!("{:0>2}", value.to_string());
        let digits: Vec<char> = cents.chars().collect();
        // `cents[0]` / `cents[1]` — Python indexes str by character. Padding
        // guarantees at least two; a hypothetical 3-digit value would take the
        // leading two, exactly as Python's subscripts do.
        let d0 = py_int_digit(digits[0])?;
        let d1 = py_int_digit(digits[1])?;

        out.push(self.card(d0)?);
        if d0 > 0 {
            out.push(CURRENCY_FLOATS[0]);
        }
        if d1 > 0 {
            out.push(self.card(d1)?);
            out.push(CURRENCY_FLOATS[1]);
        }
        Ok(out)
    }
}

/// `int(ch)` for a single character. Python raises `ValueError` on a
/// non-digit; unreachable here, since the caller's string comes from
/// `"%02d" % <non-negative int>`.
fn py_int_digit(ch: char) -> Result<u32> {
    ch.to_digit(10).ok_or_else(|| {
        N2WError::Value(format!("invalid literal for int() with base 10: '{}'", ch))
    })
}

/// `len(str(n))` — Python's decimal digit count (a leading "-" would count,
/// exactly as `BigInt`'s `Display` renders it; in `merge` these are always
/// non-negative anyway). Returned as `i64` because `merge` subtracts two of
/// these and the difference is routinely negative.
fn py_len_str(n: &BigInt) -> i64 {
    n.to_string().len() as i64
}

/// `Num2Word_ZH.merge`, verbatim, with the two per-call inputs live:
/// `self.stuff_zero` (the `to_cardinal` kwarg) and
/// `select_text(self.low_numwords[-1])` (the 零/〇 the `prefer` kwarg picks).
fn zh_merge(
    l: (&str, &BigInt),
    r: (&str, &BigInt),
    stuff_zero: i64,
    zero_word: &str,
) -> (String, BigInt) {
    let (ltext, lnum) = l;
    let (rtext, rnum) = r;

    // ignore lpair if lnum is 1 and rnum is less than 10
    if lnum.is_one() && rnum < &BigInt::from(10) {
        return (rtext.to_string(), rnum.clone());
    }

    // stuff_zero logic between discontinous numbers
    // http://www.hkame.org.hk/uploaded_files/magazine/15/271.pdf
    let with_zero = || (format!("{}{}{}", ltext, zero_word, rtext), lnum + rnum);
    let no_zero = || (format!("{}{}", ltext, rtext), lnum + rnum);

    let ldigits = py_len_str(lnum);
    let rdigits = py_len_str(rnum);

    if ldigits - rdigits > 1 {
        match stuff_zero {
            // 凡「零」必讀 — every discontinuity is spoken.
            1 => return with_zero(),
            // Discontinous high numbers. The Python inner test re-checks
            // `len(str(lnum)) - len(str(rnum)) > 1`, which the outer `if`
            // already established; only the `% 4` half carries information.
            2 => {
                if rdigits % 4 != 0 {
                    return with_zero();
                }
                return no_zero();
            }
            // 凡「零」不讀 — never.
            3 => return no_zero(),
            // Python's if/elif chain has no else: any other stuff_zero
            // (None, 4, "2", ...) falls through to the trailing
            // `return no_zero` — `None == 1` etc. are all simply False.
            _ => {}
        }
    } else if rnum > lnum {
        return (format!("{}{}", ltext, rtext), lnum * rnum);
    }
    no_zero()
}

// ---- grammatical kwargs (reading / prefer / stuff_zero / counter) ----------

/// The three states `reading` can put `select_text`/`zh_to_cap` in: Python
/// tests `reading is True` (only the bool `True`) and `reading == "capital"`;
/// everything else behaves like the default `False`.
#[derive(Clone, Copy, PartialEq)]
enum Reading {
    Plain,
    True,
    Capital,
}

fn parse_reading(kw: &Kwargs) -> Reading {
    match kw.get("reading") {
        Some(KwVal::Bool(true)) => Reading::True,
        Some(KwVal::Str(s)) if s == "capital" => Reading::Capital,
        _ => Reading::Plain,
    }
}

/// `prefer` as the item set `select_text` intersects with. A list keeps its
/// members, a str iterates characters (`set("〇") == {"〇"}`); a non-iterable
/// raises TypeError inside Python's `set()` — NotImplemented lets the
/// dispatcher fall back to the original, which owns both that raise and the
/// silently-succeeding cases where no tuple card is ever selected.
fn parse_prefer(kw: &Kwargs) -> Result<Option<Vec<String>>> {
    match kw.get("prefer") {
        None | Some(KwVal::None) => Ok(None),
        Some(KwVal::List(l)) => Ok(Some(l.clone())),
        Some(KwVal::Str(s)) => Ok(Some(s.chars().map(|c| c.to_string()).collect())),
        Some(_) => Err(N2WError::Fallback("kwargs".into())),
    }
}

/// `stuff_zero`, defaulting to 2. Bools are Python ints; any other type
/// compares unequal to 1/2/3 and takes `zh_merge`'s fall-through arm (0).
fn parse_stuff_zero(kw: &Kwargs) -> i64 {
    match kw.get("stuff_zero") {
        None => 2,
        Some(KwVal::Int(i)) => *i,
        Some(KwVal::Bool(b)) => *b as i64,
        Some(_) => 0,
    }
}

/// `counter`: only a `str` short-circuits `select_text`; anything else hits
/// `len(text)` there and raises TypeError — delegated back to Python.
fn parse_counter(kw: &Kwargs) -> Result<&str> {
    match kw.get("counter") {
        None => Ok(""),
        Some(KwVal::Str(s)) => Ok(s),
        Some(_) => Err(N2WError::Fallback("kwargs".into())),
    }
}

/// `select_text` over a tuple of plain-`str` alternatives (the only tuple
/// shape ZH's tables hold): the single member of `set(alts) & set(prefer)`
/// when exactly one matches, else the first alternative.
fn select_alt<'a>(alts: &[&'a str], prefer: Option<&[String]>) -> &'a str {
    if let Some(p) = prefer {
        let hits: Vec<&str> = alts
            .iter()
            .copied()
            .filter(|a| p.iter().any(|x| x == a))
            .collect();
        if hits.len() == 1 {
            return hits[0];
        }
    }
    alts[0]
}

/// `zh_to_cap`'s capital arm: sequential `str.replace` over `CAP_map`.
fn apply_cap_map(value: &str, map: &[(&str, &str)]) -> String {
    let mut out = value.to_string();
    for (plain, cap) in map {
        if out.contains(plain) {
            out = out.replace(plain, cap);
        }
    }
    out
}

/// `Num2Word_ZH_HK`'s runtime `CAP_map`: the parent `Num2Word_ZH` table
/// (traditional capitals, *with* the `("正", "整")` row ZH_CN drops) plus the
/// two `CAP_map_CHILD` rows `__init__` appends (毫 → 角, 仙 → 分).
const HK_CAP_MAP: [(&str, &str); 16] = [
    ("千", "仟"),
    ("百", "佰"),
    ("十", "拾"),
    ("九", "玖"),
    ("八", "捌"),
    ("七", "柒"),
    ("六", "陸"),
    ("五", "伍"),
    ("四", "肆"),
    ("三", "叁"),
    ("二", "貳"),
    ("一", "壹"),
    ("元", "圓"),
    ("正", "整"),
    ("毫", "角"),
    ("仙", "分"),
];

/// The `("零", "〇")` card — the only `prefer`-selectable table entry.
const ZERO_ALTS: [&str; 2] = ["零", "〇"];
/// `year_prefix = ("公元", "西元")` — the other `prefer`-selectable tuple.
const YEAR_PREFIX_ALTS: [&str; 2] = ["公元", "西元"];

/// Digits 0-9 as `select_text(self.cards[d])` yields them at the defaults
/// (identical glyphs in both scripts; 0 is the tuple's first form).
const HK_DIGITS: [&str; 10] = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"];

/// A per-call view of the engine with the `to_cardinal` kwargs live.
struct HkKwEngine<'a> {
    base: &'a LangZhHk,
    cards: Cards,
    stuff_zero: i64,
    zero_word: &'static str,
}

impl Lang for HkKwEngine<'_> {
    fn cards(&self) -> &Cards {
        &self.cards
    }
    fn maxval(&self) -> &BigInt {
        self.base.maxval()
    }
    fn negword(&self) -> &str {
        self.base.negword()
    }
    fn pointword(&self) -> &str {
        self.base.pointword()
    }
    fn merge(&self, l: (&str, &BigInt), r: (&str, &BigInt)) -> (String, BigInt) {
        zh_merge(l, r, self.stuff_zero, self.zero_word)
    }
}

/// Python's `str(<float>)` for a finite value — fills the `%s` of the
/// TypeError format strings (`errmsg_floatord`/`errmsg_negord`/
/// `errmsg_floatyear`). The corpora record only the type; the message
/// mirrors CPython's spelling.
fn py_float_str(value: f64, precision: u32) -> String {
    let a = value.abs();
    let mag = if a != 0.0 && (a >= 1e16 || a < 1e-4) {
        let s = format!("{:e}", a);
        let (mant, exp) = s.split_once('e').expect("LowerExp always emits an e");
        let exp: i32 = exp.parse().expect("exponent is a small int");
        format!(
            "{}e{}{:02}",
            mant,
            if exp < 0 { '-' } else { '+' },
            exp.abs()
        )
    } else {
        format!("{:.*}", precision as usize, a)
    };
    if value.is_sign_negative() {
        format!("-{}", mag)
    } else {
        mag
    }
}

/// `str(value)` for either FloatValue arm (Decimal's `%s` is its `str`).
fn py_value_str(value: &FloatValue) -> String {
    match value {
        FloatValue::Float { value, precision } => py_float_str(*value, *precision),
        FloatValue::Decimal { value, .. } => crate::strnum::python_decimal_str(value),
    }
}

impl Lang for LangZhHk {
    /// This language's own `to_currency(currency=...)` default,
    /// read from the live Python signature. Only 44 of 156 use EUR.
    fn default_currency(&self) -> &str {
        "XXX"
    }

    /// This language's own `to_currency(separator=...)` default,
    /// read from the live Python signature. Base's is ",", but only
    /// 36 of 149 languages actually use it — most default to " " or a
    /// conjunction, so inheriting Base's comma silently corrupts them.
    fn default_separator(&self) -> &str {
        ""
    }

    fn cards(&self) -> &Cards {
        &self.cards
    }

    fn maxval(&self) -> &BigInt {
        &self.maxval
    }

    fn negword(&self) -> &str {
        "負"
    }

    fn pointword(&self) -> &str {
        "點"
    }

    /// `Num2Word_ZH.merge`.
    ///
    /// `select_text(ltext)`/`select_text(rtext)` are identities at the default
    /// reading (see module docs), so they are elided; likewise
    /// `select_text(self.low_numwords[-1])` is [`ZERO_WORD`] at the defaults.
    /// The body lives in [`zh_merge`], shared with the kwargs engine, which
    /// carries the live `stuff_zero` and the `prefer`-selected zero.
    fn merge(&self, l: (&str, &BigInt), r: (&str, &BigInt)) -> (String, BigInt) {
        zh_merge(l, r, STUFF_ZERO as i64, ZERO_WORD)
    }

    /// `Num2Word_ZH.to_cardinal(value, stuff_zero=2, reading=False, prefer=None)`:
    ///
    /// ```python
    /// out = super().to_cardinal(value).replace(" ", "")
    /// return self.zh_to_cap(out, reading == "capital")
    /// ```
    ///
    /// The `replace(" ", "")` is what welds the negword on: the base emits
    /// `"負 " + words` (from `"%s " % self.negword.strip()`), and the space is
    /// then squeezed out → "負一". It also strips the separators `merge` never
    /// inserts, making it a no-op for positives.
    fn to_cardinal(&self, value: &BigInt) -> Result<String> {
        let out = default_to_cardinal(self, value)?.replace(' ', "");
        Ok(self.zh_to_cap_plain(&out))
    }

    /// `Num2Word_ZH.to_ordinal(value, counter="", reading=False, prefer=None)`:
    ///
    /// ```python
    /// self.verify_ordinal(value)
    /// base = self.to_cardinal(value, reading=reading, prefer=prefer)
    /// return "%s%s%s" % (select_text(self.ord_prefix), base, select_text(counter))
    /// ```
    ///
    /// `ord_prefix` is the plain string "第"; `counter` defaults to `""` and
    /// `select_text("")` short-circuits on `isinstance(text, strtype)` → "".
    /// Note the 第 is prepended *after* `to_cardinal` has already run
    /// `zh_to_cap`, so the strip still sees the bare numeral: 100000 →
    /// "一十萬" → "十萬" → "第十萬".
    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        let base = self.to_cardinal(value)?;
        Ok(format!("第{}", base))
    }

    /// `Num2Word_ZH.to_ordinal_num(value, counter="", ...)`:
    ///
    /// ```python
    /// return "%s%s%s" % (select_text(self.ord_prefix), value, select_text(counter))
    /// ```
    ///
    /// No `verify_ordinal`, no `to_cardinal`, no bounds check — the value is
    /// interpolated with `%s`, i.e. `str(value)`. Bug #3: negatives sail
    /// through, so `to_ordinal_num(-1)` == "第-1".
    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        Ok(format!("第{}", value))
    }

    /// `Num2Word_ZH.to_year(value, reading=False, prefer=None)`.
    ///
    /// ```python
    /// out = []
    /// if value < 0:
    ///     out += [self.year_prefix, self.year_bce]
    /// elif reading == "capital":
    ///     out += [self.year_prefix]
    /// out += [self.cards[int(s)] for s in str(abs(int(value)))]
    /// out += [self.year]
    /// return "".join(self.select_text(s) for s in out)
    /// ```
    ///
    /// Digit-by-digit, *not* via `to_cardinal` — so 10 → "一零年", not "十年",
    /// and there is no `MAXVAL` guard (bug #4). `year_prefix` is the tuple
    /// `("公元", "西元")` → "公元" at the default reading; `year_bce` = "前";
    /// `year` = "年". The `reading == "capital"` arm is unreachable here, so a
    /// positive year gets no prefix at all: 1 → "一年".
    ///
    /// The float guard (`if not value == int(value): raise TypeError`) is
    /// vacuous for `BigInt` input and is omitted.
    fn to_year(&self, value: &BigInt) -> Result<String> {
        let mut out = String::new();
        if value.is_negative() {
            out.push_str("公元"); // select_text(("公元", "西元")) at default reading
            out.push_str("前"); // year_bce
        }

        // str(abs(int(value))) — abs() first, so no sign char reaches the
        // cards lookup.
        for ch in value.abs().to_string().chars() {
            let d = ch.to_digit(10).ok_or_else(|| {
                // Unreachable: abs() of a BigInt renders as digits only.
                N2WError::Value(format!("invalid literal for int() with base 10: '{}'", ch))
            })?;
            let word = self
                .cards
                .get(&BigInt::from(d))
                .ok_or_else(|| N2WError::Key(format!("{}", d)))?;
            out.push_str(word);
        }

        out.push_str("年"); // self.year
        Ok(out)
    }

    /// `Num2Word_ZH.to_cardinal_float(value)`:
    ///
    /// ```python
    /// def to_cardinal_float(self, value):
    ///     out = super().to_cardinal_float(value).replace(" ", "")
    ///     return self.zh_to_cap(out, self.capital)
    /// ```
    ///
    /// `super().to_cardinal_float` is `Num2Word_Base.to_cardinal_float` — the
    /// [`default_to_cardinal_float`] port — which space-joins the integer part,
    /// 點, and each fractional digit (`"零 點 五"`). ZH squeezes the spaces out
    /// with the same `replace(" ", "")` its integer `to_cardinal` uses to weld
    /// 負 on, then runs `zh_to_cap` over the whole string. The default trait
    /// impl would return the *space-joined* form, so this override is required.
    ///
    /// The integer part is produced by `self.to_cardinal(pre)` inside the base
    /// method, i.e. ZH's own wrapped `to_cardinal`, so its leading-一 strip has
    /// already fired: `12.34` → `to_cardinal(12)` = "十二" → "十二點三四", and
    /// `-12.34` → `to_cardinal(-12)` = "負一十二" (bug #1, the strip is
    /// prefix-anchored and a leading 負 blocks it) → "負一十二點三四".
    ///
    /// Two Python facts pinned down here:
    ///
    /// * **ZH's override drops the `precision=` parameter.** Its signature is
    ///   `to_cardinal_float(self, value)` — no `precision` — so it always calls
    ///   `super().to_cardinal_float(value)` with `precision=None`, and base then
    ///   lets `float2tuple` recompute `self.precision` from the value's own
    ///   `repr`/`as_tuple().exponent`. `precision=` is therefore a no-op for
    ///   this language (verified live: `num2words(0.5, lang="zh_HK",
    ///   precision=5)` is still "零點五", not "零點五零零零零"). So
    ///   `precision_override` is deliberately ignored and `None` threaded
    ///   through — honouring it would pad/truncate the fraction and diverge.
    ///   See `concerns`.
    /// * **The outer `zh_to_cap` is a no-op.** The string always begins with
    ///   the already-stripped integer part (or 負 when value<0 and pre==0),
    ///   never a fresh "一十", so the leading-一 strip can never fire again
    ///   (bug #9's idempotence). Applied anyway, exactly as Python does; the
    ///   `capital` flag is `False` on every path that can reach Rust.
    fn to_cardinal_float(
        &self,
        value: &FloatValue,
        _precision_override: Option<u32>,
    ) -> Result<String> {
        let out = default_to_cardinal_float(self, value, None)?.replace(' ', "");
        Ok(self.zh_to_cap_plain(&out))
    }

    // ---- currency ---------------------------------------------------------
    //
    // `Num2Word_ZH` overrides `to_currency` outright, so only `lang_name`,
    // `currency_forms` and the two entry points below are language-specific.
    // Everything else keeps its trait default *because Python does too*:
    // `pluralize` raises (ZH has no plural forms and never calls it);
    // `currency_adjective` is None and `currency_precision` is 100 (both dicts
    // are empty); `money_verbose` is `to_cardinal` (Base's, used by
    // `to_cheque`); `cents_verbose`/`cents_terse` are unreachable.

    fn lang_name(&self) -> &str {
        "Num2Word_ZH_HK"
    }

    fn currency_forms(&self, code: &str) -> Option<&CurrencyForms> {
        self.currency_forms.get(code)
    }

    /// `Num2Word_ZH.to_currency`:
    ///
    /// ```python
    /// self.set_str_selection(reading, prefer)
    /// left, right, is_negative = parse_currency_parts(val, is_int_with_cents=False)
    /// try:
    ///     cr = self.CURRENCY_FORMS[currency]
    /// except KeyError:
    ///     raise NotImplementedError(...)
    /// minus_str = self.negword if is_negative else ""
    /// money_str = self.to_cardinal(left, reading=reading, prefer=prefer)
    /// if currency == "XXX":
    ///     cr_pre, cr_post = ("", cr)
    /// else:
    ///     cr_pre, cr_post = (cr, self.CURRENCY_FORMS["XXX"])
    /// cents_str = self.to_currency_float(right, reading=reading, prefer=prefer)
    /// cheque = self.cheque_suffix if len(cents_str) == 0 and reading == "capital" else ""
    /// for c in [minus_str, money_str, cr_post, *cents_str, cheque]:
    ///     cr_pre += self.zh_to_cap(self.select_text(c), reading == "capital")
    /// return cr_pre
    /// ```
    ///
    /// `cents`, `separator` and `adjective` are in ZH's signature and are never
    /// read by its body — there is no `_cents_verbose` call to switch, nothing
    /// to interpolate a separator between, and a `# CURRENCY_ADJECTIVES are not
    /// implemented` comment where the prefix would go. Hence the three `_`
    /// parameters: ignoring them is the port, not an omission. (`separator`
    /// still arrives pre-resolved through `default_separator`, which is `""`
    /// for this language — see the override above.)
    fn to_currency(
        &self,
        val: &CurrencyValue,
        currency: &str,
        _cents: bool,
        _separator: Option<&str>,
        _adjective: bool,
    ) -> Result<String> {
        // `parse_currency_parts(val, is_int_with_cents=False)` — ZH passes that
        // one kwarg and nothing else, so `keep_precision=False` and
        // `divisor=100` stay at *currency.py's* defaults. The 100 is hardcoded
        // rather than read from `currency_precision()` on purpose: ZH never
        // consults CURRENCY_PRECISION, so a hypothetical KWD entry would not
        // make this path use 1000. The two happen to agree only because ZH's
        // CURRENCY_PRECISION is empty.
        //
        // Consequences worth naming: for a true `int` the float branch is
        // skipped entirely and `right` is 0, so ints never print subunits; for
        // a float, `keep_precision=False` means the value is first quantized to
        // 2dp ROUND_HALF_UP (2.675 → 2.68 → 二元六毫八仙) and fractional cents
        // can never survive — which is why `cardinal_from_decimal` stays at its
        // default and this language needs no fractional-cents branch.
        let (left, right, is_negative) = parse_currency_parts(val, false, false, 100);
        // `cents = int(fraction * divisor)` already truncated to scale 0.
        let right = right.as_bigint_and_exponent().0;

        let cr = self.currency_string(currency)?;

        // `self.negword`, *not* Base's `"%s " % self.negword.strip()`: ZH adds
        // no trailing space, because nothing in the output is space-separated.
        let minus_str = if is_negative { self.negword() } else { "" };

        // `self.to_cardinal(left, ...)` — the *absolute* integer part, since
        // `parse_currency_parts` split the sign off into `is_negative`. So the
        // leading-一 strip fires normally and -12.34 reads 負 + 十二; contrast
        // module-doc bug #1, where `to_cardinal(-12)` on its own yields the
        // unstripped 負一十二.
        let money_str = self.to_cardinal(&left)?;

        // A non-XXX code prefixes its own name and *still* closes the integer
        // part with the generic 元: "歐羅一百元", not "歐羅一百歐羅".
        let (mut cr_pre, cr_post) = if currency == "XXX" {
            (String::new(), cr)
        } else {
            // `self.CURRENCY_FORMS["XXX"]` is a subscript, so a miss here would
            // be KeyError rather than the NotImplementedError above — but "XXX"
            // is a class-body literal that no override removes.
            let xxx = self
                .currency_forms
                .get("XXX")
                .expect("XXX is a class-body literal of Num2Word_ZH.CURRENCY_FORMS");
            (cr.to_string(), xxx.unit[0].as_str())
        };

        let cents_str = self.to_currency_float(&right)?;

        // `cheque = self.cheque_suffix if len(cents_str) == 0 and reading ==
        // "capital" else ""`. 正 is only ever appended in a capital reading,
        // which cannot reach this path, so `cheque` is always "" and its
        // append is a no-op. Omitted rather than modelled as `push_str("")`.
        //
        // `select_text(c)` is the identity on every fragment here: they are all
        // plain `str`, and the one tuple-valued card (`cards[0]`) is stored
        // pre-selected as 零. `zh_to_cap(c, False)` is likewise a no-op on all
        // of them (bug #9) but is applied anyway, as Python does.
        for c in [minus_str, money_str.as_str(), cr_post]
            .into_iter()
            .chain(cents_str)
        {
            cr_pre.push_str(&self.zh_to_cap_plain(c));
        }
        Ok(cr_pre)
    }

    /// `Num2Word_Base.to_cheque`, inherited unchanged — `Num2Word_ZH` overrides
    /// `to_currency` but leaves this alone. Reimplemented here instead of
    /// delegating to [`crate::currency::default_to_cheque`] for exactly one
    /// reason: Base unpacks the currency entry as a 2-tuple, and ZH's entries
    /// are strings.
    ///
    /// ```python
    /// try:
    ///     cr1, _cr2 = self.CURRENCY_FORMS[currency]
    /// except KeyError:
    ///     raise NotImplementedError(...)
    /// ...
    /// unit = cr1[-1] if isinstance(cr1, tuple) else cr1
    /// ```
    ///
    /// **Bug #7.** Unpacking a `str` iterates its *characters*, so `cr1, _cr2 =
    /// "歐羅"` binds `cr1 = "歐"`, `_cr2 = "羅"` — and the `except` clause
    /// catches only `KeyError`, so the unpack's `ValueError` escapes uncaught.
    /// Every outcome below is pinned by the frozen corpus:
    ///
    /// | code | value | chars | `to_cheque(1234.56)` |
    /// |---|---|---|---|
    /// | EUR | 歐羅 | 2 | `"一千二百三十四 AND 56/100 歐"` — **half the name** |
    /// | CNY | 人民幣 | 3 | `ValueError: too many values to unpack (expected 2)` |
    /// | CHF | 瑞士法郎 | 4 | `ValueError: too many values to unpack (expected 2)` |
    /// | XXX | 元 | 1 | `ValueError: not enough values to unpack (expected 2, got 1)` |
    /// | KWD | — | — | `KeyError` → `NotImplementedError` |
    ///
    /// So `to_cheque` "succeeds" for only 9 of the 17 codes (AUD CAD EUR GBP
    /// HKD JPY KRW THB USD — the two-character ones), and even then prints just
    /// the first half of the currency name. The other 8 raise `ValueError` on a
    /// perfectly valid code. `N2WError::Value` is the right variant precisely
    /// *because* Python's failure is a `ValueError` and not a currency error —
    /// mapping it to `NotImplemented` would erase the distinction the corpus
    /// tests. Do not "fix" any of this.
    fn to_cheque(&self, val: &BigDecimal, currency: &str) -> Result<String> {
        let cr = self.currency_string(currency)?;

        // `cr1, _cr2 = <str>` — an iterable unpack over characters.
        let chars: Vec<char> = cr.chars().collect();
        if chars.len() != 2 {
            return Err(N2WError::Value(if chars.len() < 2 {
                format!(
                    "not enough values to unpack (expected 2, got {})",
                    chars.len()
                )
            } else {
                "too many values to unpack (expected 2)".to_string()
            }));
        }
        // `unit = cr1[-1] if isinstance(cr1, tuple) else cr1` — cr1 is a
        // one-character `str`, never a tuple, so `unit` is cr1 itself.
        let unit = chars[0];

        // `self.CURRENCY_PRECISION.get(currency, 100)` — empty dict, so 100 for
        // every code. Read through the hook, as Base reads the dict.
        let divisor = self.currency_precision(currency);
        let is_negative = val.is_negative();
        let abs_val = val.abs();
        // `whole = int(abs_val)` — truncation, which on a non-negative equals
        // the floor `with_scale(0)` performs.
        let whole = abs_val.with_scale(0).as_bigint_and_exponent().0;

        let fraction_str = if divisor > 1 {
            let sub = (&abs_val - BigDecimal::from(whole.clone())) * BigDecimal::from(divisor);
            let sub = sub.with_scale(0).as_bigint_and_exponent().0;
            let digits = divisor.to_string().len() - 1;
            format!("{:0>width$}/{}", sub.to_string(), divisor, width = digits)
        } else {
            String::new()
        };

        // Base's `_money_verbose`, i.e. `self.to_cardinal(whole)` — ZH's
        // wrapped one, so 1234 → 一千二百三十四.
        let words = self.money_verbose(&whole, currency)?;
        let sign = if is_negative { "MINUS " } else { "" };
        let body = if fraction_str.is_empty() {
            format!("{} {}", words, unit)
        } else {
            format!("{} AND {} {}", words, fraction_str, unit)
        };
        // `.upper()` — a no-op on CJK; the literals are already uppercase.
        Ok(format!("{}{}", sign, body).to_uppercase())
    }

    // ---- float/Decimal entry routing --------------------------------------

    /// `to_ordinal(float/Decimal)`: `Num2Word_Base.verify_ordinal` runs with
    /// both arms live. Non-whole → TypeError(`errmsg_floatord`) *first*;
    /// whole-but-negative → TypeError(`errmsg_negord`); `-0.0` passes both
    /// (`int(-0.0) == -0.0`, `abs(-0.0) == -0.0`) → "第零". A whole value
    /// then takes `to_cardinal`'s integer path, prefixed with 第.
    fn ordinal_float_entry(&self, value: &FloatValue) -> Result<String> {
        match value.as_whole_int() {
            None => Err(N2WError::Type(format!(
                "Cannot treat float {} as ordinal.",
                py_value_str(value)
            ))),
            Some(i) => {
                if i.is_negative() {
                    return Err(N2WError::Type(format!(
                        "Cannot treat negative num {} as ordinal.",
                        py_value_str(value)
                    )));
                }
                Ok(format!("第{}", self.to_cardinal(&i)?))
            }
        }
    }

    /// `to_ordinal_num(float/Decimal)`: no verification — `str(value)`
    /// between 第 and the (default-empty) counter: "第-0.0", "第1e+16".
    fn ordinal_num_float_entry(&self, _value: &FloatValue, repr_str: &str) -> Result<String> {
        Ok(format!("第{}", repr_str))
    }

    /// `to_year(float/Decimal)`: `if not value == int(value)` raises
    /// TypeError(`errmsg_floatyear`); whole values render digit-by-digit
    /// through the integer `to_year` (`int(-0.0)` is 0 → no 公元前 prefix).
    fn year_float_entry(&self, value: &FloatValue) -> Result<String> {
        match value.as_whole_int() {
            None => Err(N2WError::Type(format!(
                "Cannot treat float {} as year.",
                py_value_str(value)
            ))),
            Some(i) => self.to_year(&i),
        }
    }

    // ---- grammatical kwargs ------------------------------------------------

    /// `to_cardinal(value, stuff_zero=2, reading=False, prefer=None)`.
    fn to_cardinal_kw(&self, value: &BigInt, kw: &Kwargs) -> Result<String> {
        if !kw.only(&["stuff_zero", "reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        let prefer = parse_prefer(kw)?;
        self.kw_cardinal(
            value,
            parse_stuff_zero(kw),
            parse_reading(kw),
            prefer.as_deref(),
        )
    }

    /// `to_ordinal(value, counter="", reading=False, prefer=None)`:
    /// `verify_ordinal` (negatives raise) then the kwargs cardinal at the
    /// default `stuff_zero=2` — Python forwards only `reading`/`prefer`.
    fn to_ordinal_kw(&self, value: &BigInt, kw: &Kwargs) -> Result<String> {
        if !kw.only(&["counter", "reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        let counter = parse_counter(kw)?;
        let prefer = parse_prefer(kw)?;
        let reading = parse_reading(kw);
        self.verify_ordinal(value)?;
        let base = self.kw_cardinal(value, 2, reading, prefer.as_deref())?;
        Ok(format!("第{}{}", base, counter))
    }

    /// `to_ordinal_num(value, counter="", reading=False, prefer=None)`:
    /// "第" + `str(value)` + counter; `reading`/`prefer` are inert (only
    /// plain strings ever reach `select_text` here).
    fn to_ordinal_num_kw(&self, value: &BigInt, kw: &Kwargs) -> Result<String> {
        if !kw.only(&["counter", "reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        let counter = parse_counter(kw)?;
        Ok(format!("第{}{}", value, counter))
    }

    /// `to_year(value, reading=False, prefer=None)`: the `elif reading ==
    /// "capital"` arm prefixes a positive year with 公元 — the digits stay
    /// un-capitalized (`to_year` never calls `zh_to_cap`). `prefer` can
    /// re-select the 零/〇 digit and the 公元/西元 prefix.
    fn to_year_kw(&self, value: &BigInt, kw: &Kwargs) -> Result<String> {
        if !kw.only(&["reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        let prefer = parse_prefer(kw)?;
        let reading = parse_reading(kw);
        let p = prefer.as_deref();

        let mut out = String::new();
        if value.is_negative() {
            out.push_str(select_alt(&YEAR_PREFIX_ALTS, p));
            out.push_str("前");
        } else if reading == Reading::Capital {
            out.push_str(select_alt(&YEAR_PREFIX_ALTS, p));
        }
        for ch in value.abs().to_string().chars() {
            let d = ch.to_digit(10).expect("abs(BigInt) is all digits") as usize;
            if d == 0 {
                out.push_str(select_alt(&ZERO_ALTS, p));
            } else {
                out.push_str(HK_DIGITS[d]);
            }
        }
        out.push_str("年");
        Ok(out)
    }

    /// `to_currency(val, ..., reading, prefer)` with the kwargs live. Every
    /// component runs through `zh_to_cap(select_text(c), capital)`; under
    /// capital that CAP-maps (元 → 圓, and HK's table *does* carry
    /// ("正", "整"), so the cheque suffix reads 整 — "零圓整") and the leading
    /// zero cents digit is skipped (`not (int(cents[0]) == 0 and reading ==
    /// "capital")`).
    fn to_currency_kw(
        &self,
        val: &CurrencyValue,
        currency: &str,
        cents: bool,
        separator: Option<&str>,
        adjective: bool,
        kw: &Kwargs,
    ) -> Result<String> {
        if !kw.only(&["reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        if kw.is_empty() {
            return self.to_currency(val, currency, cents, separator, adjective);
        }
        let prefer = parse_prefer(kw)?;
        let reading = parse_reading(kw);
        let p = prefer.as_deref();
        let capital = reading == Reading::Capital;

        let (left, right, is_negative) = parse_currency_parts(val, false, false, 100);
        let right = right.as_bigint_and_exponent().0;

        let cr = self.currency_string(currency)?;
        let minus_str = if is_negative {
            self.negword().to_string()
        } else {
            String::new()
        };
        let money_str = self.kw_cardinal(&left, 2, reading, p)?;
        let (mut out, cr_post) = if currency == "XXX" {
            (String::new(), cr.to_string())
        } else {
            let xxx = self
                .currency_forms
                .get("XXX")
                .expect("XXX is a class-body literal of Num2Word_ZH.CURRENCY_FORMS");
            (cr.to_string(), xxx.unit[0].clone())
        };

        // to_currency_float(right, reading, prefer) — the capital guard on
        // the leading zero digit is live here.
        let digit = |d: u32| -> String {
            if d == 0 {
                select_alt(&ZERO_ALTS, p).to_string()
            } else {
                HK_DIGITS[d as usize].to_string()
            }
        };
        let cents_num: u32 = right.to_string().parse().unwrap_or(0);
        let mut cents_parts: Vec<String> = Vec::new();
        if cents_num > 0 {
            let d0 = cents_num / 10;
            let d1 = cents_num % 10;
            if !(d0 == 0 && capital) {
                cents_parts.push(digit(d0));
            }
            if d0 > 0 {
                cents_parts.push(CURRENCY_FLOATS[0].to_string());
            }
            if d1 > 0 {
                cents_parts.push(digit(d1));
                cents_parts.push(CURRENCY_FLOATS[1].to_string());
            }
        }
        // cheque_suffix "正" — only in capital readings with no cents; the
        // loop's CAP-map pass turns it into 整.
        let cheque = if cents_parts.is_empty() && capital {
            "正".to_string()
        } else {
            String::new()
        };

        for c in std::iter::once(minus_str)
            .chain(std::iter::once(money_str))
            .chain(std::iter::once(cr_post))
            .chain(cents_parts)
            .chain(std::iter::once(cheque))
        {
            let piece = if capital {
                apply_cap_map(&c, &HK_CAP_MAP)
            } else {
                self.zh_to_cap_plain(&c)
            };
            out.push_str(&piece);
        }
        Ok(out)
    }

    /// `to_cardinal(float/Decimal, stuff_zero, reading, prefer)`. A whole
    /// value runs the integer engine with the kwargs live; a fractional one
    /// goes through `to_cardinal_float`, whose inner `self.to_cardinal(part)`
    /// calls reset every kwarg to its default — only the caller's final
    /// `zh_to_cap(out, reading == "capital")` survives.
    fn to_cardinal_float_kw(
        &self,
        value: &FloatValue,
        precision_override: Option<u32>,
        kw: &Kwargs,
    ) -> Result<String> {
        if !kw.only(&["stuff_zero", "reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        if kw.is_empty() {
            return self.cardinal_float_entry(value, precision_override);
        }
        let prefer = parse_prefer(kw)?;
        let reading = parse_reading(kw);
        if let Some(i) = value.as_whole_int() {
            return self.kw_cardinal(&i, parse_stuff_zero(kw), reading, prefer.as_deref());
        }
        let out = self.to_cardinal_float(value, None)?;
        Ok(match reading {
            Reading::Capital => apply_cap_map(&out, &HK_CAP_MAP),
            _ => self.zh_to_cap_plain(&out),
        })
    }
}

#[cfg(test)]
mod float_tests {
    use super::*;
    use std::str::FromStr;

    /// Drive the float arm the way the binding does.
    ///
    /// `precision` is *not* derived here: Python computes it as
    /// `abs(Decimal(repr(value)).as_tuple().exponent)`, which depends on
    /// `repr(float)` and is deliberately not reimplemented in the core. Every
    /// value below carries the precision the live interpreter reported for it.
    fn f(value: f64, precision: u32) -> String {
        LangZhHk::new()
            .to_cardinal_float(&FloatValue::Float { value, precision }, None)
            .unwrap()
    }

    /// Drive the Decimal arm — exact arbitrary precision, never an f64 cast.
    fn d(s: &str, precision: u32) -> String {
        LangZhHk::new()
            .to_cardinal_float(
                &FloatValue::Decimal {
                    value: BigDecimal::from_str(s).unwrap(),
                    precision,
                },
                None,
            )
            .unwrap()
    }

    /// Every `"to": "cardinal"` corpus row for `zh_HK` whose `arg` has a dot
    /// and is non-integral, i.e. every row that actually reaches the float
    /// path. ("0.0" and "1.0" are corpus rows too, but they satisfy
    /// `int(v) == v` in `Num2Word_Base.to_cardinal` and take the integer
    /// branch, so they never arrive here.)
    #[test]
    fn corpus_cardinal_float() {
        let rows: &[(f64, u32, &str)] = &[
            (0.5, 1, "零點五"),
            (1.5, 1, "一點五"),
            (2.25, 2, "二點二五"),
            (3.14, 2, "三點一四"),
            (0.01, 2, "零點零一"),
            (0.1, 1, "零點一"),
            (0.99, 2, "零點九九"),
            (1.01, 2, "一點零一"),
            // pre == 12 → "十二": ZH's leading-一 strip has already fired
            // inside to_cardinal before 點 is appended.
            (12.34, 2, "十二點三四"),
            (99.99, 2, "九十九點九九"),
            (100.5, 1, "一百點五"),
            (1234.56, 2, "一千二百三十四點五六"),
            // pre == 0 → the 負 comes from to_cardinal_float itself
            // (`value < 0 and pre == 0`), then the space-squeeze welds it on.
            (-0.5, 1, "負零點五"),
            (-1.5, 1, "負一點五"),
            // Bug #1: to_cardinal(-12) is "負一十二" — the leading-一 strip is
            // prefix-anchored and the 負 blocks it — so the float form keeps
            // the 一 that positive 12.34 loses. Corpus-pinned; do not "fix".
            (-12.34, 2, "負一十二點三四"),
            // The f64-artefact pair. 1.005 → post 4.999999999999893…,
            // 2.675 → post 674.9999999999998; the `< 0.01` heuristic in
            // float2tuple rounds both back up rather than flooring them, and
            // 1.005's "5" is then zero-padded to "005".
            (1.005, 3, "一點零零五"),
            (2.675, 3, "二點六七五"),
        ];
        for (value, precision, want) in rows {
            assert_eq!(&f(*value, *precision), want, "value {}", value);
        }
    }

    /// Every `"to": "cardinal_dec"` corpus row for `zh_HK`. The Decimal arm is
    /// exact: "1.10" keeps its trailing zero (post = 10, precision 2 → 一零),
    /// and 98_746_251_323_029.99 keeps its cents — the very case an f64 cast
    /// would corrupt at trillion scale (issue #603).
    #[test]
    fn corpus_cardinal_dec() {
        let rows: &[(&str, u32, &str)] = &[
            ("0.01", 2, "零點零一"),
            ("1.10", 2, "一點一零"),
            ("12.345", 3, "十二點三四五"),
            (
                "98746251323029.99",
                2,
                "九十八兆七千四百六十二億五千一百三十二萬三千零二十九點九九",
            ),
            ("0.001", 3, "零點零零一"),
        ];
        for (value, precision, want) in rows {
            assert_eq!(&d(value, precision.to_owned()), want, "value {}", value);
        }
    }

    /// `Num2Word_ZH.to_cardinal_float(self, value)` has no `precision`
    /// parameter, so the `precision=` kwarg is dropped before Base ever sees
    /// it — verified live: `num2words(0.5, lang="zh_HK", precision=5)` is
    /// still "零點五", not "零點五零零零零". The override must therefore
    /// ignore `precision_override`.
    #[test]
    fn precision_override_is_dropped() {
        let out = LangZhHk::new()
            .to_cardinal_float(
                &FloatValue::Float {
                    value: 0.5,
                    precision: 1,
                },
                Some(5),
            )
            .unwrap();
        assert_eq!(out, "零點五");
    }

    /// The strip *does* fire through the float path when nothing blocks it:
    /// pre == 11 → "一十一" → "十一", then 點五. (Live: 11.5 → "十一點五",
    /// 10.5 → "十點五" — 10 is a bare card and never had the 一.)
    #[test]
    fn leading_one_ten_strip_through_float_path() {
        assert_eq!(f(11.5, 1), "十一點五");
        assert_eq!(f(10.5, 1), "十點五");
    }
}
