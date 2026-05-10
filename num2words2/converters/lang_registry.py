"""Per-language surface-form registry for SentenceConverter.

Drives ordinal detection, date parsing, temperature parsing, and
negative-word selection across every language with a well-defined
ordinal/date written form.

Surface forms compiled from official orthography references and
established corpus practice. Languages without an unambiguous written
ordinal form (e.g. some bare-form scripts) are intentionally absent —
contributors should add them with a citation.
"""
from __future__ import annotations

import re
from typing import Optional


# ---------------------------------------------------------------------------
# Ordinal surface forms.
#
# Pattern must capture the integer in group(1). The overall match consumes
# the integer + the ordinal suffix so the SentenceConverter can replace
# the whole span with the spelled-out ordinal.
# ---------------------------------------------------------------------------
ORDINAL_PATTERNS: dict[str, str] = {
    # Germanic
    "en": r"(\d+)(?:st|nd|rd|th)\b",
    "de": r"(\d+)(?:te[rnms]?|\.)",
    "nl": r"(\d+)(?:ste|de|e)\b",
    "sv": r"(\d+):(?:a|e)\b",
    "da": r"(\d+)\.",
    "no": r"(\d+)\.",
    "is": r"(\d+)\.",
    "af": r"(\d+)(?:ste|de)\b",

    # Romance
    "fr": r"(\d+)(?:ers?|ères?|res?|èmes?|emes?|es?)\b",
    "es": r"(\d+)(?:º|ª|°)",
    "pt": r"(\d+)(?:º|ª|°)",
    "it": r"(\d+)(?:º|ª|°)",
    "ro": r"(\d+)(?:[-‐](?:l?ea|a))\b",
    "ca": r"(\d+)(?:r|n|t|è|a)\b",
    "rm": r"(\d+)(?:avel|evel)\b",

    # Slavic
    "ru": r"(\d+)[-‐](?:й|я|е|ое|ой|го|му|ый|ии)\b",
    "uk": r"(\d+)[-‐](?:й|а|е|ий|ого)\b",
    "be": r"(\d+)[-‐](?:ы|і|я|е)\b",
    "bg": r"(\d+)[-‐](?:ти|ри|ви|ма|и)\b",
    "pl": r"(\d+)\.",
    "cs": r"(\d+)\.",
    "sk": r"(\d+)\.",
    "sl": r"(\d+)\.",
    "hr": r"(\d+)\.",
    "sr": r"(\d+)\.",
    "mk": r"(\d+)[-‐](?:ти|ри|ви|ма)\b",

    # Baltic
    "lt": r"(\d+)[-‐](?:as|oji|asis|toji)\b",
    "lv": r"(\d+)\.",
    "et": r"(\d+)\.",

    # Greek
    "el": r"(\d+)(?:ος|η|ο|ός)\b",

    # Finno-Ugric
    "fi": r"(\d+)\.",
    "hu": r"(\d+)\.",

    # Turkic / Caucasian
    "tr": r"(\d+)(?:\.|inci|ıncı|uncu|üncü)\b",
    "az": r"(\d+)[-‐](?:ci|cu|cü|cı)\b",

    # Semitic
    "ar": r"(\d+)\b",  # Arabic: dot suffix or none; conservative match
    "he": r"(\d+)\b",  # Hebrew: ordinal often left as digit + context

    # Indo-Aryan / Dravidian
    "hi": r"(\d+)(?:वां|वीं|वें)\b",
    "bn": r"(\d+)(?:তম|ম|য়|র্থ)\b",
    "ta": r"(\d+)(?:வது|ஆம்)\b",
    "te": r"(\d+)(?:వ)\b",

    # Iranian
    "fa": r"(\d+)(?:م|مین|ام)\b",

    # CJK
    "zh": r"第(\d+)",
    "ja": r"第(\d+)|(\d+)番目",
    "ko": r"제(\d+)|(\d+)번째",

    # Vietnamese
    "vi": r"thứ\s*(\d+)",

    # Thai
    "th": r"ที่\s*(\d+)",

    # Indonesian / Malay (shared "ke-" prefix)
    "id": r"ke[-‐](\d+)",
    "ms": r"ke[-‐](\d+)",

    # Esperanto / Interlingua / Latin
    "eo": r"(\d+)\.?-?a\b",
    "ia": r"(\d+)me\b",
    "la": r"(\d+)\.",
}


