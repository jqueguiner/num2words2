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


# Punjabi language support
class Num2Word_PA(Num2Word_Base):
    CURRENCY_FORMS = {
        "INR": (("ਰੁਪਈਆ", "ਰੁਪਏ"), ("ਪੈਸਾ", "ਪੈਸੇ")),
        "USD": (("dollar", "dollars"), ("cent", "cents")),
        "EUR": (("euro", "euros"), ("cent", "cents")),
    }

    def setup(self):
        self.negword = "ਮਾਇਨਸ "
        self.pointword = "ਦਸ਼ਮਲਵ"
        self.ones = ["", "ਇੱਕ", "ਦੋ", "ਤਿੰਨ", "ਚਾਰ", "ਪੰਜ", "ਛੇ", "ਸੱਤ", "ਅੱਠ", "ਨੌ"]
        self.tens = [
            "",
            "ਦਸ",
            "ਵੀਹ",
            "ਤੀਹ",
            "ਚਾਲੀ",
            "ਪੰਜਾਹ",
            "ਸੱਠ",
            "ਸੱਤਰ",
            "ਅੱਸੀ",
            "ਨੱਬੇ",
        ]
        self.teens = [
            "ਦਸ",
            "ਗਿਆਰਾਂ",
            "ਬਾਰਾਂ",
            "ਤੇਰਾਂ",
            "ਚੌਦਾਂ",
            "ਪੰਦਰਾਂ",
            "ਸੋਲਾਂ",
            "ਸਤਾਰਾਂ",
            "ਅਠਾਰਾਂ",
            "ਉੱਨੀ",
        ]
        self.hundred = "ਸੌ"
        self.thousand = "ਹਜ਼ਾਰ"
        self.lakh = "ਲੱਖ"
        self.crore = "ਕਰੋੜ"
        self.zero = "ਸਿਫਰ"

    def to_cardinal(self, number):
        """Convert a number to its word representation in Punjabi."""
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
            return ret.strip()
        else:
            return (ret + self._int_to_word(int(n))).strip()

    def _int_to_word(self, number):
        """Convert an integer to its word representation in Punjabi."""
        if number == 0:
            return self.zero

        if number < 0:
            return self.negword + self._int_to_word(abs(number))
        elif number < 10:
            return self.ones[number]
        elif number < 20:
            return self.teens[number - 10]
        elif number < 100:
            result = self.tens[number // 10]
            if number % 10:
                result += " " + self.ones[number % 10]
            return result
        elif number < 1000:
            result = self.ones[number // 100] + " " + self.hundred
            remainder = number % 100
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000:  # Lakh
            result = self._int_to_word(number // 1000) + " " + self.thousand
            remainder = number % 1000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 10000000:  # Crore
            result = self._int_to_word(number // 100000) + " " + self.lakh
            remainder = number % 100000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:
            result = self._int_to_word(number // 10000000) + " " + self.crore
            remainder = number % 10000000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:
            return str(number)  # Fallback for very large numbers

    def to_ordinal(self, number):
        """Convert to ordinal in Punjabi.

        Punjabi ordinals use 'ਵਾਂ' suffix for masculine and 'ਵੀਂ' for feminine.
        Special forms exist for first few ordinals.
        """
        if number == 1:
            return "ਪਹਿਲਾ"  # first
        elif number == 2:
            return "ਦੂਜਾ"  # second
        elif number == 3:
            return "ਤੀਜਾ"  # third
        elif number == 4:
            return "ਚੌਥਾ"  # fourth
        elif number == 5:
            return "ਪੰਜਵਾਂ"  # fifth
        else:
            # For other numbers, add ਵਾਂ suffix
            cardinal = self.to_cardinal(number)
            return cardinal + "ਵਾਂ"

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return str(number) + "."

    def to_year(self, val, longval=True):
        """Convert to year in Punjabi."""
        if val < 0:
            return "BC " + self.to_cardinal(abs(val))
        else:
            return "" + self.to_cardinal(val)

    def to_currency(
        self, val, currency="INR", cents=True, separator=" ", adjective=False
    ):
        """Convert to currency in Punjabi."""
        is_negative = False
        if val < 0:
            is_negative = True
            val = abs(val)

        parts = str(val).split(".")
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS["INR"])

        left_str = self._int_to_word(left)
        result = left_str + " " + (cr1[1] if left != 1 else cr1[0])

        if cents and right:
            cents_str = self._int_to_word(right)
            result += separator + cents_str + " " + (cr2[1] if right != 1 else cr2[0])

        if is_negative:
            result = self.negword + result

        return result.strip()
