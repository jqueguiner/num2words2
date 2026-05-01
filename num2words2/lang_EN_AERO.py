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
    "1": "one",
    "2": "two",
    "3": "tree",
    "4": "fower",
    "5": "fife",
    "6": "six",
    "7": "seven",
    "8": "eight",
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
