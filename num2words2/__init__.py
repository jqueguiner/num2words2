# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals

import decimal

from . import (
    lang_AF,
    lang_AM,
    lang_AR,
    lang_AS,
    lang_AZ,
    lang_BA,
    lang_BAN,
    lang_BE,
    lang_BG,
    lang_BM,
    lang_BN,
    lang_BO,
    lang_BR,
    lang_BS,
    lang_CA,
    lang_CE,
    lang_CEB,
    lang_CKB,
    lang_CNH,
    lang_CS,
    lang_CY,
    lang_DA,
    lang_DE,
    lang_DV,
    lang_EL,
    lang_EN,
    lang_EN_IN,
    lang_EN_NE,
    lang_EN_NG,
    lang_EN_NP,
    lang_EO,
    lang_ES,
    lang_ES_CO,
    lang_ES_CR,
    lang_ES_GT,
    lang_ES_HN,
    lang_ES_NI,
    lang_ES_VE,
    lang_ET,
    lang_EU,
    lang_FA,
    lang_FF,
    lang_FI,
    lang_FIL,
    lang_FO,
    lang_FR,
    lang_FR_BE,
    lang_FR_CH,
    lang_FR_DZ,
    lang_GL,
    lang_GU,
    lang_HA,
    lang_HAW,
    lang_HE,
    lang_HI,
    lang_HMN,
    lang_HR,
    lang_HT,
    lang_HU,
    lang_HY,
    lang_ID,
    lang_IS,
    lang_IT,
    lang_JA,
    lang_JW,
    lang_KA,
    lang_KI,
    lang_KK,
    lang_KM,
    lang_KN,
    lang_KO,
    lang_KOK,
    lang_KSW,
    lang_KU,
    lang_KY,
    lang_KZ,
    lang_LA,
    lang_LB,
    lang_LG,
    lang_LIJ,
    lang_LN,
    lang_LO,
    lang_LT,
    lang_LUS,
    lang_LV,
    lang_MG,
    lang_MI,
    lang_MK,
    lang_ML,
    lang_MN,
    lang_MR,
    lang_MS,
    lang_MT,
    lang_MY,
    lang_NE,
    lang_NL,
    lang_NN,
    lang_NO,
    lang_OC,
    lang_OM,
    lang_OR,
    lang_PA,
    lang_PAP,
    lang_PL,
    lang_PLI,
    lang_PS,
    lang_PT,
    lang_PT_BR,
    lang_RM,
    lang_RM_PUTER,
    lang_RM_SURMIRAN,
    lang_RM_SURSILV,
    lang_RM_SUTSILV,
    lang_RM_VALLADER,
    lang_RO,
    lang_RU,
    lang_RW,
    lang_SA,
    lang_SD,
    lang_SI,
    lang_SK,
    lang_SL,
    lang_SN,
    lang_SO,
    lang_SQ,
    lang_SR,
    lang_SR_LATN,
    lang_SU,
    lang_SV,
    lang_SW,
    lang_TA,
    lang_TE,
    lang_TET,
    lang_TG,
    lang_TH,
    lang_TI,
    lang_TK,
    lang_TL,
    lang_TR,
    lang_TT,
    lang_UK,
    lang_UR,
    lang_UZ,
    lang_UZ_CYR,
    lang_VI,
    lang_WO,
    lang_XH,
    lang_YI,
    lang_YO,
    lang_ZH_CN,
    lang_ZH_HK,
    lang_ZH_TW,
    lang_ZU,
)
from .grouping import group_digits  # noqa: E402

# Version information
try:
    from ._version import __version__, __version_tuple__
except ImportError:
    # Package is not installed, provide defaults
    __version__ = "unknown"
    __version_tuple__ = (0, 0, 0, "unknown", 0)