# ---------------------------------------------------------------------------
# Month-name regex per language. Captured in a non-capturing group.
# Used by date_patterns to find "<day> <month>" / "<month> <day>" spans.
#
# Patterns are case-insensitive; the SentenceConverter applies re.IGNORECASE.
# ---------------------------------------------------------------------------
MONTH_NAMES: dict[str, str] = {
    "en": (
        r"(?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|"
        r"Oct|Nov|Dec)"
    ),
    "fr": (
        r"(?:janvier|f[ée]vrier|mars|avril|mai|juin|juillet|ao[uû]t|"
        r"septembre|octobre|novembre|d[ée]cembre)"
    ),
    "es": (
        r"(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
        r"septiembre|octubre|noviembre|diciembre)"
    ),
    "pt": (
        r"(?:janeiro|fevereiro|mar[çc]o|abril|maio|junho|julho|agosto|"
        r"setembro|outubro|novembro|dezembro)"
    ),
    "it": (
        r"(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|"
        r"settembre|ottobre|novembre|dicembre)"
    ),
    "de": (
        r"(?:Januar|Februar|M[äa]rz|April|Mai|Juni|Juli|August|"
        r"September|Oktober|November|Dezember|J[äa]nner)"
    ),
    "nl": (
        r"(?:januari|februari|maart|april|mei|juni|juli|augustus|"
        r"september|oktober|november|december)"
    ),
    "sv": (
        r"(?:januari|februari|mars|april|maj|juni|juli|augusti|"
        r"september|oktober|november|december)"
    ),
    "da": (
        r"(?:januar|februar|marts|april|maj|juni|juli|august|"
        r"september|oktober|november|december)"
    ),
    "no": (
        r"(?:januar|februar|mars|april|mai|juni|juli|august|"
        r"september|oktober|november|desember)"
    ),
    "fi": (
        r"(?:tammikuu(?:ta)?|helmikuu(?:ta)?|maaliskuu(?:ta)?|"
        r"huhtikuu(?:ta)?|toukokuu(?:ta)?|kes[äa]kuu(?:ta)?|"
        r"hein[äa]kuu(?:ta)?|elokuu(?:ta)?|syyskuu(?:ta)?|"
        r"lokakuu(?:ta)?|marraskuu(?:ta)?|joulukuu(?:ta)?)"
    ),
    "is": (
        r"(?:jan[úu]ar|febr[úu]ar|mars|apr[íi]l|ma[íi]|j[úu]n[íi]|"
        r"j[úu]l[íi]|[áa]g[úu]st|september|okt[óo]ber|n[óo]vember|"
        r"desember)"
    ),
    "ru": (
        r"(?:январ[ьея]|феврал[ьея]|март[а]?|апрел[ьея]|ма[йяе]|"
        r"июн[ьея]|июл[ьея]|август[а]?|сентябр[ьея]|октябр[ьея]|"
        r"ноябр[ьея]|декабр[ьея])"
    ),
    "uk": (
        r"(?:січн[яеі]|лют[ого]|березн[яе]|квітн[яе]|травн[яе]|"
        r"червн[яе]|липн[яе]|серпн[яе]|вересн[яе]|жовтн[яе]|"
        r"листопад[а]?|грудн[яе])"
    ),
    "pl": (
        r"(?:styczni[ae]|luty|lutego|marzec|marca|kwiecie[nń]|"
        r"kwietnia|maj[a]?|czerwiec|czerwca|lipiec|lipca|sierpie[nń]|"
        r"sierpnia|wrzesie[nń]|wrze[śs]nia|pa[źz]dziernik[a]?|"
        r"listopad[a]?|grudzie[nń]|grudnia)"
    ),
    "cs": (
        r"(?:ledn[aue]|[úu]nor[a]?|b[řr]ezn[aue]|duben|dubna|kv[ěe]ten|"
        r"kv[ěe]tna|[čc]erven[ae]?|[čc]ervna|[čc]ervenec|[čc]ervence|"
        r"srpen|srpna|z[áa][řr][íi]|[řr][íi]jen|[řr][íi]jna|listopad[au]?|"
        r"prosinec|prosince)"
    ),
    "sk": (
        r"(?:janu[áa]r[a]?|febru[áa]r[a]?|marec|marca|apr[íi]l[a]?|"
        r"m[áa]j[a]?|j[úu]n[a]?|j[úu]l[a]?|august[a]?|september|"
        r"septembra|okt[óo]ber|okt[óo]bra|november|novembra|"
        r"december|decembra)"
    ),
    "ro": (
        r"(?:ianuarie|februarie|martie|aprilie|mai|iunie|iulie|"
        r"august|septembrie|octombrie|noiembrie|decembrie)"
    ),
    "el": (
        r"(?:Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Ιουνίου|"
        r"Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|"
        r"Δεκεμβρίου|Ιανουάριος|Φεβρουάριος|Μάρτιος|Απρίλιος|Μάιος|"
        r"Ιούνιος|Ιούλιος|Αύγουστος|Σεπτέμβριος|Οκτώβριος|"
        r"Νοέμβριος|Δεκέμβριος)"
    ),
    "tr": (
        r"(?:Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|"
        r"Eylül|Ekim|Kasım|Aralık)"
    ),
    "hu": (
        r"(?:janu[áa]r|febru[áa]r|m[áa]rcius|[áa]prilis|m[áa]jus|"
        r"j[úu]nius|j[úu]lius|augusztus|szeptember|okt[óo]ber|"
        r"november|december)"
    ),
    "ar": (
        r"(?:يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|"
        r"سبتمبر|أكتوبر|نوفمبر|ديسمبر|كانون|شباط|آذار|نيسان|"
        r"أيار|حزيران|تموز|آب|أيلول|تشرين|تشرين)"
    ),
    "he": (
        r"(?:ינואר|פברואר|מרץ|אפריל|מאי|יוני|יולי|אוגוסט|"
        r"ספטמבר|אוקטובר|נובמבר|דצמבר)"
    ),
    "ja": (
        r"(?:1月|2月|3月|4月|5月|6月|7月|8月|9月|10月|11月|12月|"
        r"睦月|如月|弥生|卯月|皐月|水無月|文月|葉月|長月|神無月|霜月|師走)"
    ),
    "ko": (
        r"(?:1월|2월|3월|4월|5월|6월|7월|8월|9월|10월|11월|12월)"
    ),
    "zh": (
        r"(?:1月|2月|3月|4月|5月|6月|7月|8月|9月|10月|11月|12月|"
        r"一月|二月|三月|四月|五月|六月|七月|八月|九月|十月|十一月|十二月)"
    ),
    "vi": (
        r"(?:th[áa]ng\s*(?:m[ộo]t|hai|ba|b[ốo]n|n[ăa]m|s[áa]u|b[ảa]y|"
        r"t[áa]m|ch[íi]n|m[ưu][ờo]i|m[ưu][ờo]i\s*m[ộo]t|"
        r"m[ưu][ờo]i\s*hai|\d+))"
    ),
    "th": (
        r"(?:มกราคม|กุมภาพันธ์|มีนาคม|เมษายน|พฤษภาคม|มิถุนายน|"
        r"กรกฎาคม|สิงหาคม|กันยายน|ตุลาคม|พฤศจิกายน|ธันวาคม)"
    ),
    "id": (
        r"(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|"
        r"September|Oktober|November|Desember)"
    ),
    "ms": (
        r"(?:Januari|Februari|Mac|April|Mei|Jun|Julai|Ogos|"
        r"September|Oktober|November|Disember)"
    ),
    "hi": (
        r"(?:जनवरी|फ़रवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|"
        r"अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर)"
    ),
    "bn": (
        r"(?:জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|মে|জুন|"
        r"জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর)"
    ),
    "fa": (
        r"(?:ژانویه|فوریه|مارس|آوریل|می|ژوئن|ژوئیه|اوت|"
        r"سپتامبر|اکتبر|نوامبر|دسامبر|فروردین|اردیبهشت|خرداد|"
        r"تیر|مرداد|شهریور|مهر|آبان|آذر|دی|بهمن|اسفند)"
    ),
}


