# -*- coding: utf-8 -*-
# Copyright (c) 2026, num2words2 contributors. All Rights Reserved.
# Licensed under LGPL-2.1 (see COPYING).
"""ICAO/aviation English ('en_AERO').

Per ICAO Annex 10 vol II (and the related FAA / NATO conventions):

* numbers are enunciated digit-by-digit, never as a composite cardinal
  (so ``5739`` reads "fife seven tree niner", not "five thousand seven
  hundred thirty-nine") — the goal is unambiguous transmission over
  noisy radio links;
* a handful of digits are respelled to avoid acoustic confusion:
  ``3 → tree``, ``4 → fower``, ``5 → fife``, ``7 → seven``, ``9 → niner``;
* the decimal mark is read as "decimal".

Source: https://en.wikipedia.org/wiki/NATO_phonetic_alphabet#Pronunciation
Issue savoirfairelinux/num2words#478.
"""
from __future__ import unicode_literals

from decimal import Decimal

from .lang_EN import Num2Word_EN

# ICAO standard digit pronunciations. The respellings are chosen to be
# distinct under heavy radio static; speakers who hear "five" in noisy
# audio can mistake it for "nine", but "fife"/"niner" pair cleanly.
_ICAO_DIGITS = {
    "0": "zero",
    "1": "wun",
    "2": "too",
    "3": "tree",
    "4": "fower",
    "5": "fife",
    "6": "six",
    "7": "seven",
    "8": "ait",
    "9": "niner",
}
_ICAO_DECIMAL = "decimal"
_ICAO_MINUS = "minus"


