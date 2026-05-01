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
        # Strict ICAO Annex 10 vol II respellings (FAA / SKYbrary
        # confirm the same set). 1/2/8 use the aggressive forms
        # wun/too/ait, not the everyday English words.
        cases = {
            0: "zero",
            1: "wun",
            2: "too",
            3: "tree",
            4: "fower",
            5: "fife",
            6: "six",
            7: "seven",
            8: "ait",
            9: "niner",
        }
        for v, expected in cases.items():
            self.assertEqual(num2words(v, lang="en_Aero_ICAO"), expected)

    def test_multi_digit(self):
        # The canonical example from the issue: 5739 → fife seven tree niner.
        self.assertEqual(
            num2words(5739, lang="en_Aero_ICAO"), "fife seven tree niner"
        )

    def test_round_hundred(self):
        # Aviation reads round numbers digit-by-digit too.
        self.assertEqual(
            num2words(100, lang="en_Aero_ICAO"), "wun zero zero"
        )
        self.assertEqual(
            num2words(1000, lang="en_Aero_ICAO"), "wun zero zero zero"
        )

    def test_year(self):
        # Years follow the same digit-by-digit rule.
        self.assertEqual(
            num2words(1971, lang="en_Aero_ICAO", to="year"),
            "wun niner seven wun",
        )
        self.assertEqual(
            num2words(2026, lang="en_Aero_ICAO", to="year"),
            "too zero too six",
        )

    def test_decimal_point(self):
        # The decimal mark is "decimal" in ICAO usage.
        self.assertEqual(
            num2words(127.5, lang="en_Aero_ICAO"),
            "wun too seven decimal fife",
        )
        self.assertEqual(
            num2words(0.99, lang="en_Aero_ICAO"),
            "zero decimal niner niner",
        )

    def test_negative(self):
        self.assertEqual(
            num2words(-42, lang="en_Aero_ICAO"), "minus fower too"
        )
        self.assertEqual(
            num2words(-1.5, lang="en_Aero_ICAO"),
            "minus wun decimal fife",
        )


class TestEnAeroStringInput(unittest.TestCase):

    def test_string_int(self):
        self.assertEqual(
            num2words("5739", lang="en_Aero_ICAO"), "fife seven tree niner"
        )

    def test_string_float(self):
        self.assertEqual(
            num2words("127.5", lang="en_Aero_ICAO"),
            "wun too seven decimal fife",
        )

    def test_explicit_method_call_strips_separators(self):
        # The dispatcher's str_to_number path doesn't tolerate comma
        # thousand separators (it routes mixed-text through
        # num2words_sentence). Calling to_cardinal directly handles them
        # via _digits_of. Document that here as the supported path.
        from num2words2 import CONVERTER_CLASSES
        c = CONVERTER_CLASSES["en_Aero_ICAO"]
        self.assertEqual(c.to_cardinal("12,345"), "wun too tree fower fife")
        self.assertEqual(c.to_cardinal("12_345"), "wun too tree fower fife")


class TestEnAeroLookup(unittest.TestCase):
    """The canonical key is ``en_Aero_ICAO``. Aliases keep older
    callers working: ``en_aero_icao``, ``en-x-aero-icao`` (BCP 47
    private-use form), and the v1.0.14 alias ``en_AERO``."""

    def test_canonical_key(self):
        self.assertEqual(
            num2words(5739, lang="en_Aero_ICAO"), "fife seven tree niner"
        )

    def test_lowercase_alias(self):
        self.assertEqual(
            num2words(5739, lang="en_aero_icao"), "fife seven tree niner"
        )

    def test_bcp47_private_use(self):
        # 'en-x-aero-icao' — BCP 47 private-use subtag form.
        self.assertEqual(
            num2words(5739, lang="en-x-aero-icao"), "fife seven tree niner"
        )

    def test_v1014_back_compat_alias(self):
        # The v1.0.14 keys still resolve to the same converter.
        self.assertEqual(
            num2words(5739, lang="en_AERO"), "fife seven tree niner"
        )
        self.assertEqual(
            num2words(5739, lang="en-AERO"), "fife seven tree niner"
        )
        self.assertEqual(
            num2words(5739, lang="en_aero"), "fife seven tree niner"
        )


class TestEnAeroFractionsRoute(unittest.TestCase):
    """Fraction routing still works for the AERO variant since it
    inherits to_fraction from Num2Word_EN."""

    def test_fraction_inherits_english(self):
        self.assertEqual(num2words("1/3", lang="en_Aero_ICAO"), "one third")
        self.assertEqual(num2words("1/2", lang="en_Aero_ICAO"), "one half")