# ---------------------------------------------------------------------------
# Date-pattern templates. A list of (pattern_template, is_ordinal) entries.
#
# {month} placeholder is substituted with MONTH_NAMES[lang] if available.
# is_ordinal=True means the day number should be spelled as an ordinal in
# the target language; False means it stays cardinal.
# ---------------------------------------------------------------------------
DATE_PATTERNS_TEMPLATE: dict[str, list[tuple[str, bool]]] = {
    "en": [
        (r"(\d+)(?:st|nd|rd|th)\s+({month})", True),
        (r"({month})\s+(\d+)(?:st|nd|rd|th)?", True),  # "December 5" / "December 5th"
        (r"(\d+)\s+({month})", True),  # "5 December"
    ],
    "fr": [
        (r"(\d+)(?:er|ère|e|ème)?\s+({month})", True),  # "1er mai", "5 mai"
    ],
    "es": [
        (r"(\d+)\s+de\s+({month})", False),  # "5 de mayo"
    ],
    "pt": [
        (r"(\d+)\s+de\s+({month})", False),
    ],
    "it": [
        (r"(\d+)\s+({month})", False),
    ],
    "de": [
        (r"(\d+)\.\s+({month})", True),  # "5. März"
        (r"(\d+)\s+({month})", True),
    ],
    "nl": [
        (r"(\d+)\s+({month})", True),  # "5 mei"
    ],
    "sv": [
        (r"(\d+)\s+({month})", True),
    ],
    "da": [
        (r"(\d+)\.\s+({month})", True),
    ],
    "no": [
        (r"(\d+)\.\s+({month})", True),
    ],
    "fi": [
        (r"(\d+)\.\s+({month})", True),
    ],
    "ru": [
        (r"(\d+)\s+({month})", False),
    ],
    "uk": [
        (r"(\d+)\s+({month})", False),
    ],
    "pl": [
        (r"(\d+)\s+({month})", False),
    ],
    "cs": [
        (r"(\d+)\.\s+({month})", True),
    ],
    "sk": [
        (r"(\d+)\.\s+({month})", True),
    ],
    "ro": [
        (r"(\d+)\s+({month})", False),
    ],
    "el": [
        (r"(\d+)\s+({month})", False),
    ],
    "tr": [
        (r"(\d+)\s+({month})", False),
    ],
    "hu": [
        (r"({month})\s+(\d+)\.?", True),  # "május 5." (Hungarian ordinal-after-month)
    ],
    "ar": [
        (r"(\d+)\s+({month})", False),
    ],
    "he": [
        (r"(\d+)\s+({month})", False),
    ],
    "ja": [
        (r"({month})\s*(\d+)日", False),  # "5月3日" form
        (r"(\d+)月\s*(\d+)日", False),
    ],
    "zh": [
        (r"({month})\s*(\d+)日?", False),
        (r"(\d+)月\s*(\d+)日?", False),
    ],
    "ko": [
        (r"({month})\s*(\d+)일", False),
    ],
    "vi": [
        (r"(\d+)\s+({month})", False),
    ],
    "th": [
        (r"(\d+)\s+({month})", False),
    ],
    "id": [
        (r"(\d+)\s+({month})", False),
    ],
    "ms": [
        (r"(\d+)\s+({month})", False),
    ],
    "hi": [
        (r"(\d+)\s+({month})", False),
    ],
    "bn": [
        (r"(\d+)\s+({month})", False),
    ],
    "fa": [
        (r"(\d+)\s+({month})", False),
    ],
}


