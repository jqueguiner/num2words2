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


# Basque language support
class Num2Word_EU(Num2Word_Base):
    CURRENCY_FORMS = {
        "EUR": (("euro", "euro"), ("zentimo", "zentimo")),
        "USD": (("dolar", "dolar"), ("zentabo", "zentabo")),
        "GBP": (("libera", "libera"), ("penike", "penike")),
    }

    def setup(self):
        self.negword = "minus "
        self.pointword = "koma"

    def to_cardinal(self, number):
        """Convert a number to its word representation in Basque."""
        n = str(number).strip()

        if n.startswith("-"):
            n = n[1:]
            ret = self.negword
        else:
            ret = ""

        if "." in n:
            left, right = n.split(".", 1)
            ret += self._int_to_word(int(left)) + " " + self.pointword + " "
            ret += " ".join(self._int_to_word(int(d)) for d in right)
            return ret
        else:
            return ret + self._int_to_word(int(n))

    def _int_to_word(self, number):
        """Convert an integer to its word representation in Basque."""
        if number == 0:
            return "zero"

        ones = [
            "",
            "bat",
            "bi",
            "hiru",
            "lau",
            "bost",
            "sei",
            "zazpi",
            "zortzi",
            "bederatzi",
        ]
        tens = [
            "",
            "hamar",
            "hogei",
            "hogeita hamar",
            "berrogei",
            "berrogeita hamar",
            "hirurogei",
            "hirurogeita hamar",
            "laurogei",
            "laurogeita hamar",
        ]

        if number < 10:
            return ones[number]
        elif number == 10:
            return "hamar"
        elif number < 20:
            return "hama" + ones[number - 10]
        elif number < 100:
            ten_val = number // 10
            one_val = number % 10
            if one_val == 0:
                return tens[ten_val]
            else:
                return tens[ten_val] + "ta " + ones[one_val]
        elif number < 1000:
            hundred_val = number // 100
            remainder = number % 100
            if hundred_val == 1:
                result = "ehun"
            else:
                result = ones[hundred_val] + "ehun"
            if remainder:
                result += " eta " + self._int_to_word(remainder)
            return result
        elif number < 1000000:
            thousand_val = number // 1000
            remainder = number % 1000
            if thousand_val == 1:
                result = "mila"
            else:
                result = self._int_to_word(thousand_val) + " mila"
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:
            million_val = number // 1000000
            remainder = number % 1000000
            if million_val == 1:
                result = "milioi bat"
            else:
                result = self._int_to_word(million_val) + " milioi"
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:
            billion_val = number // 1000000000
            remainder = number % 1000000000
            result = self._int_to_word(billion_val) + " mila milioi"
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result

    def to_ordinal(self, number):
        """Convert to ordinal."""
        cardinal = self.to_cardinal(number)
        if cardinal.endswith("t"):
            return cardinal + "garren"
        else:
            return cardinal + "garren"

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return str(number) + "."

    def to_year(self, val, longval=True):
        """Convert to year."""
        return self.to_cardinal(val) + ". urtea"

    def to_currency(
        self, val, currency="EUR", cents=True, separator=" eta ", adjective=False
    ):
        """Convert to currency."""
        try:
            left, right, is_negative = self.parse_currency(val)
        except AttributeError:
            is_negative = False
            if val < 0:
                is_negative = True
                val = abs(val)

            left, right = self._split_currency(val)

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS["EUR"])

        left_str = self._int_to_word(int(left))
        cents_str = self._int_to_word(int(right)) if cents and right else ""

        result = left_str + " " + cr1[0]

        if cents_str:
            result += separator + cents_str + " " + cr2[0]

        return self.negword + result if is_negative else result

    def _split_currency(self, n):
        """Split currency into whole and fraction parts."""
        parts = str(n).split(".")
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0
        return left, right