class TestEnAeroAviationPhraseology(unittest.TestCase):
    """Aviation-specific reading conventions for altitude / flight level
    / heading / squawk / runway / frequency. Each follows FAA AIM 4-2-9
    and the matching ICAO Annex 10 vol II rule.

    These methods are aviation-only and live on Num2Word_EN_AERO; users
    call them via the converter instance:

        from num2words2 import CONVERTER_CLASSES
        aero = CONVERTER_CLASSES['en_Aero_ICAO']
        aero.to_altitude(5500)   # "fife thousand fife hundred feet"
    """

    def setUp(self):
        from num2words2 import CONVERTER_CLASSES
        self.aero = CONVERTER_CLASSES["en_Aero_ICAO"]

    # ---- altitude ----
    def test_altitude_thousands_under_10k(self):
        self.assertEqual(
            self.aero.to_altitude(5500),
            "fife thousand fife hundred feet",
        )
        self.assertEqual(
            self.aero.to_altitude(1000),
            "wun thousand feet",
        )
        self.assertEqual(
            self.aero.to_altitude(9900),
            "niner thousand niner hundred feet",
        )

    def test_altitude_at_or_above_10k_digit_by_digit(self):
        # Per FAA AIM 4-2-9, ≥10 000 ft uses digit-by-digit thousands.
        self.assertEqual(
            self.aero.to_altitude(10000),
            "wun zero thousand feet",
        )
        self.assertEqual(
            self.aero.to_altitude(12500),
            "wun too thousand fife hundred feet",
        )
        self.assertEqual(
            self.aero.to_altitude(25000),
            "too fife thousand feet",
        )

    def test_altitude_unit_override(self):
        self.assertEqual(
            self.aero.to_altitude(3000, unit="meters"),
            "tree thousand meters",
        )

    def test_altitude_negative_raises(self):
        with self.assertRaises(ValueError):
            self.aero.to_altitude(-100)

    # ---- flight level ----
    def test_flight_level(self):
        self.assertEqual(self.aero.to_flight_level(230), "flight level too tree zero")
        self.assertEqual(self.aero.to_flight_level(360), "flight level tree six zero")
        self.assertEqual(self.aero.to_flight_level(50), "flight level zero fife zero")

    def test_flight_level_out_of_range(self):
        with self.assertRaises(ValueError):
            self.aero.to_flight_level(1000)

    # ---- heading ----
    def test_heading_three_digits(self):
        self.assertEqual(self.aero.to_heading(360), "heading tree six zero")
        self.assertEqual(self.aero.to_heading(30), "heading zero tree zero")
        self.assertEqual(self.aero.to_heading(180), "heading wun ait zero")

    def test_heading_zero_maps_to_360(self):
        # In aviation, 360 (or 000) is north. Treat 0 as 360.
        self.assertEqual(self.aero.to_heading(0), "heading tree six zero")

    # ---- squawk ----
    def test_squawk_codes(self):
        # Common codes: 7700 emergency, 7600 lost-comms, 7500 hijack,
        # 1200 VFR (US).
        self.assertEqual(self.aero.to_squawk(7700), "squawk seven seven zero zero")
        self.assertEqual(self.aero.to_squawk(7600), "squawk seven six zero zero")
        self.assertEqual(self.aero.to_squawk(7500), "squawk seven fife zero zero")
        self.assertEqual(self.aero.to_squawk(1200), "squawk wun too zero zero")
        self.assertEqual(self.aero.to_squawk(0), "squawk zero zero zero zero")

    def test_squawk_out_of_range(self):
        with self.assertRaises(ValueError):
            self.aero.to_squawk(8888)

    # ---- runway ----
    def test_runway_with_suffix(self):
        self.assertEqual(self.aero.to_runway("27R"), "runway too seven right")
        self.assertEqual(self.aero.to_runway("09L"), "runway zero niner left")
        self.assertEqual(self.aero.to_runway("36C"), "runway tree six center")

    def test_runway_no_suffix(self):
        self.assertEqual(self.aero.to_runway("14"), "runway wun fower")
        self.assertEqual(self.aero.to_runway("5"), "runway fife")

    def test_runway_int_input(self):
        self.assertEqual(self.aero.to_runway(27), "runway too seven")

    def test_runway_lowercase_suffix(self):
        self.assertEqual(self.aero.to_runway("27r"), "runway too seven right")

    # ---- frequency ----
    def test_frequency_with_decimal(self):
        # Common ATC freqs: 121.5 = guard; 118.x range = tower.
        self.assertEqual(
            self.aero.to_frequency(121.5),
            "wun too wun decimal fife",
        )
        self.assertEqual(
            self.aero.to_frequency(118.025),
            "wun wun ait decimal zero too fife",
        )

    def test_frequency_string_preserves_trailing_zero(self):
        # Strings keep trailing zeros that float literals lose.
        self.assertEqual(
            self.aero.to_frequency("121.50"),
            "wun too wun decimal fife zero",
        )

    def test_frequency_integer(self):
        self.assertEqual(
            self.aero.to_frequency(122),
            "wun too too",
        )


if __name__ == "__main__":
    unittest.main()
