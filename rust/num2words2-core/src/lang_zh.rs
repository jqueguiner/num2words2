//! Port of the class the `"zh"` code actually resolves to: `Num2Word_ZH_CN`
//! (`lang_ZH_CN.py`), which subclasses `Num2Word_ZH` (`lang_ZH.py`) →
//! `Num2Word_Base`.
//!
//! `Num2Word_ZH` is an abstract-ish base that nothing registers directly:
//! `__init__.py` maps `"zh"` (and `"zh_CN"`, `"cn"`) to `Num2Word_ZH_CN`, and
//! `"zh_TW"`/`"zh_HK"` to their own subclasses. `ZH_CN.setup()` calls
//! `super().setup()` and then overrides `negword`/`pointword`/`high_numwords`
//! with the **simplified** forms (负 / 点 / 万,亿,兆…), so this file reproduces
//! the simplified output the frozen corpus records for `"zh"`. `mid_numwords`
//! and `low_numwords` are *not* overridden by ZH_CN — they stay as ZH set them
//! (千/百/十, 九…一, ("零","〇")), whose glyphs are identical in both scripts.
//!
//! Engine-style: cards + `merge` drive `Num2Word_Base.to_cardinal`; ZH then
//! post-processes with `.replace(" ", "")` + `zh_to_cap`.
//!
//! Kwargs note: the Python methods take `reading`/`prefer`/`counter`/
//! `stuff_zero` keywords. The plain (no-kwargs) entry points hold their
//! defaults (`reading=False`, `prefer=None`, `counter=""`, `stuff_zero=2`),
//! which collapses `select_text` to a constant choice — see `select_text`
//! below. The `*_kw` hooks at the bottom of the `Lang` impl carry the live
//! kwargs: `reading="capital"` swaps in the 大寫 forms via `CAP_map`
//! (`zh_to_cap`'s capital arm), `prefer=["〇"]` re-selects the one
//! tuple-valued card `("零", "〇")`, and `stuff_zero` parameterizes `merge`.
//!
//! Float/Decimal entry semantics (`ordinal_float_entry` & friends):
//! `to_ordinal` runs `Num2Word_Base.verify_ordinal`, whose *float* arm is
//! live for float input — a non-whole value raises TypeError
//! (`errmsg_floatord`) before the negative check (`errmsg_negord`); note
//! `-0.0` passes both (`int(-0.0) == -0.0` and `abs(-0.0) == -0.0`), so
//! `to_ordinal(-0.0)` is "第零" while `to_ordinal(-1.0)` raises. `to_year`
//! raises its own TypeError (`errmsg_floatyear`) on non-whole values and
//! renders whole ones digit-by-digit ("一零零零年"). `to_ordinal_num` never
//! verifies anything: it interpolates `str(value)` — "第-0.0", "第1e+16".

use crate::base::{
    default_to_cardinal, set_low_numwords, set_mid_numwords, Cards, Kwargs, KwVal, Lang, N2WError,
    Result,
};
use crate::currency::CurrencyValue;
use crate::floatpath::FloatValue;
use bigdecimal::BigDecimal;
use num_bigint::BigInt;
use num_traits::{One, Signed, Zero};

/// `ord_prefix` — a plain `str`, so `select_text` returns it unchanged.
const ORD_PREFIX: &str = "第";
/// `year`, `year_bce` — plain `str`s.
const YEAR: &str = "年";
const YEAR_BCE: &str = "前";
/// `year_prefix = ("公元", "西元")` is a *tuple*. With `reading=False` and
/// `prefer=None`, `select_text` falls through to `text[0]` → "公元".
const YEAR_PREFIX: &str = "公元";
/// `select_text(self.low_numwords[-1])` where `low_numwords[-1] == ("零","〇")`
/// → "零" (same `text[0]` fallthrough).
const ZERO_WORD: &str = "零";

/// `to_cardinal`'s default `stuff_zero=2` — "discontinuous high numbers".
const STUFF_ZERO: u8 = 2;

pub struct LangZh {
    cards: Cards,
    maxval: BigInt,
    exclude_title: Vec<String>,
}

impl Default for LangZh {
    fn default() -> Self {
        Self::new()
    }
}

/// Python's `len(str(n))`. Values reaching `merge` are non-negative (base
/// `to_cardinal` takes `abs` first), so this is the plain decimal digit count.
fn digit_len(n: &BigInt) -> i64 {
    n.to_string().len() as i64
}

