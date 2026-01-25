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

from .base import Num2Word_Base
from .utils import get_digits, splitbyx

ZERO = ("nula",)

ONES = {
    1: ("jedan", "jedna"),
    2: ("dva", "dvije"),
    3: ("tri", "tri"),
    4: ("četiri", "četiri"),
    5: ("pet", "pet"),
    6: ("šest", "šest"),
    7: ("sedam", "sedam"),
    8: ("osam", "osam"),
    9: ("devet", "devet"),
}

TENS = {
    0: ("deset",),
    1: ("jedanaest",),
    2: ("dvanaest",),
    3: ("trinaest",),
    4: ("četrnaest",),
    5: ("petnaest",),
    6: ("šesnaest",),
    7: ("sedamnaest",),
    8: ("osamnaest",),
    9: ("devetnaest",),
}

TWENTIES = {
    2: ("dvadeset",),
    3: ("trideset",),
    4: ("četrdeset",),
    5: ("pedeset",),
    6: ("šezdeset",),
    7: ("sedamdeset",),
    8: ("osamdeset",),
    9: ("devedeset",),
}

HUNDREDS = {
    1: ("sto",),
    2: ("dvjesto",),
    3: ("tristo",),
    4: ("četiristo",),
    5: ("petsto",),
    6: ("šesto",),
    7: ("sedamsto",),
    8: ("osamsto",),
    9: ("devetsto",),
}

SCALE = {
    0: ("", "", "", False),
    1: ("tisuća", "tisuće", "tisuća", True),  # 10^3
    2: ("milijun", "milijuna", "milijuna", False),  # 10^6
    3: ("milijarda", "milijarde", "milijardi", False),  # 10^9
    4: ("bilijun", "bilijuna", "bilijuna", False),  # 10^12
    5: ("bilijardu", "bilijarde", "bilijardi", False),  # 10^15
    6: ("trilijun", "trilijuna", "trilijuna", False),  # 10^18
    7: ("trilijarda", "trilijarde", "trilijardi", False),  # 10^21
    8: ("kvadrilijun", "kvadrilijuna", "kvadrilijuna", False),  # 10^24
    9: ("kvadrilijarda", "kvadrilijarde", "kvadrilijardi", False),  # 10^27
    10: ("kvintilijun", "kvintilijuna", "kvintilijuna", False),  # 10^30
}


