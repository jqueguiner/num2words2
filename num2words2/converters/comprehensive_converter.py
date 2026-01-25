#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive Number-to-Words Converter
========================================
A unified converter that combines all features:
- Automatic language detection
- Temperature conversion with proper formatting
- Grammatical agreement (gender, number, case)
- Support for 100+ languages
- Context-aware number type detection
"""

import os
import re
import sys
from typing import List, Optional, Tuple

import langdetect
from langdetect import detect_langs

from num2words2 import num2words

# Configure langdetect
langdetect.DetectorFactory.seed = 0

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


class ComprehensiveConverter:
    """
    Comprehensive converter with all features:
    - Auto language detection
    - Temperature/date/year/currency conversion
    - Grammatical agreement
    """

    def __init__(self):
        self.lang = None

        # Temperature patterns for major languages
        self.temp_patterns = {
            "fr": r"(-?\d+(?:[.,]\d+)?)\s+degrés?(?:\s+[Cc]elsius)?",
            "es": r"(-?\d+(?:[.,]\d+)?)\s+grados?(?:\s+[Cc]elsius)?",
            "it": r"(-?\d+(?:[.,]\d+)?)\s+gradi?(?:\s+[Cc]elsius)?",
            "pt": r"(-?\d+(?:[.,]\d+)?)\s+graus?(?:\s+[Cc]elsius)?",
            "de": r"(-?\d+(?:[.,]\d+)?)\s+[Gg]rad(?:\s+[Cc]elsius)?",
            "en": r"(-?\d+(?:[.,]\d+)?)\s+degrees?(?:\s+[Cc]elsius)?",
            "nl": r"(-?\d+(?:[.,]\d+)?)\s+graden?(?:\s+[Cc]elsius)?",
            "ru": r"(-?\d+(?:[.,]\d+)?)\s+градус(?:а|ов)?",
            "pl": r"(-?\d+(?:[.,]\d+)?)\s+stopni(?:e|i)?",
            "sv": r"(-?\d+(?:[.,]\d+)?)\s+grader?",
            "ja": r"(-?\d+(?:[.,]\d+)?)\s*度",
            "zh": r"(-?\d+(?:[.,]\d+)?)\s*[度度]",
            "ko": r"(-?\d+(?:[.,]\d+)?)\s*도",
        }

        # Temperature words for each language
        self.temp_words = {
            "fr": "degrés",
            "es": "grados",
            "it": "gradi",
            "pt": "graus",
            "de": "Grad",
            "en": "degrees",
            "nl": "graden",
            "ru": "градусов",
            "pl": "stopni",
            "sv": "grader",
            "ja": "度",
            "zh": "度",
            "ko": "도",
            "da": "grader",
            "no": "grader",
            "fi": "astetta",
            "cs": "stupňů",
            "hu": "fok",
            "tr": "derece",
            "ar": "درجة",
            "hi": "डिग्री",
        }

        # Celsius translations
        self.celsius_words = {
            "fr": "Celsius",
            "es": "Celsius",
            "it": "Celsius",
            "pt": "Celsius",
            "de": "Celsius",
            "en": "Celsius",
            "nl": "Celsius",
            "ru": "Цельсия",
            "pl": "Celsjusza",
            "sv": "Celsius",
            "ja": "摂氏",
            "zh": "摄氏",
            "ko": "섭씨",
        }

        # Negative prefixes
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
            "ja": "マイナス",
            "zh": "负",
            "ko": "마이너스",
            "cs": "minus",
            "da": "minus",
            "no": "minus",
            "fi": "miinus",
            "hu": "mínusz",
            "tr": "eksi",
            "ar": "ناقص",
            "hi": "ऋण",
        }

    def detect_language(self, text: str) -> str:
        """Detect the language of the text."""
        # Try langdetect first
        try:
            langs = detect_langs(text)
            if langs and langs[0].prob > 0.6:
                detected = langs[0].lang
                # Handle language variants
                if detected == "zh-cn":
                    return "zh"
                return detected
        except Exception:
            pass

        langid_module = _load_langid()
        if langid_module:
            try:
                lang, confidence = langid_module.classify(text)
                if confidence > 0.6:
                    return lang.split("-")[0] if "-" in lang else lang
            except Exception:
                pass

        # Heuristic detection based on common words
        heuristics = [
            (r"\b(le|la|les|un|une|de|et|est|pour|avec)\b", "fr"),
            (r"\b(der|die|das|ein|und|ist|mit|für)\b", "de"),
            (r"\b(el|la|los|las|y|es|con|para)\b", "es"),
            (r"\b(il|la|i|le|e|è|con|per)\b", "it"),
            (r"\b(o|a|os|as|e|é|com|para)\b", "pt"),
            (r"\b(the|a|an|and|is|with|for)\b", "en"),
        ]

        for pattern, lang in heuristics:
            if re.search(pattern, text, re.I):
                return lang

        return "en"  # Default

    def extract_numbers(self, sentence: str) -> List[Tuple[int, int, str, float, str]]:
        """
        Extract all numbers from sentence with their types.
        Returns: [(start_pos, end_pos, original_text, value, type)]
        """
        extractions = []
        used_positions = set()

        # 1. Temperature with degree symbol (highest priority)
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
            for match in re.finditer(self.temp_patterns[self.lang], sentence):
                start, end = match.span()
                if not any(p in used_positions for p in range(start, end)):
                    value = float(match.group(1).replace(",", "."))
                    extractions.append(
                        (start, end, match.group(0), value, "temperature_word")
                    )
                    used_positions.update(range(start, end))

        # 3. Date patterns with ordinals
        date_patterns = {
            "fr": [r"(\d+)er\s+([a-zéû]+)", r"(\d+)e\s+([a-zéû]+)"],
            "de": [r"(\d+)\.\s+([A-ZÄÖÜ][a-zäöüß]+)"],
            "es": [r"(\d+)\s+de\s+([a-z]+)"],
            "en": [r"(\d+)(?:st|nd|rd|th)\s+([A-Z][a-z]+)"],
        }

        if self.lang in date_patterns:
            for pattern in date_patterns[self.lang]:
                for match in re.finditer(pattern, sentence):
                    num_start = match.start(1)
                    num_end = match.end(1)
                    if not any(p in used_positions for p in range(num_start, num_end)):
                        value = int(match.group(1))

                        # Special handling for French "1er"
                        if self.lang == "fr" and "er" in match.group(0):
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
                        # German ordinals include period
                        elif self.lang == "de":
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
                            extractions.append(
                                (
                                    num_start,
                                    num_end,
                                    match.group(1),
                                    value,
                                    "date_number",
                                )
                            )
                            used_positions.update(range(num_start, num_end))

        # 4. Years (1900-2100)
        for match in re.finditer(r"\b(19\d{2}|20\d{2}|2100)\b", sentence):
            start, end = match.span()
            if not any(p in used_positions for p in range(start, end)):
                value = int(match.group(0))
                extractions.append((start, end, match.group(0), value, "year"))
                used_positions.update(range(start, end))

        # 5. Currency
        for match in re.finditer(r"([$€£¥]\s*)(\d+(?:[.,]\d+)?)", sentence):
            if not any(p in used_positions for p in range(match.start(), match.end())):
                value = float(match.group(2).replace(",", "."))
                extractions.append(
                    (match.start(), match.end(), match.group(0), value, "currency")
                )
                used_positions.update(range(match.start(), match.end()))

        # 6. Regular numbers
        for match in re.finditer(r"\b(\d+(?:[.,]\d+)?)\b", sentence):
            start, end = match.span()
            if not any(p in used_positions for p in range(start, end)):
                text = match.group(0)
                value = float(text.replace(",", "."))

                # Check for negative
                if start > 0 and sentence[start - 1] == "-":
                    start -= 1
                    text = "-" + text
                    value = -value

                extractions.append((start, end, text, value, "number"))
                used_positions.update(range(start, end))

        return sorted(extractions, key=lambda x: x[0])

    def convert_number(self, value: float, num_type: str) -> str:
        """Convert a number based on its type and language."""
        try:
            # Map language codes for num2words
            lang_map = {
                "pt_BR": "pt-br",
                "zh": "zh",
                "en_IN": "en",
            }
            num2words_lang = lang_map.get(self.lang, self.lang)

            # Temperature with symbol (e.g., 25°C)
            if num_type == "temperature_symbol":
                temp_word = self.temp_words.get(self.lang, "degrees")
                celsius = self.celsius_words.get(self.lang, "Celsius")

                if value < 0:
                    neg = self.negative_words.get(self.lang, "minus")
                    num = num2words(abs(value), lang=num2words_lang)
                    return f"{neg} {num} {temp_word} {celsius}"
                else:
                    num = num2words(value, lang=num2words_lang)
                    return f"{num} {temp_word} {celsius}"

            # Temperature with word (e.g., 25 degrees)
            elif num_type == "temperature_word":
                temp_word = self.temp_words.get(self.lang, "degrees")

                if value < 0:
                    neg = self.negative_words.get(self.lang, "minus")
                    num = num2words(abs(value), lang=num2words_lang)
                    return f"{neg} {num} {temp_word}"
                else:
                    num = num2words(value, lang=num2words_lang)
                    return f"{num} {temp_word}"

            # Ordinal dates
            elif num_type == "ordinal_date":
                if self.lang == "fr" and value == 1:
                    return "premier"
                elif self.lang == "de":
                    ordinal = num2words(value, lang=num2words_lang, ordinal=True)
                    # Check context for case (simplified)
                    return ordinal
                else:
                    return num2words(value, lang=num2words_lang, ordinal=True)

            # Date numbers (cardinal)
            elif num_type == "date_number":
                return num2words(value, lang=num2words_lang)

            # Years
            elif num_type == "year":
                try:
                    return num2words(value, lang=num2words_lang, to="year")
                except Exception:
                    return num2words(value, lang=num2words_lang)

            # Currency
            elif num_type == "currency":
                try:
                    return num2words(
                        value, lang=num2words_lang, to="currency", currency="EUR"
                    )
                except Exception:
                    return num2words(value, lang=num2words_lang)

            # Regular numbers
            else:
                if value < 0:
                    neg = self.negative_words.get(self.lang, "minus")
                    return f"{neg} {num2words(abs(value), lang=num2words_lang)}"
                else:
                    if value == int(value):
                        return num2words(int(value), lang=num2words_lang)
                    else:
                        return num2words(value, lang=num2words_lang)

        except Exception:
            # Fallback to English
            if value < 0:
                return f"minus {num2words(abs(value), lang='en')}"
            else:
                return num2words(value, lang="en")

    def convert_sentence(
        self, sentence: str, force_language: Optional[str] = None
    ) -> str:
        """
        Convert all numbers in a sentence to words.

        Args:
            sentence: Input sentence with numbers
            force_language: Optional language code to use instead of auto-detection

        Returns:
            Sentence with numbers converted to words
        """
        # Set language
        self.lang = force_language if force_language else self.detect_language(sentence)

        # Extract all numbers
        extractions = self.extract_numbers(sentence)

        if not extractions:
            return sentence

        # Convert from end to start (preserve positions)
        result = sentence
        for start, end, original, value, num_type in reversed(extractions):
            converted = self.convert_number(value, num_type)

            # Smart replacement for temperature words
            if num_type == "temperature_word" and self.lang in self.temp_words:
                # Only replace the number part, keep the temperature word
                number_match = re.match(r"(-?\d+(?:[.,]\d+)?)", original)
                if number_match:
                    number_only = number_match.group(1)
                    # Get just the number part from conversion
                    temp_word = self.temp_words[self.lang]
                    if temp_word in converted:
                        converted_num = converted.split(f" {temp_word}")[0]
                    else:
                        converted_num = converted
                    # Replace only the number in the original
                    result = (
                        result[:start]
                        + original.replace(number_only, converted_num, 1)
                        + result[end:]
                    )
                else:
                    result = result[:start] + converted + result[end:]
            else:
                # Direct replacement
                result = result[:start] + converted + result[end:]

        return result


def test_converter():
    """Test the comprehensive converter with various examples."""
    converter = ComprehensiveConverter()

    test_cases = [
        # French
        ("La température sera de 25°C demain.", "fr"),
        ("Le 1er janvier 2025, il fera -10°C.", "fr"),
        ("Il fait 35 degrés aujourd'hui.", "fr"),
        # German
        ("Heute sind es -5 Grad Celsius.", "de"),
        ("Am 15. Januar 2024 werden es 12°C.", "de"),
        # Spanish
        ("Hoy la temperatura es de 23 grados.", "es"),
        ("El 15 de agosto de 2023 hace 42°C.", "es"),
        # English
        ("The temperature is 72 degrees today.", "en"),
        ("On January 1st, 2025, it will be -20°C.", "en"),
        # Auto-detection tests
        ("Il fait 28°C.", None),
        ("Heute 30 Grad.", None),
        ("Today is 25 degrees.", None),
    ]

    print("=" * 80)
    print("COMPREHENSIVE CONVERTER TEST")
    print("=" * 80)

    for sentence, lang in test_cases:
        if lang:
            result = converter.convert_sentence(sentence, force_language=lang)
            print(f"\n[{lang}] {sentence}")
        else:
            result = converter.convert_sentence(sentence)
            detected = converter.lang
            print(f"\n[Auto:{detected}] {sentence}")
        print(f"→ {result}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Interactive mode with input
        converter = ComprehensiveConverter()
        sentence = " ".join(sys.argv[1:])

        # Check for language hint
        if ":" in sentence and len(sentence.split(":")[0]) <= 5:
            lang, text = sentence.split(":", 1)
            result = converter.convert_sentence(
                text.strip(), force_language=lang.strip()
            )
            print(f"[{lang}] {result}")
        else:
            result = converter.convert_sentence(sentence)
            print(f"[{converter.lang}] {result}")
    else:
        # Run tests
        test_converter()