/// `Num2Word_ZH.merge`, verbatim, with the two per-call inputs live:
/// `self.stuff_zero` (set by `to_cardinal`'s kwarg) and
/// `select_text(self.low_numwords[-1])` (the 零/〇 the `prefer` kwarg picks).
fn zh_merge(
    l: (&str, &BigInt),
    r: (&str, &BigInt),
    stuff_zero: i64,
    zero_word: &str,
) -> (String, BigInt) {
    let (ltext, lnum) = l;
    let (rtext, rnum) = r;
    let ten = BigInt::from(10);

    // ignore lpair if lnum is 1 and rnum is less than 10
    if lnum.is_one() && rnum < &ten {
        return (rtext.to_string(), rnum.clone());
    }

    let with_zero = || (format!("{}{}{}", ltext, zero_word, rtext), lnum + rnum);
    let no_zero = || (format!("{}{}", ltext, rtext), lnum + rnum);

    let lo_len = digit_len(lnum);
    let ro_len = digit_len(rnum);

    if lo_len - ro_len > 1 {
        match stuff_zero {
            // 凡「零」必讀 — all discontinuous numbers
            1 => return with_zero(),
            // discontinuous *high* numbers only
            2 => {
                if lo_len - ro_len > 1 && ro_len % 4 != 0 {
                    return with_zero();
                }
                return no_zero();
            }
            // 凡「零」不讀 — no zeros
            3 => return no_zero(),
            // Python's if/elif chain has no else: any other stuff_zero
            // (None, 4, "2", ...) falls through to the trailing `return
            // no_zero` — `None == 1` etc. are all simply False.
            _ => {}
        }
    } else if rnum > lnum {
        return (format!("{}{}", ltext, rtext), lnum * rnum);
    }
    no_zero()
}

// ---- grammatical kwargs (reading / prefer / stuff_zero / counter) ----------

/// The three states `reading` can put `select_text`/`zh_to_cap` in.
///
/// Python tests `reading is True` (identity, so only the bool `True`) and
/// `reading == "capital"`; every other value — `False`, `None`, other
/// strings, ints — behaves like the default.
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

/// The `prefer` kwarg as the item set `select_text` intersects with.
///
/// Python does `set(text) & set(self.prefer or set())`: a list keeps its
/// members, a *string* iterates characters (`set("〇") == {"〇"}`), and a
/// non-iterable (int/bool) raises TypeError inside `set()` — returned as
/// NotImplemented so the dispatcher falls back to Python, which owns that
/// raise (and, for values whose rendering never touches a tuple card,
/// silently succeeds — the fallback reproduces both outcomes).
fn parse_prefer(kw: &Kwargs) -> Result<Option<Vec<String>>> {
    match kw.get("prefer") {
        None | Some(KwVal::None) => Ok(None),
        Some(KwVal::List(l)) => Ok(Some(l.clone())),
        Some(KwVal::Str(s)) => Ok(Some(s.chars().map(|c| c.to_string()).collect())),
        Some(_) => Err(N2WError::Fallback("kwargs".into())),
    }
}

/// `stuff_zero`, defaulting to 2. `True`/`False` are Python ints (1/0); any
/// non-int value compares unequal to 1/2/3 and takes `zh_merge`'s
/// fall-through arm, modelled as the sentinel 0.
fn parse_stuff_zero(kw: &Kwargs) -> i64 {
    match kw.get("stuff_zero") {
        None => 2,
        Some(KwVal::Int(i)) => *i,
        Some(KwVal::Bool(b)) => *b as i64,
        Some(_) => 0,
    }
}

/// The `counter` kwarg. Only a `str` reaches the output via `select_text`'s
/// `strtype` short-circuit; anything else (`None`, an int) hits `len(text)`
/// inside `select_text` and raises TypeError — delegated back to Python.
fn parse_counter(kw: &Kwargs) -> Result<&str> {
    match kw.get("counter") {
        None => Ok(""),
        Some(KwVal::Str(s)) => Ok(s),
        Some(_) => Err(N2WError::Fallback("kwargs".into())),
    }
}

/// `select_text` over a tuple of plain-`str` alternatives (the only tuple
/// shape ZH_CN's tables hold): the single member of `set(alts) & set(prefer)`
/// if exactly one matches, else the first alternative. `reading` never
/// matters for these tables — no item is itself a tuple.
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

/// `Num2Word_ZH_CN.CAP_map` — the 大寫 substitution table `zh_to_cap` walks
/// under `reading == "capital"`. ZH_CN re-declares the parent's table with
/// simplified capitals and **drops** the `("正", "整")` row, which is why the
/// cheque suffix stays 正 here ("零圆正") while zh_HK/zh_TW print 整.
const ZH_CN_CAP_MAP: [(&str, &str); 13] = [
    ("千", "仟"),
    ("百", "佰"),
    ("十", "拾"),
    ("九", "玖"),
    ("八", "捌"),
    ("七", "柒"),
    ("六", "陆"),
    ("五", "伍"),
    ("四", "肆"),
    ("三", "叁"),
    ("二", "贰"),
    ("一", "壹"),
    ("元", "圆"),
];

