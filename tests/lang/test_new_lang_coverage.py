# Coverage gap-filler for the 23 new languages added in PR #14.
# Targets the three under-covered code paths shared across these
# implementations: > 1B fallback, currency-with-cents, and pluralize
# edge cases.
from unittest import TestCase

from num2words2 import num2words

NEW_LANG_CODES = [
    "ban", "bm", "ceb", "ckb", "cnh", "ff", "fil", "hmn", "ki", "kok",
    "ksw", "ku", "ky", "lg", "lus", "om", "or", "pap", "pli", "rw",
    "ti", "xh", "zu",
]


class TestLargeNumberFallback(TestCase):
    """Hit the str(number) fallback path for numbers >= 1e9."""

    def test_billion_plus(self):
        for code in NEW_LANG_CODES:
            with self.subTest(code=code):
                # 10^12 — beyond the explicit million scale in most templates
                result = num2words(10 ** 12, lang=code)
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)


class TestCurrencyWithCents(TestCase):
    """Hit the `if cents and right:` branch in to_currency."""

    def test_currency_with_fractional(self):
        for code in NEW_LANG_CODES:
            with self.subTest(code=code):
                # Float with non-zero cents triggers the cents branch
                result = num2words(12.34, lang=code, to="currency")
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)

    def test_currency_negative_with_cents(self):
        for code in NEW_LANG_CODES:
            with self.subTest(code=code):
                result = num2words(-7.89, lang=code, to="currency")
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)


class TestPluralizeEdgeCases(TestCase):
    """Hit the pluralize() edge cases."""

    def test_pluralize_empty_forms(self):
        from num2words2 import CONVERTER_CLASSES

        for code in NEW_LANG_CODES:
            with self.subTest(code=code):
                converter = CONVERTER_CLASSES[code]
                # Empty list — should return ''
                self.assertEqual(converter.pluralize(1, []), "")
                self.assertEqual(converter.pluralize(2, []), "")
                # None — should return ''
                self.assertEqual(converter.pluralize(1, None), "")
                # Single form — should return that form for both n=1 and n>1
                self.assertEqual(converter.pluralize(1, ["a"]), "a")
                # Multi forms — n=1 picks first, n>1 picks last
                self.assertEqual(converter.pluralize(1, ["a", "b"]), "a")
                self.assertEqual(converter.pluralize(5, ["a", "b"]), "b")