# ---------------------------------------------------------------------------
# Temperature patterns. Tuple: (regex, scale_word, scale_unit_for_speech).
#
# regex captures the value in group(1). scale_word and scale_unit are kept
# as plain strings to let the SentenceConverter render natural speech
# without re-deriving them.
# ---------------------------------------------------------------------------
TEMP_PATTERNS: dict[str, tuple[str, str, str]] = {
    "en": (
        r"(-?\d+(?:[.,]\d+)?)\s+degrees?(?:\s+[Ff]ahrenheit|\s+[Cc]elsius)?",
        "degrees", "Fahrenheit",
    ),
    "fr": (
        r"(-?\d+(?:[.,]\d+)?)\s+degr[ée]s?(?:\s+[Cc]elsius)?",
        "degrés", "Celsius",
    ),
    "es": (
        r"(-?\d+(?:[.,]\d+)?)\s+grados?(?:\s+[Cc]elsius)?",
        "grados", "Celsius",
    ),
    "pt": (
        r"(-?\d+(?:[.,]\d+)?)\s+graus?(?:\s+[Cc]elsius)?",
        "graus", "Celsius",
    ),
    "it": (
        r"(-?\d+(?:[.,]\d+)?)\s+gradi?(?:\s+[Cc]elsius)?",
        "gradi", "Celsius",
    ),
    "de": (
        r"(-?\d+(?:[.,]\d+)?)\s+[Gg]rad(?:\s+[Cc]elsius)?",
        "Grad", "Celsius",
    ),
    "nl": (
        r"(-?\d+(?:[.,]\d+)?)\s+graden?(?:\s+[Cc]elsius)?",
        "graden", "Celsius",
    ),
    "sv": (
        r"(-?\d+(?:[.,]\d+)?)\s+grader?(?:\s+[Cc]elsius)?",
        "grader", "Celsius",
    ),
    "da": (
        r"(-?\d+(?:[.,]\d+)?)\s+grader?(?:\s+[Cc]elsius)?",
        "grader", "Celsius",
    ),
    "no": (
        r"(-?\d+(?:[.,]\d+)?)\s+grader?(?:\s+[Cc]elsius)?",
        "grader", "Celsius",
    ),
    "fi": (
        r"(-?\d+(?:[.,]\d+)?)\s+astetta?(?:\s+[Cc]elsiusta)?",
        "astetta", "Celsius",
    ),
    "ru": (
        r"(-?\d+(?:[.,]\d+)?)\s+градус(?:а|ов)?",
        "градусов", "Цельсия",
    ),
    "uk": (
        r"(-?\d+(?:[.,]\d+)?)\s+градус(?:а|ів)?",
        "градусів", "Цельсія",
    ),
    "pl": (
        r"(-?\d+(?:[.,]\d+)?)\s+stopni(?:e|i)?",
        "stopni", "Celsjusza",
    ),
    "cs": (
        r"(-?\d+(?:[.,]\d+)?)\s+stup(?:ňů|eň|ně)",
        "stupňů", "Celsia",
    ),
    "tr": (
        r"(-?\d+(?:[.,]\d+)?)\s+derece",
        "derece", "santigrat",
    ),
    "ja": (
        r"(-?\d+(?:[.,]\d+)?)\s*度",
        "度", "摂氏",
    ),
    "zh": (
        r"(-?\d+(?:[.,]\d+)?)\s*度",
        "度", "摄氏",
    ),
    "ko": (
        r"(-?\d+(?:[.,]\d+)?)\s*도",
        "도", "섭씨",
    ),
    "el": (
        r"(-?\d+(?:[.,]\d+)?)\s+βαθμο[ίυ]?ς?",
        "βαθμοί", "Κελσίου",
    ),
    "ar": (
        r"(-?\d+(?:[.,]\d+)?)\s+درجة",
        "درجة", "مئوية",
    ),
    "hi": (
        r"(-?\d+(?:[.,]\d+)?)\s+डिग्री",
        "डिग्री", "सेल्सियस",
    ),
}