/// The `("零", "〇")` card — the only `prefer`-selectable table entry.
const ZERO_ALTS: [&str; 2] = ["零", "〇"];
/// `year_prefix = ("公元", "西元")` — the other `prefer`-selectable tuple.
const YEAR_PREFIX_ALTS: [&str; 2] = ["公元", "西元"];

/// A per-call view of the engine with the `to_cardinal` kwargs live:
/// `stuff_zero` parameterizes `merge`, and the zero card is re-selected
/// under `prefer` (the only card `select_text` can change).
struct ZhKwEngine<'a> {
    base: &'a LangZh,
    cards: Cards,
    stuff_zero: i64,
    zero_word: &'static str,
}

impl Lang for ZhKwEngine<'_> {
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

/// Python's `str(<float>)` for a finite value — used only to fill the `%s`
/// of the TypeError format strings (`errmsg_floatord`/`errmsg_negord`/
/// `errmsg_floatyear`); the corpora record the exception *type*, the message
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

impl LangZh {
    pub fn new() -> Self {
        // ZH_CN.setup() rebuilds high_numwords in simplified script, then
        // reverses it. Listed here already reversed: 10**72 first, 10**4 last.
        let high = [
            "不可说",     // 10 ** 72
            "无量",       // 10 ** 68
            "不可思议",   // 10 ** 64
            "那由他",     // 10 ** 60
            "阿僧祇",     // 10 ** 56
            "恒河沙",     // 10 ** 52
            "极",         // 10 ** 48
            "载",         // 10 ** 44
            "正",         // 10 ** 40
            "涧",         // 10 ** 36
            "沟",         // 10 ** 32
            "穣",         // 10 ** 28
            "秭",         // 10 ** 24
            "垓",         // 10 ** 20
            "京",         // 10 ** 16
            "兆",         // 10 ** 12
            "亿",         // 10 ** 8
            "万",         // 10 ** 4
        ];

        let mut cards = Cards::new();

        // ZH.set_high_numwords: max = 4 * len(high); zip(high, range(max, 0, -4)).
        // 18 words zip exactly against 72,68,…,4.
        let mut n: u32 = 4 * high.len() as u32;
        for word in high.iter() {
            if n == 0 {
                break; // mirrors range(max, 0, -4) exhausting before zip does
            }
            cards.insert(BigInt::from(10u8).pow(n), *word);
            n -= 4;
        }

        set_mid_numwords(&mut cards, &[(1000, "千"), (100, "百"), (10, "十")]);
        // low_numwords[-1] is the tuple ("零","〇"); select_text pins it to
        // "零" for every call the four ported modes make, so store "零".
        set_low_numwords(
            &mut cards,
            &["九", "八", "七", "六", "五", "四", "三", "二", "一", ZERO_WORD],
        );

        // MAXVAL = 1000 * list(self.cards.keys())[0] = 1000 * 10**72 = 10**75.
        let maxval = cards
            .highest()
            .cloned()
            .expect("zh cards are non-empty")
            * BigInt::from(1000);

        LangZh {
            cards,
            maxval,
            // is_title is False for ZH, so exclude_title never gets consulted;
            // carried over for fidelity with setup().
            exclude_title: vec!["负".into(), "点".into()],
        }
    }

    /// `Num2Word_Base.verify_ordinal`. The float check is unreachable for
    /// integer input; only the negative check can fire.
    fn verify_ordinal(&self, value: &BigInt) -> Result<()> {
        if value.is_negative() {
            return Err(N2WError::Type(format!(
                "Cannot treat negative num {} as ordinal.",
                value
            )));
        }
        Ok(())
    }

