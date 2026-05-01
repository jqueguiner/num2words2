# -*- coding: utf-8 -*-
"""Issue savoirfairelinux/num2words#478 — ICAO/aviation English.

Per ICAO Annex 10 vol II, numbers transmitted over voice radio are
enunciated digit-by-digit with five digits respelled to avoid acoustic
confusion: 3→tree, 4→fower, 5→fife, 7→seven, 9→niner.
"""
from __future__ import unicode_literals

import unittest

from num2words2 import num2words


class TestEnAeroDigitByDigit(unittest.TestCase):

    def test_zero_through_nine(self):
        cases = {
            0: "zero",
            1: "one",
            2: "two",
            3: "tree",
            4: "fower",
            5: "fife",
            6: "six",
            7: "seven",
            8: "eight",
            9: "niner",
        }
        for v, expected in cases.items():
            self.assertEqual(num2words(v, lang="en_AERO"), expected)

    def test_multi_digit(self):
        # The canonical example from the issue: 5739 → fife seven tree niner.
        self.assertEqual(num2words(5739, lang="en_AERO"), "fife seven tree niner")

    def test_round_hundred(self):
        # Aviation reads round numbers digit-by-digit too.
        self.assertEqual(num2words(100, lang="en_AERO"), "one zero zero")
        self.assertEqual(num2words(1000, lang="en_AERO"), "one zero zero zero")

    def test_year(self):
        # Years follow the same digit-by-digit rule.
        self.assertEqual(
            num2words(1971, lang="en_AERO", to="year"), "one niner seven one"
        )
        self.assertEqual(
            num2words(2026, lang="en_AERO", to="year"), "two zero two six"
        )

    def test_decimal_point(self):
        # The decimal mark is "decimal" in ICAO usage.
        self.assertEqual(
            num2words(127.5, lang="en_AERO"), "one two seven decimal fife"
        )
        self.assertEqual(
            num2words(0.99, lang="en_AERO"), "zero decimal niner niner"
        )

    def test_negative(self):
        self.assertEqual(num2words(-42, lang="en_AERO"), "minus fower two")
        self.assertEqual(
            num2words(-1.5, lang="en_AERO"), "minus one decimal fife"
        )


class TestEnAeroStringInput(unittest.TestCase):

    def test_string_int(self):
        self.assertEqual(
            num2words("5739", lang="en_AERO"), "fife seven tree niner"
        )

    def test_string_float(self):
        self.assertEqual(
            num2words("127.5", lang="en_AERO"), "one two seven decimal fife"
        )

    def test_explicit_method_call_strips_separators(self):
        # The dispatcher's str_to_number path doesn't tolerate comma
        # thousand separators (it routes mixed-text through
        # num2words_sentence). Calling to_cardinal directly handles them
        # via _digits_of. Document that here as the supported path.
        from num2words2 import CONVERTER_CLASSES
        c = CONVERTER_CLASSES["en_AERO"]
        self.assertEqual(c.to_cardinal("12,345"), "one two tree fower fife")
        self.assertEqual(c.to_cardinal("12_345"), "one two tree fower fife")


class TestEnAeroLookup(unittest.TestCase):

    def test_underscore_lower(self):
        self.assertEqual(
            num2words(5739, lang="en_aero"), "fife seven tree niner"
        )

    def test_dash_upper(self):
        self.assertEqual(
            num2words(5739, lang="en-AERO"), "fife seven tree niner"
        )

    def test_dash_lower(self):
        self.assertEqual(
            num2words(5739, lang="en-aero"), "fife seven tree niner"
        )


class TestEnAeroFractionsRoute(unittest.TestCase):
    """Fraction routing still works for the AERO variant since it
    inherits to_fraction from Num2Word_EN."""

    def test_fraction_inherits_english(self):
        self.assertEqual(num2words("1/3", lang="en_AERO"), "one third")
        self.assertEqual(num2words("1/2", lang="en_AERO"), "one half")


if __name__ == "__main__":
    unittest.main()