# ---------------------------------------------------------------------------
# Negative-marker word per language. Used when the SentenceConverter
# encounters a negative number in a numeric context.
# ---------------------------------------------------------------------------
NEGATIVE_WORDS: dict[str, str] = {
    "en": "minus", "fr": "moins", "es": "menos", "it": "meno",
    "pt": "menos", "de": "minus", "nl": "min", "sv": "minus",
    "da": "minus", "no": "minus", "is": "mínus", "fi": "miinus",
    "et": "miinus", "lt": "minus", "lv": "mīnus",
    "ru": "минус", "uk": "мінус", "be": "мінус", "bg": "минус",
    "pl": "minus", "cs": "mínus", "sk": "mínus", "sl": "minus",
    "hr": "minus", "sr": "минус", "mk": "минус",
    "el": "πλην", "ro": "minus", "hu": "mínusz", "tr": "eksi",
    "az": "mənfi",
    "ar": "سالب", "he": "מינוס", "fa": "منفی",
    "hi": "माइनस", "bn": "মাইনাস", "ta": "மைனஸ்", "te": "మైనస్",
    "ja": "マイナス", "zh": "负", "zh-cn": "负", "ko": "마이너스",
    "vi": "âm", "th": "ติดลบ",
    "id": "minus", "ms": "minus",
    "eo": "minus", "la": "minus", "rm": "minus",
}