    /// `zh_to_cap(value, capital=False)`.
    ///
    /// The `capital=True` branch (CAP_map substitution) is unreachable here —
    /// it needs `reading == "capital"`, which only `to_currency` passes. The
    /// `False` branch drops a leading 一 from 一十… so 一十 → 十, 一十二万 → 十二万.
    ///
    /// Python slices `out[len(one):]`, i.e. it strips only `one` and keeps
    /// `ten`. `starts_with(one + ten)` guarantees the prefix, so
    /// `strip_prefix(one)` is the exact equivalent (and stays char-safe).
    fn zh_to_cap(&self, value: &str) -> String {
        let one = self.cards.get(&BigInt::one()).unwrap_or("");
        let ten = self.cards.get(&BigInt::from(10)).unwrap_or("");
        let prefix = format!("{}{}", one, ten);
        if value.starts_with(&prefix) {
            return value.strip_prefix(one).unwrap_or(value).to_string();
        }
        value.to_string()
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
    /// `prefer` can only change the zero card (the sole tuple entry), so the
    /// engine view swaps that one card; `stuff_zero` rides through `merge`;
    /// `reading == "capital"` takes `zh_to_cap`'s CAP_map arm, which — unlike
    /// the plain arm — performs **no** leading-一 strip (11 → "壹拾壹").
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
        let eng = ZhKwEngine {
            base: self,
            cards,
            stuff_zero,
            zero_word: zero,
        };
        let out = default_to_cardinal(&eng, value)?.replace(' ', "");
        Ok(match reading {
            Reading::Capital => apply_cap_map(&out, &ZH_CN_CAP_MAP),
            _ => self.zh_to_cap(&out),
        })
    }
}

impl Lang for LangZh {
    /// `Num2Word_ZH_CN.__class__.__name__`, for the NotImplementedError text.
    fn lang_name(&self) -> &str {
        "Num2Word_ZH_CN"
    }

    /// Port of `Num2Word_ZH.to_currency` under ZH_CN's simplified tables.
    ///
    /// The four ported entry points never pass `reading`/`prefer`, so they
    /// hold their defaults (False/None) throughout — same collapse as the
    /// integer modes. `cents`/`separator`/`adjective` are accepted and
    /// ignored, exactly as Python ignores them ("CURRENCY_ADJECTIVES are not
    /// implemented"; `cents`/`separator` are never read in the body).
    fn to_currency(
        &self,
        val: &CurrencyValue,
        currency: &str,
        _cents: bool,
        _separator: Option<&str>,
        _adjective: bool,
    ) -> Result<String> {
        // parse_currency_parts(val, is_int_with_cents=False): ints keep their
        // magnitude with zero cents; floats quantize to .01 ROUND_HALF_UP.
        let (left, right, is_negative) =
            crate::currency::parse_currency_parts(val, false, false, 100);

        let cr = zh_cn_currency_form(currency).ok_or_else(|| {
            N2WError::NotImplemented(format!(
                "Currency code \"{}\" not implemented for \"{}\"",
                currency,
                self.lang_name()
            ))
        })?;

        // minus_str = self.negword (ZH_CN: 负, no trailing space).
        let minus_str = if is_negative { self.negword() } else { "" };
        let money_str = self.to_cardinal(&left)?;

        // XXX renders bare; every real code prefixes its name and uses 元.
        let (mut out, cr_post) = if currency == "XXX" {
            (String::new(), cr)
        } else {
            (cr.to_string(), "元")
        };

        // to_currency_float(right): "%02d" over the cents, digit + 角/分.
        let cents_num: u32 = right
            .with_scale(0)
            .as_bigint_and_exponent()
            .0
            .to_string()
            .parse()
            .unwrap_or(0);
        let mut cents_parts: Vec<String> = Vec::new();
        if cents_num > 0 {
            let d0 = cents_num / 10;
            let d1 = cents_num % 10;
            // reading != "capital", so the leading zero digit IS emitted.
            cents_parts.push(ZH_DIGITS[d0 as usize].to_string());
            if d0 > 0 {
                cents_parts.push("角".to_string());
            }
            if d1 > 0 {
                cents_parts.push(ZH_DIGITS[d1 as usize].to_string());
                cents_parts.push("分".to_string());
            }
        }
        // cheque suffix "正" only under reading == "capital" — never here.

        // zh_to_cap(select_text(c), capital=False): strip a leading 一 from
        // anything that starts 一十 ("一十二" -> "十二").
        for c in std::iter::once(minus_str.to_string())
            .chain(std::iter::once(money_str))
            .chain(std::iter::once(cr_post.to_string()))
            .chain(cents_parts.into_iter())
        {
            let c = match c.strip_prefix("一十") {
                Some(rest) => format!("十{}", rest),
                None => c,
            };
            out.push_str(&c);
        }
        Ok(out)
    }