class Num2Word_HR(Num2Word_Base):
    CURRENCY_FORMS = {
        "HRK": (("kuna", "kune", "kuna", True), ("lipa", "lipe", "lipa", True)),
        "EUR": (("euro", "eura", "eura", False), ("cent", "centa", "centi", False)),
        "USD": (
            ("dolar", "dolara", "dolara", False),
            ("cent", "centa", "centi", False),
        ),
    }

    def setup(self):
        self.negword = "minus"
        self.pointword = "zarez"

    def to_cardinal(self, number, feminine=False):
        n = str(number).replace(",", ".")
        if "." in n:
            is_negative = n.startswith("-")
            abs_n = n[1:] if is_negative else n
            left, right = abs_n.split(".")
            leading_zero_count = len(right) - len(right.lstrip("0"))
            decimal_part = (ZERO[0] + " ") * leading_zero_count + self._int2word(
                int(right), feminine
            )
            result = "%s %s %s" % (
                self._int2word(int(left), feminine),
                self.pointword,
                decimal_part,
            )
            if is_negative:
                result = self.negword + " " + result
            return result
        else:
            return self._int2word(int(n), feminine)

    def pluralize(self, number, forms):
        """
        Croatian pluralization rules:
        - 1: singular form (1 kuna)
        - 2,3,4: paucal form (2,3,4 kune)
        - 5+ and numbers ending in 11,12,13,14: plural form (5 kuna, 11 kuna)
        """
        if number % 100 in [11, 12, 13, 14]:
            form = 2  # plural for teens
        elif number % 10 == 1:
            form = 0  # singular
        elif number % 10 in [2, 3, 4]:
            form = 1  # paucal
        else:
            form = 2  # plural
        return forms[form]

    def to_ordinal(self, number):
        """Convert to Croatian ordinal numbers."""
        try:
            num = int(number)
        except (ValueError, TypeError):
            return str(number)

        # Croatian ordinals
        ordinals = {
            1: "prvi",
            2: "drugi",
            3: "treći",
            4: "četvrti",
            5: "peti",
            6: "šesti",
            7: "sedmi",
            8: "osmi",
            9: "deveti",
            10: "deseti",
            11: "jedanaesti",
            12: "dvanaesti",
            13: "trinaesti",
            14: "četrnaesti",
            15: "petnaesti",
            16: "šesnaesti",
            17: "sedamnaesti",
            18: "osamnaesti",
            19: "devetnaesti",
            20: "dvadeseti",
            30: "trideseti",
            40: "četrdeseti",
            50: "pedeseti",
            60: "šezdeseti",
            70: "sedamdeseti",
            80: "osamdeseti",
            90: "devedeseti",
            100: "stoti",
            1000: "tisući",
        }

        if num in ordinals:
            return ordinals[num]

        # For other numbers, add 'i' suffix to the cardinal
        # This is a simplified implementation
        cardinal = self.to_cardinal(num)
        return cardinal + "i"

    def _cents_verbose(self, number, currency):
        return self._int2word(number, self.CURRENCY_FORMS[currency][1][-1])

    def _int2word(self, number, feminine=False):
        if number < 0:
            return " ".join([self.negword, self._int2word(abs(number))])

        if number == 0:
            return ZERO[0]

        # Special cases for exact powers of thousands in Croatian
        if number == 1000:
            return "tisuća"
        elif number == 1000000:
            return "milijun"
        elif number == 1000000000:
            return "milijarda"

        words = []
        chunks = list(splitbyx(str(number), 3))
        chunk_len = len(chunks)
        for chunk in chunks:
            chunk_len -= 1
            digit_right, digit_mid, digit_left = get_digits(chunk)

            if digit_left > 0:
                words.append(HUNDREDS[digit_left][0])

            if digit_mid > 1:
                words.append(TWENTIES[digit_mid][0])

            if digit_mid == 1:
                words.append(TENS[digit_right][0])
            elif digit_right > 0:
                # Skip "jedna/jedan" for thousands, millions etc. when it's the leading digit
                if not (
                    chunk_len > 0
                    and digit_left == 0
                    and digit_mid == 0
                    and digit_right == 1
                ):
                    is_feminine = feminine or SCALE[chunk_len][-1]
                    gender_idx = int(is_feminine)
                    words.append(ONES[digit_right][gender_idx])

            if chunk_len > 0 and chunk != 0:
                words.append(self.pluralize(chunk, SCALE[chunk_len]))

        return " ".join(words)

    def to_currency(
        self, val, currency="EUR", cents=True, separator="", adjective=False
    ):
        if isinstance(val, int):
            left = abs(val)
            right = 0
            is_negative = val < 0
            is_float = False
        else:
            from decimal import Decimal

            from .currency import parse_currency_parts

            # Check if value has fractional cents
            decimal_val = Decimal(str(val))
            has_fractional_cents = (decimal_val * 100) % 1 != 0

            left, right, is_negative = parse_currency_parts(
                val, is_int_with_cents=False, keep_precision=has_fractional_cents
            )
            is_float = True

        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]
        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"'
                % (currency, self.__class__.__name__)
            )

        minus_str = "%s " % self.negword.strip() if is_negative else ""
        money_str = self.to_cardinal(left)

        # Show cents if right > 0 OR if input was a float (even if 0 cents)
        if right > 0 or is_float:
            if right == 0:
                cents_str = self.to_cardinal(0) if cents else "0"
            else:
                # Handle fractional cents
                from decimal import Decimal

                if isinstance(right, Decimal):
                    # Convert fractional cents (e.g., 65.3 cents)
                    cents_str = (
                        self.to_cardinal_float(float(right))
                        if cents
                        else str(float(right))
                    )
                else:
                    cents_str = self.to_cardinal(right) if cents else str(right)
            # Always add comma before cents if no separator specified
            if separator:
                sep = separator
            else:
                sep = ","
            return "%s%s %s%s %s %s" % (
                minus_str,
                money_str,
                self.pluralize(left, cr1),
                sep,
                cents_str,
                self.pluralize(right, cr2),
            )
        else:
            return "%s%s %s" % (minus_str, money_str, self.pluralize(left, cr1))
