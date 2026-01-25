#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sentence-level number to words converter.
Converts all numbers in a sentence to their word equivalents.
"""

import os
import re
import sys
from typing import List, Optional, Tuple

from .. import CONVERTER_CLASSES, num2words

try:
    import langdetect
    from langdetect import detect_langs

    langdetect.DetectorFactory.seed = 0
    HAS_LANGDETECT = True
except ImportError:
    HAS_LANGDETECT = False

_LANGID = None
_LANGID_CHECKED = False


def _load_langid():
    global _LANGID
    global _LANGID_CHECKED

    if _LANGID_CHECKED:
        return _LANGID

    _LANGID_CHECKED = True
    if sys.platform == "darwin" and os.environ.get(
        "NUM2WORDS2_ENABLE_LANGID", ""
    ).lower() not in {"1", "true", "yes"}:
        return None

    try:
        import langid
    except Exception:
        return None

    _LANGID = langid
    return _LANGID


class SentenceConverter:
    """
    Convert all numbers in a sentence to words.
    Handles temperatures, dates, years, currency, and regular numbers.
    """

    def __init__(self):
        self.lang = None

        # Temperature patterns for major languages
        self.temp_patterns = {
            "fr": (
                r"(-?\d+(?:[.,]\d+)?)\s+degrés?(?:\s+[Cc]elsius)?",
                "degrés",
                "Celsius",
            ),
            "es": (
                r"(-?\d+(?:[.,]\d+)?)\s+grados?(?:\s+[Cc]elsius)?",
                "grados",
                "Celsius",
            ),
            "it": (
                r"(-?\d+(?:[.,]\d+)?)\s+gradi?(?:\s+[Cc]elsius)?",
                "gradi",
                "Celsius",
            ),
            "pt": (
                r"(-?\d+(?:[.,]\d+)?)\s+graus?(?:\s+[Cc]elsius)?",
                "graus",
                "Celsius",
            ),
            "de": (
                r"(-?\d+(?:[.,]\d+)?)\s+[Gg]rad(?:\s+[Cc]elsius)?",
                "Grad",
                "Celsius",
            ),
            "en": (
                r"(-?\d+(?:[.,]\d+)?)\s+degrees?(?:\s+[Ff]ahrenheit)?",
                "degrees",
                "Fahrenheit",
            ),
            "nl": (
                r"(-?\d+(?:[.,]\d+)?)\s+graden?(?:\s+[Cc]elsius)?",
                "graden",
                "Celsius",
            ),
            "ru": (r"(-?\d+(?:[.,]\d+)?)\s+градус(?:а|ов)?", "градусов", "Цельсия"),
            "pl": (r"(-?\d+(?:[.,]\d+)?)\s+stopni(?:e|i)?", "stopni", "Celsjusza"),
        }

        # Negative word mapping
        self.negative_words = {
            "fr": "moins",
            "es": "menos",
            "it": "meno",
            "pt": "menos",
            "de": "minus",
            "en": "minus",
            "nl": "min",
            "ru": "минус",
            "pl": "minus",
            "sv": "minus",
            "da": "minus",
            "no": "minus",
        }

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the text.

        Args:
            text: Input text

        Returns:
            ISO 639-1 language code
        """
        # Try langdetect first
        if HAS_LANGDETECT:
            try:
                langs = detect_langs(text)
                if langs and langs[0].prob > 0.7:
                    detected = langs[0].lang
                    # Map special cases
                    if detected == "zh-cn":
                        return "zh"
                    return detected
            except Exception:
                pass

        langid_module = _load_langid()
        if langid_module:
            try:
                lang, confidence = langid_module.classify(text)
                if confidence > 0.7:
                    return lang.split("-")[0] if "-" in lang else lang
            except Exception:
                pass

        # Simple heuristics based on common words
        patterns = [
            (r"\b(le|la|les|un|une|de|et|est|pour|avec)\b", "fr"),
            (r"\b(der|die|das|ein|und|ist|mit|für)\b", "de"),
            (r"\b(el|la|los|las|y|es|con|para)\b", "es"),
            (r"\b(il|la|i|le|e|è|con|per)\b", "it"),
            (r"\b(o|a|os|as|e|é|com|para)\b", "pt"),
            (r"\b(the|a|an|and|is|with|for|in|on)\b", "en"),
        ]

        for pattern, lang in patterns:
            if re.search(pattern, text, re.I):
                return lang

        return "en"  # Default to English

    def extract_numbers(self, sentence: str) -> List[Tuple[int, int, str, float, str]]:
        """
        Extract all numbers from sentence with their types.

        Args:
            sentence: Input sentence

        Returns:
            List of (start_pos, end_pos, original_text, value, type)
        """
        extractions = []
        used_positions = set()

        # 1. Temperature with degree symbol (°C, °F)
        for match in re.finditer(r"(-?\d+(?:[.,]\d+)?)\s*°[CFcf]", sentence):
            start, end = match.span()
            if not any(p in used_positions for p in range(start, end)):
                value = float(match.group(1).replace(",", "."))
                extractions.append(
                    (start, end, match.group(0), value, "temperature_symbol")
                )
                used_positions.update(range(start, end))

        # 2. Temperature with language-specific words
        if self.lang in self.temp_patterns:
            pattern, _, _ = self.temp_patterns[self.lang]
            for match in re.finditer(pattern, sentence):
                start, end = match.span()
                if not any(p in used_positions for p in range(start, end)):
                    value = float(match.group(1).replace(",", "."))
                    extractions.append(
                        (start, end, match.group(0), value, "temperature_word")
                    )
                    used_positions.update(range(start, end))

        # 3. Standalone ordinal numbers (1st, 2nd, 3rd, 4th, etc.) - must come before dates
        if self.lang == "en":
            for match in re.finditer(r"(\d+)(?:st|nd|rd|th)\b", sentence):
                # Check if it's followed by a month name (if so, skip - will be handled as date)
                after_text = (
                    sentence[match.end() : match.end() + 20]
                    if match.end() < len(sentence)
                    else ""
                )
                if not re.match(
                    r"\s*(?:January|February|March|April|May|June|July|August|September|October|November|December)",
                    after_text,
                    re.I,
                ):
                    start, end = match.span()
                    if not any(p in used_positions for p in range(start, end)):
                        value = int(match.group(1))
                        extractions.append(
                            (start, end, match.group(0), value, "ordinal")
                        )
                        used_positions.update(range(start, end))

        # 4. Dates with ordinals (language-specific)
        # Month names for date detection
        months_en = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"

        date_patterns = {
            "fr": [(r"(\d+)er\s+([a-zéû]+)", True), (r"(\d+)e\s+([a-zéû]+)", False)],
            "de": [(r"(\d+)\.\s+([A-ZÄÖÜ][a-zäöüß]+)", True)],
            "es": [(r"(\d+)\s+de\s+([a-z]+)", False)],
            "en": [
                (
                    r"(\d+)(?:st|nd|rd|th)\s+(" + months_en + ")",
                    True,
                ),  # Explicit ordinal with month
                (
                    r"(" + months_en + r")\s+(\d+)",
                    True,
                    "month_first",
                ),  # Month Day -> ordinal
                (
                    r"(\d+)\s+(" + months_en + ")",
                    True,
                    "day_first",
                ),  # Day Month -> ordinal
            ],
        }

        if self.lang in date_patterns:
            for pattern_info in date_patterns[self.lang]:
                if len(pattern_info) == 3:
                    pattern, is_ordinal, format_type = pattern_info
                else:
                    pattern, is_ordinal = pattern_info
                    format_type = None

                for match in re.finditer(pattern, sentence, re.I):
                    # Handle English month+day patterns specially
                    if self.lang == "en" and format_type in [
                        "month_first",
                        "day_first",
                    ]:
                        if format_type == "month_first":
                            # "April 5" - number is in group 2
                            num_start = match.start(2)
                            num_end = match.end(2)
                            num_text = match.group(2)
                        else:  # day_first
                            # "5 April" - number is in group 1
                            num_start = match.start(1)
                            num_end = match.end(1)
                            num_text = match.group(1)

                        if not any(
                            p in used_positions for p in range(num_start, num_end)
                        ):
                            value = int(num_text)
                            extractions.append(
                                (num_start, num_end, num_text, value, "ordinal_date")
                            )
                            used_positions.update(range(num_start, num_end))
                    else:
                        # Original handling for other patterns
                        num_start = match.start(1)
                        num_end = match.end(1)
                        if not any(
                            p in used_positions for p in range(num_start, num_end)
                        ):
                            value = int(match.group(1))

                            if self.lang == "fr" and "er" in match.group(0):
                                # French "1er"
                                extractions.append(
                                    (
                                        num_start,
                                        num_end + 2,
                                        match.group(1) + "er",
                                        value,
                                        "ordinal_date",
                                    )
                                )
                                used_positions.update(range(num_start, num_end + 2))
                            elif self.lang == "de":
                                # German with period
                                extractions.append(
                                    (
                                        num_start,
                                        num_end + 1,
                                        match.group(1) + ".",
                                        value,
                                        "ordinal_date",
                                    )
                                )
                                used_positions.update(range(num_start, num_end + 1))
                            else:
                                dtype = "ordinal_date" if is_ordinal else "date_number"
                                extractions.append(
                                    (num_start, num_end, match.group(1), value, dtype)
                                )
                                used_positions.update(range(num_start, num_end))

        # 5. Years (1900-2100) ONLY in actual date contexts with month names
        # Look for years after month names with a comma and day
        for match in re.finditer(r"\b(19\d{2}|20\d{2}|2100)\b", sentence):
            start, end = match.span()
            if not any(p in used_positions for p in range(start, end)):
                value = int(match.group(0))
                # Check if this looks like a year in a date context
                before_text = sentence[:start].strip()
                # Only treat as year if preceded by "month day," pattern
                # This ensures we only get dates like "April 5, 2022"
                if re.search(
                    r"(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d+,\s*$",
                    before_text.lower(),
                ):
                    # This looks like a year in a date
                    extractions.append((start, end, match.group(0), value, "year"))
                    used_positions.update(range(start, end))

        # 6. Currency
        for match in re.finditer(r"([$€£¥]\s*)(\d+(?:[.,]\d+)?)", sentence):
            if not any(p in used_positions for p in range(match.start(), match.end())):
                value = float(match.group(2).replace(",", "."))
                symbol = match.group(1).strip()
                extractions.append(
                    (
                        match.start(),
                        match.end(),
                        match.group(0),
                        value,
                        f"currency_{symbol}",
                    )
                )
                used_positions.update(range(match.start(), match.end()))

        # 7. Regular numbers (including negative) - only standalone numbers
        # Use lookahead/lookbehind to ensure we don't match numbers within words
        for match in re.finditer(
            r"(?<![a-zA-Z0-9])(-?\d+(?:[.,]\d+)?)(?![a-zA-Z0-9])", sentence
        ):
            start, end = match.span()
            if not any(p in used_positions for p in range(start, end)):
                text = match.group(0)
                value = float(text.replace(",", "."))
                extractions.append((start, end, text, value, "number"))
                used_positions.update(range(start, end))

        return sorted(extractions, key=lambda x: x[0])

    def convert_number(self, value: float, num_type: str) -> str:
        """
        Convert a number based on its type.

        Args:
            value: Numeric value
            num_type: Type of number (temperature_symbol, year, etc.)

        Returns:
            Number converted to words
        """
        try:
            # Temperature with symbol
            if num_type == "temperature_symbol":
                if self.lang in self.temp_patterns:
                    _, temp_word, celsius_word = self.temp_patterns[self.lang]
                else:
                    temp_word, celsius_word = "degrees", "Celsius"

                if value < 0:
                    neg_word = self.negative_words.get(self.lang, "minus")
                    converted = num2words(abs(value), lang=self.lang)
                    return f"{neg_word} {converted} {temp_word} {celsius_word}"
                else:
                    converted = num2words(value, lang=self.lang)
                    return f"{converted} {temp_word} {celsius_word}"

            # Temperature with word
            elif num_type == "temperature_word":
                if value < 0:
                    neg_word = self.negative_words.get(self.lang, "minus")
                    return f"{neg_word} {num2words(abs(value), lang=self.lang)}"
                else:
                    return num2words(value, lang=self.lang)

            # Ordinal numbers (1st, 2nd, 3rd, etc.)
            elif num_type == "ordinal":
                return num2words(value, to="ordinal", lang=self.lang)

            # Ordinal dates
            elif num_type == "ordinal_date":
                if self.lang == "fr" and value == 1:
                    return "premier"
                elif self.lang == "de":
                    # German ordinals need case agreement
                    base = num2words(value, to="ordinal", lang=self.lang)
                    # Default to base form, context will be handled in replacement
                    return base
                return num2words(value, to="ordinal", lang=self.lang)

            # Regular dates (cardinal)
            elif num_type == "date_number":
                return num2words(value, lang=self.lang)

            # Years - use year format for proper conversion
            elif num_type == "year":
                try:
                    return num2words(value, to="year", lang=self.lang)
                except Exception:
                    # Fallback to regular cardinal if year format not supported
                    return num2words(value, lang=self.lang)

            # Currency
            elif num_type.startswith("currency_"):
                symbol = num_type.split("_")[1]
                currency_map = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY"}
                currency = currency_map.get(symbol, "USD")
                try:
                    return num2words(
                        value, to="currency", currency=currency, lang=self.lang
                    )
                except Exception:
                    return num2words(value, lang=self.lang)

            # Regular numbers
            else:
                # Check if we have a conversion type override
                conversion_type = getattr(self, "conversion_type", "cardinal")

                if value < 0:
                    neg_word = self.negative_words.get(self.lang, "minus")
                    if conversion_type == "ordinal":
                        return f"{neg_word} {num2words(abs(value), to='ordinal', lang=self.lang)}"
                    else:
                        return f"{neg_word} {num2words(abs(value), lang=self.lang)}"
                elif value == int(value):
                    if conversion_type == "ordinal":
                        return num2words(int(value), to="ordinal", lang=self.lang)
                    else:
                        return num2words(int(value), lang=self.lang)
                else:
                    if conversion_type == "ordinal":
                        return num2words(value, to="ordinal", lang=self.lang)
                    else:
                        return num2words(value, lang=self.lang)

        except Exception:
            # Fallback to English
            return num2words(value, lang="en")

    def convert(
        self, sentence: str, lang: Optional[str] = None, to: str = "cardinal"
    ) -> str:
        """
        Convert all numbers in a sentence to words.

        Args:
            sentence: Input sentence containing numbers
            lang: Language code (optional, auto-detected if not provided)
            to: Conversion type ('cardinal', 'ordinal', etc.)

        Returns:
            Sentence with all numbers converted to words
        """
        self.conversion_type = to
        # Set language
        self.lang = lang if lang else self.detect_language(sentence)

        # Validate language is supported
        if (
            self.lang not in CONVERTER_CLASSES
            and self.lang[:2] not in CONVERTER_CLASSES
        ):
            raise NotImplementedError(f"Language '{self.lang}' is not supported")

        # Extract all numbers
        extractions = self.extract_numbers(sentence)

        if not extractions:
            return sentence

        # Replace from end to beginning to preserve positions
        result = sentence
        for start, end, original, value, num_type in reversed(extractions):
            converted = self.convert_number(value, num_type)

            # Check if the number is at the beginning of a sentence
            # (after period, exclamation, question mark, or at the very start)
            needs_capitalization = False
            if start == 0:
                needs_capitalization = True
            elif start > 0:
                # Look for sentence boundaries
                before_text = sentence[:start].rstrip()
                if before_text and before_text[-1] in ".!?":
                    needs_capitalization = True

            # Apply capitalization if needed
            if needs_capitalization and converted:
                converted = (
                    converted[0].upper() + converted[1:]
                    if len(converted) > 1
                    else converted.upper()
                )

            # Smart replacement for temperature words
            if num_type == "temperature_word" and self.lang in self.temp_patterns:
                # Only replace the number part
                number_match = re.match(r"(-?\d+(?:[.,]\d+)?)", original)
                if number_match:
                    number_only = number_match.group(1)
                    result = (
                        result[:start]
                        + original.replace(number_only, converted, 1)
                        + result[end:]
                    )
                else:
                    result = result[:start] + converted + result[end:]
            # German ordinal dates need case agreement
            elif num_type == "ordinal_date" and self.lang == "de":
                # Check context for German case
                before = sentence[:start].strip().lower()
                if (
                    before.endswith("am")
                    or before.endswith("zum")
                    or before.endswith("vom")
                ):
                    # Dative case - add 'n'
                    converted = (
                        converted + "n" if not converted.endswith("n") else converted
                    )
                elif before.endswith("den"):
                    # Accusative case - add 'n'
                    converted = (
                        converted + "n" if not converted.endswith("n") else converted
                    )
                # else: nominative/genitive - use base form
                result = result[:start] + converted + result[end:]
            else:
                result = result[:start] + converted + result[end:]

        return result