    /// `Num2Word_Base.to_cheque` under ZH_CN's single-string CURRENCY_FORMS.
    ///
    /// The base does `cr1, _cr2 = self.CURRENCY_FORMS[currency]` — a tuple
    /// unpack of a *string*, which iterates characters. A 2-char name
    /// ("欧元") unpacks to cr1="欧"; 1 char raises "not enough values to
    /// unpack", 3+ chars "too many values to unpack" — both ValueError,
    /// which the corpus records for CNY (人民币) and CHF (瑞士法郎).
    fn to_cheque(&self, val: &BigDecimal, currency: &str) -> Result<String> {
        let cr = zh_cn_currency_form(currency).ok_or_else(|| {
            N2WError::NotImplemented(format!(
                "Currency code \"{}\" not implemented for \"{}\"",
                currency,
                self.lang_name()
            ))
        })?;
        let nchars = cr.chars().count();
        if nchars != 2 {
            return Err(N2WError::Value(if nchars < 2 {
                format!("not enough values to unpack (expected 2, got {})", nchars)
            } else {
                format!("too many values to unpack (expected 2)")
            }));
        }
        let unit: String = cr.chars().take(1).collect();

        let is_negative = val.sign() == num_bigint::Sign::Minus;
        let abs_val = if is_negative { -val } else { val.clone() };
        let whole = abs_val.with_scale(0).as_bigint_and_exponent().0;
        let sub = ((&abs_val - BigDecimal::from(whole.clone())) * BigDecimal::from(100))
            .with_scale(0)
            .as_bigint_and_exponent()
            .0;
        let words = self.to_cardinal(&whole)?;
        let sign = if is_negative { "MINUS " } else { "" };
        // .upper() is a no-op on Chinese text.
        Ok(format!("{}{} AND {:02}/100 {}", sign, words, sub, unit))
    }

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
        "负"
    }
    fn pointword(&self) -> &str {
        "点"
    }
    fn exclude_title(&self) -> &[String] {
        &self.exclude_title
    }

    /// `Num2Word_ZH.merge`.
    ///
    /// `select_text(ltext)`/`select_text(rtext)` are identity here: by the time
    /// merge runs, both texts are plain `str`s (the only tuple card, 0, is
    /// stored pre-selected as "零"). Shared with the kwargs engine — see
    /// [`zh_merge`] for the verbatim Python body.
    fn merge(&self, l: (&str, &BigInt), r: (&str, &BigInt)) -> (String, BigInt) {
        zh_merge(l, r, STUFF_ZERO as i64, ZERO_WORD)
    }

    /// `Num2Word_ZH.to_cardinal`: run the base engine, strip the spaces the
    /// engine inserts, then `zh_to_cap`.
    fn to_cardinal(&self, value: &BigInt) -> Result<String> {
        let out = default_to_cardinal(self, value)?;
        // super().to_cardinal(value).replace(" ", "") — kills the space the
        // base inserts after negword ("负 一" → "负一").
        let out = out.replace(' ', "");
        Ok(self.zh_to_cap(&out))
    }

    /// `Num2Word_ZH.to_cardinal_float`:
    ///
    /// ```python
    /// def to_cardinal_float(self, value):
    ///     out = super().to_cardinal_float(value).replace(" ", "")
    ///     return self.zh_to_cap(out, self.capital)
    /// ```
    ///
    /// `super().to_cardinal_float` is `Num2Word_Base.to_cardinal_float`
    /// (`default_to_cardinal_float`); its per-part `self.to_cardinal(...)`
    /// calls are ZH's own `to_cardinal`, so each part is already space-free and
    /// `zh_to_cap`-ed. This method then strips the spaces the base joins with
    /// (after negword and around the pointword) and runs `zh_to_cap` once more
    /// over the whole string.
    ///
    /// `self.capital` is always False here: only `to_currency(reading=
    /// "capital")` sets it, and every `to_cardinal` call the base float path
    /// makes runs `set_str_selection(False, ...)` first, resetting it. So
    /// `zh_to_cap` takes its capital=False branch — the one already ported.
    ///
    /// The outer `zh_to_cap` only fires when the *whole* string starts with
    /// 一十, but the inner per-part strip already removed that for positives
    /// ("十二点三四"), and a negative keeps its 一 because the leading 负 pushes
    /// 一十 off the string start ("负一十二点三四"). Reproduced faithfully — the
    /// quirk is the point.
    ///
    /// `precision_override` is dropped, faithfully: ZH forwards `value` only,
    /// and `float2tuple` recomputes `self.precision` from the value regardless,
    /// so Python's `precision=` kwarg is a verified no-op on this path
    /// (`num2words(2.675, lang="zh", precision=5) == "二点六七五"`).
    fn to_cardinal_float(
        &self,
        value: &FloatValue,
        _precision_override: Option<u32>,
    ) -> Result<String> {
        let out = crate::floatpath::default_to_cardinal_float(self, value, None)?;
        // super().to_cardinal_float(value).replace(" ", "")
        let out = out.replace(' ', "");
        Ok(self.zh_to_cap(&out))
    }

    /// `Num2Word_ZH.to_ordinal` with `counter=""` (select_text("") == "").
    fn to_ordinal(&self, value: &BigInt) -> Result<String> {
        self.verify_ordinal(value)?;
        let base = self.to_cardinal(value)?;
        Ok(format!("{}{}", ORD_PREFIX, base))
    }

    /// `Num2Word_ZH.to_ordinal_num`.
    ///
    /// Faithful quirk: unlike `to_ordinal`, this one never calls
    /// `verify_ordinal`, so a negative is formatted rather than rejected —
    /// `to_ordinal_num(-1) == "第-1"`.
    fn to_ordinal_num(&self, value: &BigInt) -> Result<String> {
        Ok(format!("{}{}", ORD_PREFIX, value))
    }

    /// `Num2Word_ZH.to_year`: digit-by-digit, not cardinal.
    ///
    /// The `elif reading == "capital"` prefix branch is unreachable
    /// (`reading` is always False here), so positive years carry no prefix.
    /// Note zh_to_cap is *not* applied, so 10 → "一零年" keeps its 一.
    fn to_year(&self, value: &BigInt) -> Result<String> {
        let mut out = String::new();
        if value.is_negative() {
            out.push_str(YEAR_PREFIX);
            out.push_str(YEAR_BCE);
        }
        // [self.cards[int(s)] for s in str(abs(int(value)))] — digits 0-9 are
        // all present as low numwords, so the lookup cannot miss.
        for ch in value.abs().to_string().chars() {
            let d = BigInt::from(ch.to_digit(10).expect("abs(BigInt) is all digits"));
            out.push_str(self.cards.get(&d).unwrap_or(""));
        }
        out.push_str(YEAR);
        Ok(out)
    }

    // ---- float/Decimal entry routing --------------------------------------

    /// `to_ordinal(float/Decimal)`: `Num2Word_Base.verify_ordinal` runs with
    /// both arms live. Non-whole → TypeError(`errmsg_floatord`) *first*;
    /// whole-but-negative → TypeError(`errmsg_negord`); `-0.0` passes both
    /// (`int(-0.0) == -0.0`, `abs(-0.0) == -0.0`) and renders "第零". A whole
    /// value then takes `to_cardinal`'s integer path, prefixed with 第.
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
                Ok(format!("{}{}", ORD_PREFIX, self.to_cardinal(&i)?))
            }
        }
    }

    /// `to_ordinal_num(float/Decimal)`: no verification at all — Python
    /// interpolates `str(value)` between 第 and the (default-empty) counter,
    /// so "第-0.0", "第0.5", "第1e+16" are all faithful outputs.
    fn ordinal_num_float_entry(&self, _value: &FloatValue, repr_str: &str) -> Result<String> {
        Ok(format!("{}{}", ORD_PREFIX, repr_str))
    }

    /// `to_year(float/Decimal)`: `if not value == int(value)` raises
    /// TypeError(`errmsg_floatyear`); a whole value renders digit-by-digit
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
    /// `verify_ordinal` (negatives raise) then the kwargs cardinal with the
    /// default `stuff_zero=2` — Python forwards only `reading`/`prefer`.
    /// The 第 prefix and the counter are plain `str`s through `select_text`.
    fn to_ordinal_kw(&self, value: &BigInt, kw: &Kwargs) -> Result<String> {
        if !kw.only(&["counter", "reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        let counter = parse_counter(kw)?;
        let prefer = parse_prefer(kw)?;
        let reading = parse_reading(kw);
        self.verify_ordinal(value)?;
        let base = self.kw_cardinal(value, 2, reading, prefer.as_deref())?;
        Ok(format!("{}{}{}", ORD_PREFIX, base, counter))
    }

    /// `to_ordinal_num(value, counter="", reading=False, prefer=None)`:
    /// "第" + `str(value)` + counter. `reading`/`prefer` are inert here —
    /// `select_text` only ever sees the plain strings 第 and the counter —
    /// so they are accepted and ignored, exactly as any value of them is.
    fn to_ordinal_num_kw(&self, value: &BigInt, kw: &Kwargs) -> Result<String> {
        if !kw.only(&["counter", "reading", "prefer"]) {
            return Err(N2WError::Fallback("kwargs".into()));
        }
        let counter = parse_counter(kw)?;
        Ok(format!("{}{}{}", ORD_PREFIX, value, counter))
    }

    /// `to_year(value, reading=False, prefer=None)`. The one kwargs-reachable
    /// branch beyond the defaults: `elif reading == "capital"` prefixes a
    /// positive year with `year_prefix` ("公元一二三四年") — the digits are
    /// *not* CAP-mapped (`to_year` never calls `zh_to_cap`). `prefer` can
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
            out.push_str(YEAR_BCE);
        } else if reading == Reading::Capital {
            out.push_str(select_alt(&YEAR_PREFIX_ALTS, p));
        }
        for ch in value.abs().to_string().chars() {
            let d = ch.to_digit(10).expect("abs(BigInt) is all digits") as usize;
            if d == 0 {
                out.push_str(select_alt(&ZERO_ALTS, p));
            } else {
                out.push_str(ZH_DIGITS[d]);
            }
        }
        out.push_str(YEAR);
        Ok(out)
    }

    /// `to_currency(val, currency="XXX", ..., reading=False, prefer=None)`
    /// with the reading/prefer kwargs live. Every component (minus, money,
    /// the closing 元, each cents word, the cheque suffix) runs through
    /// `zh_to_cap(select_text(c), capital)`; under capital that CAP-maps
    /// (元 → 圆) and appends 正 when there are no cents — ZH_CN's CAP_map has
    /// no ("正", "整") row, so the suffix stays 正 ("零圆正"). The leading
    /// zero cents digit is *skipped* under capital (`not (int(cents[0]) == 0
    /// and reading == "capital")`).
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

        let (left, right, is_negative) =
            crate::currency::parse_currency_parts(val, false, false, 100);
        let cr = zh_cn_currency_form(currency).ok_or_else(|| {
            N2WError::NotImplemented(format!(
                "Currency code \"{}\" not implemented for \"{}\"",
                currency,
                self.lang_name()
            ))
        })?;

        let minus_str = if is_negative {
            self.negword().to_string()
        } else {
            String::new()
        };
        let money_str = self.kw_cardinal(&left, 2, reading, p)?;
        let (mut out, cr_post) = if currency == "XXX" {
            (String::new(), cr)
        } else {
            (cr.to_string(), "元")
        };

        let cents_num: u32 = right
            .with_scale(0)
            .as_bigint_and_exponent()
            .0
            .to_string()
            .parse()
            .unwrap_or(0);
        let digit = |d: u32| -> String {
            if d == 0 {
                select_alt(&ZERO_ALTS, p).to_string()
            } else {
                ZH_DIGITS[d as usize].to_string()
            }
        };
        let mut cents_parts: Vec<String> = Vec::new();
        if cents_num > 0 {
            let d0 = cents_num / 10;
            let d1 = cents_num % 10;
            if !(d0 == 0 && capital) {
                cents_parts.push(digit(d0));
            }
            if d0 > 0 {
                cents_parts.push("角".to_string());
            }
            if d1 > 0 {
                cents_parts.push(digit(d1));
                cents_parts.push("分".to_string());
            }
        }
        // cheque_suffix "正" — only in capital readings with no cents.
        let cheque = if cents_parts.is_empty() && capital {
            "正".to_string()
        } else {
            String::new()
        };

        for c in std::iter::once(minus_str)
            .chain(std::iter::once(money_str))
            .chain(std::iter::once(cr_post.to_string()))
            .chain(cents_parts)
            .chain(std::iter::once(cheque))
        {
            let piece = if capital {
                apply_cap_map(&c, &ZH_CN_CAP_MAP)
            } else {
                self.zh_to_cap(&c)
            };
            out.push_str(&piece);
        }
        Ok(out)
    }

    /// `to_cardinal(float/Decimal, stuff_zero, reading, prefer)`.
    ///
    /// A *whole* value passes base's `assert int(value) == value` and runs
    /// the integer engine with the kwargs still live — identical to the int
    /// path. A fractional value goes through `to_cardinal_float`, whose
    /// inner `self.to_cardinal(part)` calls re-run `set_str_selection(False,
    /// None)` / `self.stuff_zero = 2` for every part, resetting everything —
    /// the only survivor is the caller's final `zh_to_cap(out, reading ==
    /// "capital")`, applied over the already-assembled plain string (so
    /// `12.34` capital reads "拾贰点叁肆": the inner strip already ate the 壹).
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
            Reading::Capital => apply_cap_map(&out, &ZH_CN_CAP_MAP),
            _ => self.zh_to_cap(&out),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use bigdecimal::BigDecimal;
    use std::str::FromStr;

    /// `precision` is what the Python shim derives from `repr(value)`.
    fn f(lang: &LangZh, value: f64, precision: u32) -> String {
        lang.to_cardinal_float(&FloatValue::Float { value, precision }, None)
            .unwrap()
    }

    fn d(lang: &LangZh, lit: &str, precision: u32) -> String {
        lang.to_cardinal_float(
            &FloatValue::Decimal {
                value: BigDecimal::from_str(lit).unwrap(),
                precision,
            },
            None,
        )
        .unwrap()
    }

    /// The float `to: "cardinal"` rows of the frozen `zh` corpus.
    #[test]
    fn corpus_float_rows() {
        let l = LangZh::new();
        assert_eq!(f(&l, 0.5, 1), "零点五");
        assert_eq!(f(&l, 1.5, 1), "一点五");
        assert_eq!(f(&l, 2.25, 2), "二点二五");
        assert_eq!(f(&l, 3.14, 2), "三点一四");
        assert_eq!(f(&l, 0.01, 2), "零点零一");
        assert_eq!(f(&l, 0.1, 1), "零点一");
        assert_eq!(f(&l, 0.99, 2), "零点九九");
        assert_eq!(f(&l, 1.01, 2), "一点零一");
        // 12 alone strips its leading 一 (十二); the pre part is rendered
        // through ZH.to_cardinal, so the float form inherits the strip.
        assert_eq!(f(&l, 12.34, 2), "十二点三四");
        assert_eq!(f(&l, 99.99, 2), "九十九点九九");
        assert_eq!(f(&l, 100.5, 1), "一百点五");
        assert_eq!(f(&l, 1234.56, 2), "一千二百三十四点五六");
        // int(-0.5) == 0 carries no minus, so base re-attaches negword.
        assert_eq!(f(&l, -0.5, 1), "负零点五");
        assert_eq!(f(&l, -1.5, 1), "负一点五");
        // A negative keeps its 一: the leading 负 pushes 一十 off the string
        // start, so neither the inner nor the outer zh_to_cap fires.
        assert_eq!(f(&l, -12.34, 2), "负一十二点三四");
        // f64-artefact cases: 1.005*1000 → 4.999999999999893 and
        // 2.675*1000 → 674.9999999999998, both rescued by the < 0.01 rule.
        assert_eq!(f(&l, 1.005, 3), "一点零零五");
        assert_eq!(f(&l, 2.675, 3), "二点六七五");
    }

    /// The `to: "cardinal_dec"` rows — Decimal stays exact (issue #603).
    #[test]
    fn corpus_decimal_rows() {
        let l = LangZh::new();
        assert_eq!(d(&l, "0.01", 2), "零点零一");
        // Trailing zero is preserved: post "10" padded to precision 2.
        assert_eq!(d(&l, "1.10", 2), "一点一零");
        assert_eq!(d(&l, "12.345", 3), "十二点三四五");
        // Trillion-scale Decimal keeps .99 exactly — no float cast.
        assert_eq!(
            d(&l, "98746251323029.99", 2),
            "九十八兆七千四百六十二亿五千一百三十二万三千零二十九点九九"
        );
        assert_eq!(d(&l, "0.001", 3), "零点零零一");
    }

    /// Live-interpreter checks beyond the corpus.
    #[test]
    fn live_interpreter_extras() {
        let l = LangZh::new();
        // The same value as a float rounds to .984375 → floor → 98, matching
        // repr(-98746251323029.99) == '-98746251323029.98' (issue #603's bug,
        // reproduced): 负…零二十九点九八.
        assert_eq!(
            f(&l, -98746251323029.99, 2),
            "负九十八兆七千四百六十二亿五千一百三十二万三千零二十九点九八"
        );
        // precision= is a verified no-op on ZH's float path: float2tuple
        // recomputes self.precision from the value regardless.
        assert_eq!(
            l.to_cardinal_float(
                &FloatValue::Float {
                    value: 2.675,
                    precision: 3
                },
                Some(5),
            )
            .unwrap(),
            "二点六七五"
        );
    }
}

/// `Num2Word_ZH_CN.CURRENCY_FORMS` — simplified names, single strings.
fn zh_cn_currency_form(code: &str) -> Option<&'static str> {
    Some(match code {
        "XXX" => "元",
        "CNY" => "人民币",
        "NTD" => "新台币",
        "HKD" => "港币",
        "MOP" => "澳门币",
        "SGD" => "新加坡元",
        "MYR" => "马来西亚令吉",
        "USD" => "美元",
        "EUR" => "欧元",
        "GBP" => "英镑",
        "JPY" => "日元",
        "CHF" => "瑞士法郎",
        "CAD" => "加元",
        "AUD" => "澳币",
        "NZD" => "纽西兰元",
        "THB" => "泰铢",
        "KRW" => "韩元",
        _ => return None,
    })
}

/// Digits 0-9 as `select_text(self.cards[d])` yields them with
/// reading=False/prefer=None — first form of the ("零","〇") tuple, plain
/// glyphs elsewhere (identical in both scripts).
const ZH_DIGITS: [&str; 10] = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"];