def maxval(lang="en"):
    """Return the maximum integer ``num2words(..., lang=lang)`` can convert.

    Issue #582 ports savoirfairelinux/num2words#582. Useful for input
    validation in apps that need to know the per-language ceiling before
    calling :func:`num2words`.
    """
    if lang not in CONVERTER_CLASSES:
        # Reuse the same prefix-fallback the dispatcher does so callers
        # don't have to know the canonical key.
        nl = lang.replace("-", "_")
        if nl in CONVERTER_CLASSES:
            lang = nl
        elif nl[:2] in CONVERTER_CLASSES:
            lang = nl[:2]
        else:
            raise NotImplementedError("No MAXVAL for lang=%r" % lang)
    converter = CONVERTER_CLASSES[lang]
    return getattr(converter, "MAXVAL", None)


# Export main functions
__all__ = [
    "num2words",
    "num2words_sentence",
    "convert_sentence",
    "sentence_to_words",
    "group_digits",
    "maxval",
]


CONVERTER_CLASSES = {
    "af": lang_AF.Num2Word_AF(),
    "am": lang_AM.Num2Word_AM(),
    "ar": lang_AR.Num2Word_AR(),
    "az": lang_AZ.Num2Word_AZ(),
    "be": lang_BE.Num2Word_BE(),
    "bg": lang_BG.Num2Word_BG(),
    "bn": lang_BN.Num2Word_BN(),
    "ca": lang_CA.Num2Word_CA(),
    "ce": lang_CE.Num2Word_CE(),
    "cs": lang_CS.Num2Word_CS(),
    "cy": lang_CY.Num2Word_CY(),
    "da": lang_DA.Num2Word_DA(),
    "de": lang_DE.Num2Word_DE(),
    "dv": lang_DV.Num2Word_DV(),
    "el": lang_EL.Num2Word_EL(),
    "en": lang_EN.Num2Word_EN(),
    "en_IN": lang_EN_IN.Num2Word_EN_IN(),
    "en_NE": lang_EN_NE.Num2Word_EN_NE(),
    "en_NG": lang_EN_NG.Num2Word_EN_NG(),
    "en_NP": lang_EN_NP.Num2Word_EN_NP(),
    "eo": lang_EO.Num2Word_EO(),
    "es": lang_ES.Num2Word_ES(),
    "es_CO": lang_ES_CO.Num2Word_ES_CO(),
    "es_CR": lang_ES_CR.Num2Word_ES_CR(),
    "es_GT": lang_ES_GT.Num2Word_ES_GT(),
    "es_HN": lang_ES_HN.Num2Word_ES_HN(),
    "es_NI": lang_ES_NI.Num2Word_ES_NI(),
    "es_VE": lang_ES_VE.Num2Word_ES_VE(),
    "et": lang_ET.Num2Word_ET(),
    "fa": lang_FA.Num2Word_FA(),
    "fi": lang_FI.Num2Word_FI(),
    "fr": lang_FR.Num2Word_FR(),
    "fr_BE": lang_FR_BE.Num2Word_FR_BE(),
    "fr_CH": lang_FR_CH.Num2Word_FR_CH(),
    "fr_DZ": lang_FR_DZ.Num2Word_FR_DZ(),
    "ha": lang_HA.Num2Word_HA(),
    "he": lang_HE.Num2Word_HE(),
    "hi": lang_HI.Num2Word_HI(),
    "hr": lang_HR.Num2Word_HR(),
    "hu": lang_HU.Num2Word_HU(),
    "hy": lang_HY.Num2Word_HY(),
    "id": lang_ID.Num2Word_ID(),
    "is": lang_IS.Num2Word_IS(),
    "it": lang_IT.Num2Word_IT(),
    "ja": lang_JA.Num2Word_JA(),
    "kn": lang_KN.Num2Word_KN(),
    "ko": lang_KO.Num2Word_KO(),
    "kz": lang_KZ.Num2Word_KZ(),
    "lt": lang_LT.Num2Word_LT(),
    "lv": lang_LV.Num2Word_LV(),
    "mn": lang_MN.Num2Word_MN(),
    "ms": lang_MS.Num2Word_MS(),
    "nl": lang_NL.Num2Word_NL(),
    "no": lang_NO.Num2Word_NO(),
    "pl": lang_PL.Num2Word_PL(),
    "pt": lang_PT.Num2Word_PT(),
    "pt_BR": lang_PT_BR.Num2Word_PT_BR(),
    "rm": lang_RM.Num2Word_RM(),
    "rm_puter": lang_RM_PUTER.Num2Word_RM_PUTER(),
    "rm_surmiran": lang_RM_SURMIRAN.Num2Word_RM_SURMIRAN(),
    "rm_sursilv": lang_RM_SURSILV.Num2Word_RM_SURSILV(),
    "rm_sutsilv": lang_RM_SUTSILV.Num2Word_RM_SUTSILV(),
    "rm_vallader": lang_RM_VALLADER.Num2Word_RM_VALLADER(),
    "ro": lang_RO.Num2Word_RO(),
    "ru": lang_RU.Num2Word_RU(),
    "sk": lang_SK.Num2Word_SK(),
    "sl": lang_SL.Num2Word_SL(),
    "sn": lang_SN.Num2Word_SN(),
    "sq": lang_SQ.Num2Word_SQ(),
    "sr": lang_SR.Num2Word_SR(),
    "sr_Cyrl": lang_SR.Num2Word_SR(),
    "sr_Latn": lang_SR_LATN.Num2Word_SR_LATN(),
    "sv": lang_SV.Num2Word_SV(),
    "sw": lang_SW.Num2Word_SW(),
    "ta": lang_TA.Num2Word_TA(),
    "te": lang_TE.Num2Word_TE(),
    "tet": lang_TET.Num2Word_TET(),
    "tg": lang_TG.Num2Word_TG(),
    "th": lang_TH.Num2Word_TH(),
    "tr": lang_TR.Num2Word_TR(),
    "uk": lang_UK.Num2Word_UK(),
    "vi": lang_VI.Num2Word_VI(),
    "zh": lang_ZH_CN.Num2Word_ZH_CN(),  # Default 'zh' to simplified Chinese
    "zh_CN": lang_ZH_CN.Num2Word_ZH_CN(),
    "zh_HK": lang_ZH_HK.Num2Word_ZH_HK(),
    "zh_TW": lang_ZH_TW.Num2Word_ZH_TW(),
    "as": lang_AS.Num2Word_AS(),
    "ba": lang_BA.Num2Word_BA(),
    "bo": lang_BO.Num2Word_BO(),
    "br": lang_BR.Num2Word_BR(),
    "bs": lang_BS.Num2Word_BS(),
    "eu": lang_EU.Num2Word_EU(),
    "fo": lang_FO.Num2Word_FO(),
    "gl": lang_GL.Num2Word_GL(),
    "gu": lang_GU.Num2Word_GU(),
    "haw": lang_HAW.Num2Word_HAW(),
    "ht": lang_HT.Num2Word_HT(),
    "jw": lang_JW.Num2Word_JW(),
    "ka": lang_KA.Num2Word_KA(),
    "kk": lang_KK.Num2Word_KK(),
    "km": lang_KM.Num2Word_KM(),
    "la": lang_LA.Num2Word_LA(),
    "lb": lang_LB.Num2Word_LB(),
    "ln": lang_LN.Num2Word_LN(),
    "lo": lang_LO.Num2Word_LO(),
    "mg": lang_MG.Num2Word_MG(),
    "mi": lang_MI.Num2Word_MI(),
    "mk": lang_MK.Num2Word_MK(),
    "ml": lang_ML.Num2Word_ML(),
    "mr": lang_MR.Num2Word_MR(),
    "mt": lang_MT.Num2Word_MT(),
    "my": lang_MY.Num2Word_MY(),
    "ne": lang_NE.Num2Word_NE(),
    "nn": lang_NN.Num2Word_NN(),
    "oc": lang_OC.Num2Word_OC(),
    "pa": lang_PA.Num2Word_PA(),
    "ps": lang_PS.Num2Word_PS(),
    "sa": lang_SA.Num2Word_SA(),
    "sd": lang_SD.Num2Word_SD(),
    "si": lang_SI.Num2Word_SI(),
    "so": lang_SO.Num2Word_SO(),
    "su": lang_SU.Num2Word_SU(),
    "tk": lang_TK.Num2Word_TK(),
    "tl": lang_TL.Num2Word_TL(),
    "tt": lang_TT.Num2Word_TT(),
    "ur": lang_UR.Num2Word_UR(),
    "uz": lang_UZ.Num2Word_UZ(),
    "uz_Cyrl": lang_UZ_CYR.Num2Word_UZ_CYRILLIC(),
    "uz_cyr": lang_UZ_CYR.Num2Word_UZ_CYRILLIC(),
    "wo": lang_WO.Num2Word_WO(),
    "yi": lang_YI.Num2Word_YI(),
    "yo": lang_YO.Num2Word_YO(),
    # Newly added languages
    "ban": lang_BAN.Num2Word_BAN(),
    "bm": lang_BM.Num2Word_BM(),
    "ceb": lang_CEB.Num2Word_CEB(),
    "ckb": lang_CKB.Num2Word_CKB(),
    "cnh": lang_CNH.Num2Word_CNH(),
    "ff": lang_FF.Num2Word_FF(),
    "fil": lang_FIL.Num2Word_FIL(),
    "hmn": lang_HMN.Num2Word_HMN(),
    "ki": lang_KI.Num2Word_KI(),
    "kok": lang_KOK.Num2Word_KOK(),
    "ksw": lang_KSW.Num2Word_KSW(),
    "ku": lang_KU.Num2Word_KU(),
    "ky": lang_KY.Num2Word_KY(),
    "lg": lang_LG.Num2Word_LG(),
    "lij": lang_LIJ.Num2Word_LIJ(),
    "lus": lang_LUS.Num2Word_LUS(),
    "om": lang_OM.Num2Word_OM(),
    "or": lang_OR.Num2Word_OR(),
    "pap": lang_PAP.Num2Word_PAP(),
    "pli": lang_PLI.Num2Word_PLI(),
    "rw": lang_RW.Num2Word_RW(),
    "ti": lang_TI.Num2Word_TI(),
    "xh": lang_XH.Num2Word_XH(),
    "zu": lang_ZU.Num2Word_ZU(),
    # Language code aliases
    "jp": lang_JA.Num2Word_JA(),  # Alias for Japanese
    "cn": lang_ZH_CN.Num2Word_ZH_CN(),  # Alias for Chinese (Simplified)
    "nb": lang_NO.Num2Word_NO(),  # Alias for Norwegian Bokmål
    "jv": lang_JW.Num2Word_JW(),  # Alias for Javanese (modern ISO 639-1)
    "miz": lang_LUS.Num2Word_LUS(),  # Alias for Mizo
    "cz": lang_CS.Num2Word_CS(),  # Pre-ISO-639 code for Czech (ISO is 'cs')
    "dk": lang_DA.Num2Word_DA(),  # Pre-ISO-639 code for Danish (ISO is 'da')
}