def num2words_sentence(
    sentence: str, lang: Optional[str] = None, to: str = "cardinal", **kwargs
) -> str:
    """
    Convert all numbers in a sentence to words.

    This is the main function for sentence-level conversion.
    It automatically detects the language if not specified and
    converts all numbers including temperatures, dates, years,
    currency, and regular numbers.

    Args:
        sentence: Input sentence containing numbers
        lang: Language code (optional, auto-detected if not provided)
              Examples: 'en', 'fr', 'de', 'es', 'it', 'pt', etc.

    Returns:
        Sentence with all numbers converted to words

    Examples:
        >>> num2words_sentence("The temperature is 25°C today.")
        'The temperature is twenty-five degrees Celsius today.'

        >>> num2words_sentence("Il fait 30 degrés.", lang='fr')
        'Il fait trente degrés.'

        >>> num2words_sentence("Das ist 15 Grad.", lang='de')
        'Das ist fünfzehn Grad.'

        >>> num2words_sentence("El 1 de enero de 2025")  # Auto-detects Spanish
        'El uno de enero de dos mil veinticinco'
    """
    converter = SentenceConverter()
    return converter.convert(sentence, lang, to)


# For backwards compatibility
sentence_to_words = num2words_sentence
convert_sentence = num2words_sentence