# ---------------------------------------------------------------------------
# Public helpers.
# ---------------------------------------------------------------------------
def get_ordinal_pattern(lang: str) -> Optional[str]:
    """Return the compiled-string ordinal regex for `lang`, or None."""
    return ORDINAL_PATTERNS.get(_norm_lang(lang))


def get_date_patterns(lang: str) -> list[tuple[str, bool]]:
    """Return concrete date regex patterns for `lang` with month names
    substituted in. Empty list when the language has no entry.

    Month-name substitution is wrapped in word boundaries so a short month
    abbreviation (e.g. EN "Mar") never partial-matches an unrelated word
    (e.g. "marks").
    """
    nlang = _norm_lang(lang)
    months = MONTH_NAMES.get(nlang)
    templates = DATE_PATTERNS_TEMPLATE.get(nlang, [])
    if not months:
        return []
    bounded_months = r"\b" + months + r"\b"
    return [(tpl.replace("{month}", bounded_months), is_ord) for tpl, is_ord in templates]


def get_month_names(lang: str) -> Optional[str]:
    """Return month-name regex for `lang`, or None."""
    return MONTH_NAMES.get(_norm_lang(lang))


def get_temp_pattern(lang: str) -> Optional[tuple[str, str, str]]:
    """Return temperature regex tuple for `lang`, or None."""
    return TEMP_PATTERNS.get(_norm_lang(lang))


def get_negative_word(lang: str) -> str:
    """Return the negative-marker word for `lang`, falling back to 'minus'."""
    return NEGATIVE_WORDS.get(_norm_lang(lang), "minus")


def supported_languages() -> set[str]:
    """All languages with at least an ordinal pattern registered."""
    return set(ORDINAL_PATTERNS.keys())


def _norm_lang(lang: str) -> str:
    if not lang:
        return "en"
    lang = lang.lower().strip()
    if lang in ORDINAL_PATTERNS or lang in NEGATIVE_WORDS:
        return lang
    base = lang.split("-")[0].split("_")[0]
    return base
