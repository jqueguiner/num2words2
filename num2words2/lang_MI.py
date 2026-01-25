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


# Maori language support
class Num2Word_MI(Num2Word_Base):
    CURRENCY_FORMS = {
        "NZD": (("tāra", "tāra"), ("hēneti", "hēneti")),
        "USD": (("dollar", "dollars"), ("cent", "cents")),
        "EUR": (("euro", "euros"), ("cent", "cents")),
    }

    def setup(self):
        self.negword = "minus "
        self.pointword = "point"
        self.ones = [
            "",
            "tahi",
            "rua",
            "toru",
            "whā",
            "rima",
            "ono",
            "whitu",
            "waru",
            "iwa",
        ]
        self.tens = [
            "",
            "tekau",
            "rua tekau",
            "toru tekau",
            "whā tekau",
            "rima tekau",
            "ono tekau",
            "whitu tekau",
            "waru tekau",
            "iwa tekau",
        ]
        self.hundred = "rau"
        self.thousand = "mano"
        self.million = "miriona"

    def to_cardinal(self, number):
        """Convert a number to its word representation in Maori."""
        n = str(number).strip()

        if n.startswith("-"):
            n = n[1:]
            ret = self.negword
        else:
            ret = ""

        if "." in n:
            left, right = n.split(".", 1)
            ret += self._int_to_word(int(left)) + " " + self.pointword + " "
            for digit in right:
                ret += self._int_to_word(int(digit)) + " "
            return ret.strip()
        else:
            return (ret + self._int_to_word(int(n))).strip()

    def _int_to_word(self, number):
        """Convert an integer to its word representation in Maori."""
        if number == 0:
            return self.ones[0] if self.ones[0] else "zero"

        if number < 0:
            return self.negword + self._int_to_word(abs(number))
        elif number < 10:
            return self.ones[number]
        elif number < 100:
            tens_val = number // 10
            ones_val = number % 10
            if ones_val == 0:
                return self.tens[tens_val]
            else:
                return self.tens[tens_val] + " " + self.ones[ones_val]
        elif number < 1000:
            hundreds_val = number // 100
            remainder = number % 100
            result = self.ones[hundreds_val] + " " + self.hundred
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000:
            thousands_val = number // 1000
            remainder = number % 1000
            result = self._int_to_word(thousands_val) + " " + self.thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:
            millions_val = number // 1000000
            remainder = number % 1000000
            result = self._int_to_word(millions_val) + " " + self.million
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:
            return str(number)  # Fallback for very large numbers

    def to_ordinal(self, number):
        """Convert to ordinal in Maori.

        Maori ordinals use 'te' prefix and 'o' suffix pattern.
        Special forms for first few ordinals.
        """
        if number == 1:
            return "tuatahi"  # first
        elif number == 2:
            return "tuarua"  # second
        elif number == 3:
            return "tuatoru"  # third
        elif number == 4:
            return "tuawhā"  # fourth
        elif number == 5:
            return "tuarima"  # fifth
        else:
            # For other numbers, use "tua" prefix + cardinal
            cardinal = self.to_cardinal(number)
            return "tua " + cardinal

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return str(number) + "."

    def to_year(self, val, longval=True):
        """Convert to year in Maori."""
        return self.to_cardinal(val)

    def to_currency(
        self, val, currency="NZD", cents=True, separator=" ", adjective=False
    ):
        """Convert to currency in Maori."""
        is_negative = False
        if val < 0:
            is_negative = True
            val = abs(val)

        parts = str(val).split(".")
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0

        cr1, cr2 = self.CURRENCY_FORMS.get(
            currency, list(self.CURRENCY_FORMS.values())[0]
        )

        left_str = self._int_to_word(left)
        result = left_str + " " + (cr1[1] if left != 1 else cr1[0])

        if cents and right:
            cents_str = self._int_to_word(right)
            result += separator + cents_str + " " + (cr2[1] if right != 1 else cr2[0])

        if is_negative:
            result = self.negword + result

        return result.strip()
