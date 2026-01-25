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
    1: ("jedna",),
    2: ("dva",),
    3: ("tři",),
    4: ("čtyři",),
    5: ("pět",),
    6: ("šest",),
    7: ("sedm",),
    8: ("osm",),
    9: ("devět",),
}

TENS = {
    0: ("deset",),
    1: ("jedenáct",),
    2: ("dvanáct",),
    3: ("třináct",),
    4: ("čtrnáct",),
    5: ("patnáct",),
    6: ("šestnáct",),
    7: ("sedmnáct",),
    8: ("osmnáct",),
    9: ("devatenáct",),
}

TWENTIES = {
    2: ("dvacet",),
    3: ("třicet",),
    4: ("čtyřicet",),
    5: ("padesát",),
    6: ("šedesát",),
    7: ("sedmdesát",),
    8: ("osmdesát",),
    9: ("devadesát",),
}

HUNDREDS = {
    1: ("sto",),
    2: ("dvě stě",),
    3: ("tři sta",),
    4: ("čtyři sta",),
    5: ("pět set",),
    6: ("šest set",),
    7: ("sedm set",),
    8: ("osm set",),
    9: ("devět set",),
}

THOUSANDS = {
    1: ("tisíc", "tisíce", "tisíc"),  # 10^3
    2: ("milion", "miliony", "milionů"),  # 10^6
    3: ("miliarda", "miliardy", "miliard"),  # 10^9
    4: ("bilion", "biliony", "bilionů"),  # 10^12
    5: ("biliarda", "biliardy", "biliard"),  # 10^15
    6: ("trilion", "triliony", "trilionů"),  # 10^18
    7: ("triliarda", "triliardy", "triliard"),  # 10^21
    8: ("kvadrilion", "kvadriliony", "kvadrilionů"),  # 10^24
    9: ("kvadriliarda", "kvadriliardy", "kvadriliard"),  # 10^27
    10: ("quintillion", "quintilliony", "quintillionů"),  # 10^30
}


class Num2Word_CS(Num2Word_Base):
    CURRENCY_FORMS = {
        "CZK": (("koruna", "koruny", "korun"), ("haléř", "haléře", "haléřů")),
        "EUR": (
            ("euro", "euro", "euro"),  # Euro doesn't decline in Czech
            ("centů", "centů", "centů"),  # Cents always in genitive plural
        ),
        "USD": (("dolar", "dolary", "dolarů"), ("cent", "centy", "centů")),
    }

    def setup(self):
        self.negword = "mínus"
        self.pointword = "čárka"

    def to_cardinal(self, number):
        n = str(number).replace(",", ".")
        if "." in n:
            is_negative = n.startswith("-")
            abs_n = n[1:] if is_negative else n
            left, right = abs_n.split(".")

            # Say each decimal digit individually
            decimal_parts = []
            for digit in right:
                if digit == "0":
                    decimal_parts.append(ZERO[0])
                else:
                    decimal_parts.append(ONES[int(digit)][0])
            decimal_part = " ".join(decimal_parts)

            result = "%s %s %s" % (
                self._int2word(int(left)),
                self.pointword,
                decimal_part,
            )
            if is_negative:
                result = self.negword + " " + result
            return result
        else:
            # Handle negative integers
            is_negative = n.startswith("-")
            if is_negative:
                abs_n = n[1:]
                result = self._int2word(int(abs_n))
                return self.negword + " " + result
            else:
                return self._int2word(int(n))

    def pluralize(self, n, forms):
        if n == 1:
            form = 0
        elif 5 > n % 10 > 1 and (n % 100 < 10 or n % 100 > 20):
            form = 1
        else:
            form = 2
        return forms[form]

    def to_currency(
        self, val, currency="EUR", cents=True, separator=",", adjective=False
    ):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_CS, self).to_currency(
                    val,
                    currency=currency,
                    cents=cents,
                    separator=separator,
                    adjective=adjective,
                )

            minus_str = self.negword if val < 0 else ""
            abs_val = abs(val)
            money_str = self.to_cardinal(abs_val)

            # Proper pluralization for currency
            if abs_val == 1:
                currency_str = cr1[0] if isinstance(cr1, tuple) else cr1
            else:
                currency_str = (
                    cr1[1]
                    if isinstance(cr1, tuple) and len(cr1) > 1
                    else (cr1[0] if isinstance(cr1, tuple) else cr1)
                )

            return ("%s %s %s" % (minus_str, money_str, currency_str)).strip()

        # For floats, use the parent class implementation
        return super(Num2Word_CS, self).to_currency(
            val,
            currency=currency,
            cents=cents,
            separator=separator,
            adjective=adjective,
        )

    def to_ordinal(self, number):
        """Convert to Czech ordinal numbers."""
        try:
            num = int(number)
        except (ValueError, TypeError):
            return str(number)

        # Czech ordinals for 1-20
        ordinals = {
            1: "první",
            2: "druhý",
            3: "třetí",
            4: "čtvrtý",
            5: "pátý",
            6: "šestý",
            7: "sedmý",
            8: "osmý",
            9: "devátý",
            10: "desátý",
            11: "jedenáctý",
            12: "dvanáctý",
            13: "třináctý",
            14: "čtrnáctý",
            15: "patnáctý",
            16: "šestnáctý",
            17: "sedmnáctý",
            18: "osmnáctý",
            19: "devatenáctý",
            20: "dvacátý",
            30: "třicátý",
            40: "čtyřicátý",
            50: "padesátý",
            60: "šedesátý",
            70: "sedmdesátý",
            80: "osmdesátý",
            90: "devadesátý",
            100: "stý",
            1000: "tisící",
        }

        if num in ordinals:
            return ordinals[num]

        # For other numbers, use cardinal + 'ý' suffix
        # This is a simplified implementation
        cardinal = self.to_cardinal(num)
        return cardinal + "ý"

    def _int2word(self, n):
        if n == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS[n3][0])

            if n2 > 1:
                words.append(TWENTIES[n2][0])

            if n2 == 1:
                words.append(TENS[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                # Check if we need feminine form for 2 with miliarda/biliarda
                if n1 == 2 and i in [3, 5, 7]:  # miliarda, biliarda, triliarda
                    words.append("dvě")
                else:
                    words.append(ONES[n1][0])

            if i > 0:
                words.append(self.pluralize(x, THOUSANDS[i]))

        return " ".join(words)