class Num2Word_EN_AERO(Num2Word_EN):
    """Digit-by-digit ICAO reading of any numeric input.

    The AERO variant only standardises cardinal/year reading. Higher-level
    modes that depend on cardinals internally (ordinals, fractions,
    currency) delegate to a sibling ``Num2Word_EN`` instance so they
    don't accidentally pick up the digit-by-digit cardinal form (which
    would turn "third" into "treeth" via vowel-substitution chaining).
    """

    def __init__(self):
        super(Num2Word_EN_AERO, self).__init__()
        # Hold a plain-English helper for modes ICAO doesn't standardise.
        self._english = Num2Word_EN()

    def _digits_of(self, value):
        # Normalise input to (sign, integer-part-string, fractional-part-string).
        if isinstance(value, str):
            s = value.strip()
        elif isinstance(value, Decimal):
            s = format(value, "f")
        else:
            s = str(value)
        is_negative = s.startswith("-")
        if is_negative:
            s = s[1:]
        # Drop any thousands separators users might pass in.
        s = s.replace(",", "").replace("_", "")
        if "." in s:
            int_part, frac_part = s.split(".", 1)
        else:
            int_part, frac_part = s, ""
        # Ensure at least one digit on the integer side ("." is invalid).
        if not int_part:
            int_part = "0"
        return is_negative, int_part, frac_part

    def to_cardinal(self, value):
        is_negative, int_part, frac_part = self._digits_of(value)
        words = []
        if is_negative:
            words.append(_ICAO_MINUS)
        for ch in int_part:
            if ch.isdigit():
                words.append(_ICAO_DIGITS[ch])
        if frac_part:
            words.append(_ICAO_DECIMAL)
            for ch in frac_part:
                if ch.isdigit():
                    words.append(_ICAO_DIGITS[ch])
        return " ".join(words)

    def to_year(self, value, **kwargs):
        # Aviation reads years digit-by-digit too: 1971 → "one niner seven one"
        return self.to_cardinal(value)

    def to_ordinal(self, value):
        # ICAO doesn't standardise ordinals; delegate to a plain English
        # converter so we get "third" not the broken "treeth" that would
        # happen if our digit-by-digit cardinal leaked into the ordinal
        # builder.
        return self._english.to_ordinal(value)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(int(value))

    def to_fraction(self, numerator, denominator):
        # Same reason as to_ordinal — fractions use the standard English
        # forms (one third, one half, ...) rather than digit-by-digit.
        return self._english.to_fraction(numerator, denominator)

    def to_currency(self, *args, **kwargs):
        return self._english.to_currency(*args, **kwargs)

    def to_cheque(self, *args, **kwargs):
        return self._english.to_cheque(*args, **kwargs)

    # ------------------------------------------------------------------
    # Aviation-specific phraseology. These follow FAA AIM 4-2-9 and
    # ICAO Annex 10 vol II conventions. Each method has its own rules
    # for which numerals are read as composite words vs digit-by-digit.
    # ------------------------------------------------------------------

    def _icao_digit(self, n):
        """Return the ICAO respelling of a single decimal digit."""
        return _ICAO_DIGITS[str(int(n))]

    def _icao_digits(self, s):
        """Render every digit character of ``s`` as ICAO words."""
        return " ".join(self._icao_digit(ch) for ch in str(s) if ch.isdigit())

    def to_altitude(self, value, unit="feet"):
        """FAA / ICAO altitude phraseology.

        Below 10 000: "<single ICAO digit> thousand[, <hundreds> hundred]"
                      — e.g. 5500 → "fife thousand fife hundred"
        At 10 000 and above: thousands portion is read digit-by-digit
                      — e.g. 12 500 → "wun too thousand fife hundred"
                            25 000 → "too fife thousand"
        Trailing unit is appended (default "feet"). Source: FAA AIM 4-2-9.
        """
        v = int(value)
        if v < 0:
            raise ValueError("altitude must be non-negative")
        thousands = v // 1000
        hundreds = (v % 1000) // 100
        leftover = v % 100
        parts = []
        if thousands > 0:
            if thousands < 10:
                parts.append(self._icao_digit(thousands))
            else:
                parts.append(self._icao_digits(thousands))
            parts.append("thousand")
        if hundreds > 0:
            parts.append(self._icao_digit(hundreds))
            parts.append("hundred")
        if leftover > 0:
            # Sub-hundred altitudes are rare but speakable digit-by-digit.
            parts.append(self._icao_digits("%02d" % leftover))
        if v == 0:
            parts.append("zero")
        if unit:
            parts.append(unit)
        return " ".join(parts)

    def to_flight_level(self, value):
        """Flight level: ``flight level <three-digit-by-digit>``.

        FL230 → "flight level too tree zero". The numeric input is
        always rendered as a 3-digit, zero-padded sequence.
        """
        v = int(value)
        if not 0 <= v <= 999:
            raise ValueError("flight level must be a 3-digit code (0-999)")
        return "flight level %s" % self._icao_digits("%03d" % v)

    def to_heading(self, value):
        """Heading: ``heading <three-digit-by-digit>``.

        Magnetic headings are always read as three digits including
        leading zeros: 30 → "heading zero tree zero", 360 → "heading
        tree six zero". Values outside 0-360 are taken modulo 360.
        """
        v = int(value) % 360 or 360
        return "heading %s" % self._icao_digits("%03d" % v)

    def to_squawk(self, value):
        """Transponder code: ``squawk <four-digit-by-digit>``.

        Codes are 4-digit octal (each digit 0-7); 7700 → "squawk seven
        seven zero zero". The input is zero-padded to four digits.
        """
        v = int(value)
        if not 0 <= v <= 7777:
            raise ValueError("squawk code must be 4 octal digits (0-7777)")
        return "squawk %s" % self._icao_digits("%04d" % v)

    def to_runway(self, value):
        """Runway designator: ``runway <digits> [left|right|center]``.

        Accepts integer ('27', '9') or string ('27R', '09L', '36C').
        Suffixes L/R/C (case-insensitive) are spoken as left/right/center.
        Magnetic-bearing digits are always read digit-by-digit.
        """
        s = str(value).strip().upper()
        suffix_map = {"L": "left", "R": "right", "C": "center"}
        suffix = ""
        if s and s[-1] in suffix_map:
            suffix = suffix_map[s[-1]]
            s = s[:-1]
        # Strip non-digit characters that may remain (e.g. whitespace).
        digits = "".join(ch for ch in s if ch.isdigit())
        if not digits:
            raise ValueError("runway designator must contain digits")
        parts = ["runway", self._icao_digits(digits)]
        if suffix:
            parts.append(suffix)
        return " ".join(parts)

    def to_frequency(self, value):
        """Radio frequency: ``<digits> decimal <digits>``.

        Common in voice-radio comms — 121.5 → "wun too wun decimal fife".
        Trailing zeros after the decimal are preserved as digits.
        """
        s = str(value).strip()
        if "." in s:
            int_part, frac_part = s.split(".", 1)
        else:
            int_part, frac_part = s, ""
        if not int_part:
            int_part = "0"
        out = self._icao_digits(int_part)
        if frac_part:
            out += " decimal " + self._icao_digits(frac_part)
        return out
