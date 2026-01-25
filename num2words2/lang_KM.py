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


# Khmer language support
class Num2Word_KM(Num2Word_Base):
    CURRENCY_FORMS = {
        "KHR": (("រៀល", "រៀល"), ("សេន", "សេន")),
        "USD": (("ដុល្លារ", "ដុល្លារ"), ("សេន", "សេន")),
        "EUR": (("អឺរ៉ូ", "អឺរ៉ូ"), ("សេន", "សេន")),
    }

    def setup(self):
        self.negword = "ដក "
        self.pointword = "ចំណុច"

        # Khmer numbers 0-10
        self.ones = [
            "សូន្យ",  # 0
            "មួយ",  # 1
            "ពីរ",  # 2
            "បី",  # 3
            "បួន",  # 4
            "ប្រាំ",  # 5
            "ប្រាំមួយ",  # 6
            "ប្រាំពីរ",  # 7
            "ប្រាំបី",  # 8
            "ប្រាំបួន",  # 9
        ]

        # Tens
        self.tens = [
            "",  # 0
            "ដប់",  # 10
            "ម្ភៃ",  # 20
            "សាមសិប",  # 30
            "សែសិប",  # 40
            "ហាសិប",  # 50
            "ហុកសិប",  # 60
            "ចិតសិប",  # 70
            "ប៉ែតសិប",  # 80
            "កៅសិប",  # 90
        ]

    def to_cardinal(self, number):
        """Convert a number to its word representation in Khmer."""
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
        """Convert an integer to its word representation in Khmer."""
        if number == 0:
            return self.ones[0]

        if number < 0:
            return self.negword + self._int_to_word(abs(number))
        elif number < 10:
            return self.ones[number]
        elif number == 10:
            return self.tens[1]
        elif number < 20:
            return self.tens[1] + self.ones[number - 10]
        elif number < 100:
            tens_val = number // 10
            ones_val = number % 10
            if ones_val == 0:
                return self.tens[tens_val]
            else:
                return self.tens[tens_val] + self.ones[ones_val]
        elif number < 1000:
            hundreds_val = number // 100
            remainder = number % 100
            result = self.ones[hundreds_val] + "រយ"  # hundred
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 10000:
            thousands_val = number // 1000
            remainder = number % 1000
            result = self.ones[thousands_val] + "ពាន់"  # thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000:
            ten_thousands_val = number // 10000
            remainder = number % 10000
            result = self.ones[ten_thousands_val] + "ម៉ឺន"  # ten thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000:
            hundred_thousands_val = number // 100000
            remainder = number % 100000
            result = self.ones[hundred_thousands_val] + "សែន"  # hundred thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:
            millions_val = number // 1000000
            remainder = number % 1000000
            result = self._int_to_word(millions_val) + " លាន"  # million
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:
            return str(number)  # Fallback for very large numbers

    def to_ordinal(self, number):
        """Convert to ordinal in Khmer."""
        cardinal = self.to_cardinal(number)
        return "ទី" + cardinal  # "ទី" is the ordinal prefix

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return "ទី" + str(number)

    def to_year(self, val, longval=True):
        """Convert to year in Khmer."""
        return "ឆ្នាំ " + self.to_cardinal(val)

    def to_currency(
        self, val, currency="KHR", cents=True, separator=" ", adjective=False
    ):
        """Convert to currency in Khmer."""
        is_negative = False
        if val < 0:
            is_negative = True
            val = abs(val)

        parts = str(val).split(".")
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS["KHR"])

        left_str = self._int_to_word(left)
        result = left_str + " " + cr1[0]

        if cents and right:
            cents_str = self._int_to_word(right)
            result += separator + cents_str + " " + cr2[0]

        return (self.negword if is_negative else "") + result