CONVERTES_TYPES = ["cardinal", "ordinal", "ordinal_num", "year", "currency"]
CONVERTER_TYPES = CONVERTES_TYPES  # Alias for compatibility


def num2words(number, ordinal=False, lang="en", to="cardinal", **kwargs):
    # We try the full language first
    if lang not in CONVERTER_CLASSES:
        normalized_lang = lang.replace("-", "_")
        if normalized_lang in CONVERTER_CLASSES:
            lang = normalized_lang
        else:
            parts = normalized_lang.split("_")
            if len(parts) >= 2:
                candidate = f"{parts[0].lower()}_{parts[1].upper()}"
                if candidate in CONVERTER_CLASSES:
                    lang = candidate
                else:
                    lang = parts[0]
            else:
                lang = normalized_lang
    if lang not in CONVERTER_CLASSES:
        # ... and then try only the first 2 letters
        lang = lang[:2]
    if lang not in CONVERTER_CLASSES:
        raise NotImplementedError()
    converter = CONVERTER_CLASSES[lang]

    if isinstance(number, str):
        # If the string is a mix of text and numerals (e.g. "text 1"),
        # route to num2words_sentence which extracts numerals and converts
        # each in place. A pure-text string like "hello" still raises so
        # we don't silently swallow caller errors. Issue #61 ports
        # savoirfairelinux/num2words#281.
        try:
            number = converter.str_to_number(number)
        except (decimal.InvalidOperation, ValueError):
            if any(ch.isdigit() for ch in number):
                return num2words_sentence(number, lang=lang, to=to, **kwargs)
            raise

    # backwards compatible
    if ordinal:
        to = "ordinal"

    if to not in CONVERTES_TYPES:
        raise NotImplementedError()

    # precision= overrides the per-language fractional precision for this
    # call. Issue #580 ports savoirfairelinux/num2words#580.
    precision_override = kwargs.pop("precision", None)
    saved_precision = None
    if precision_override is not None and hasattr(converter, "precision"):
        saved_precision = converter.precision
        converter.precision = int(precision_override)

    # cents='omit' on to='currency' drops the cents portion entirely. The
    # legacy cents=True/False kwarg is kept as-is (False historically meant
    # "use digits instead of words"). Issue #554 ports
    # savoirfairelinux/num2words#554 / #190.
    if to == "currency":
        cents_kw = kwargs.get("cents")
        if cents_kw == "omit":
            kwargs["cents"] = True  # let downstream see a valid bool
            if isinstance(number, float):
                number = int(number)  # int path drops cents naturally
        elif cents_kw == "verbose":
            kwargs["cents"] = True
        elif cents_kw == "terse":
            kwargs["cents"] = False

    # style='terse' on to='ordinal' drops the leading 'one' / 'un' / etc.
    # Issue #535 ports savoirfairelinux/num2words#535 / #147.
    style = kwargs.pop("style", None)

    try:
        result = getattr(converter, "to_{}".format(to))(number, **kwargs)
    finally:
        if saved_precision is not None:
            converter.precision = saved_precision

    if style == "terse" and to == "ordinal" and isinstance(result, str):
        # Drop a leading "one " / "un " / "uno " prefix that's stylistic.
        # 100 → "one hundredth" → "hundredth"; 1000 → "one thousandth" →
        # "thousandth"; the same applies to fr's "un millionième" but
        # that's already handled in lang_FR's _BIG_UNITS.
        for prefix in ("one ", "un ", "uno "):
            if result.startswith(prefix) and len(result) > len(prefix):
                result = result[len(prefix):]
                break
    if style == "us" and lang.startswith("en") and isinstance(result, str):
        # American English drops 'and' between hundreds and tens
        # ("two hundred fifty" not "two hundred and fifty"). Issue #562
        # ports savoirfairelinux/num2words#562 by @granvillebarker.
        result = result.replace(" and ", " ")
    return result


def num2words_sentence(sentence, lang="en", to="cardinal", **kwargs):
    """
    Convert all numbers in a sentence to their word equivalents.

    This function handles:
    - Ordinal numbers (1st, 2nd, 3rd, etc.)
    - Currency ($99.99)
    - Dates (April 5, 2022)
    - Temperature (-5 degrees)
    - Regular numbers

    Args:
        sentence (str): The input sentence containing numbers
        lang (str): Language code (default: 'en')
        **kwargs: Additional arguments passed to the converter

    Returns:
        str: The sentence with all numbers converted to words

    Examples:
        >>> num2words_sentence("I bought 6 apples")
        "I bought six apples"
        >>> num2words_sentence("The 1st place winner got $100")
        "The first place winner got one hundred dollars"
    """
    from .converters.sentence import SentenceConverter

    converter = SentenceConverter()
    return converter.convert(sentence, lang=lang, to=to)


# Aliases for num2words_sentence
convert_sentence = num2words_sentence
sentence_to_words = num2words_sentence
