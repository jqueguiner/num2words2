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


# Gujarati language support
class Num2Word_GU(Num2Word_Base):
    CURRENCY_FORMS = {
        "INR": (("રૂપિયો", "રૂપિયા"), ("પૈસો", "પૈસા")),
        "USD": (("ડોલર", "ડોલર"), ("સેન્ટ", "સેન્ટ")),
        "EUR": (("યૂરો", "યૂરો"), ("સેન્ટ", "સેન્ટ")),
        "GBP": (("પાઉન્ડ", "પાઉન્ડ"), ("પેન્સ", "પેન્સ")),
    }

    def setup(self):
        self.negword = "ઋણ "
        self.pointword = "દશાંશ"

    def to_cardinal(self, number):
        """Convert a number to its word representation in Gujarati."""
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
        """Convert an integer to its word representation in Gujarati."""
        if number == 0:
            return "શૂન્ય"

        # Gujarati number words
        ones = ["", "એક", "બે", "ત્રણ", "ચાર", "પાંચ", "છ", "સાત", "આઠ", "નવ"]
        tens = [
            "",
            "દસ",
            "વીસ",
            "ત્રીસ",
            "ચાલીસ",
            "પચાસ",
            "સાઠ",
            "સિત્તેર",
            "એંસી",
            "નેવું",
        ]
        teens = [
            "દસ",
            "અગિયાર",
            "બાર",
            "તેર",
            "ચૌદ",
            "પંદર",
            "સોળ",
            "સત્તર",
            "અઢાર",
            "ઓગણીસ",
        ]

        # Handle special numbers
        if number < 0:
            return self.negword + self._int_to_word(abs(number))
        elif number < 10:
            return ones[number]
        elif number < 20:
            return teens[number - 10]
        elif number < 100:
            result = tens[number // 10]
            if number % 10:
                result += " " + ones[number % 10]
            return result
        elif number < 1000:
            result = ones[number // 100] + " સો"
            remainder = number % 100
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000:  # Indian lakh system
            result = self._int_to_word(number // 1000) + " હજાર"
            remainder = number % 1000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 10000000:  # 1 crore
            result = self._int_to_word(number // 100000) + " લાખ"
            remainder = number % 100000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:  # Less than 100 crore
            result = self._int_to_word(number // 10000000) + " કરોડ"
            remainder = number % 10000000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000000000:  # Arab
            result = self._int_to_word(number // 1000000000) + " અબજ"
            remainder = number % 1000000000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:  # Kharab
            result = self._int_to_word(number // 100000000000) + " ખર્વ"
            remainder = number % 100000000000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result

    def to_ordinal(self, number):
        """Convert to ordinal in Gujarati."""
        cardinal = self.to_cardinal(number)

        # Gujarati ordinal suffixes
        if number == 1:
            return "પહેલો"
        elif number == 2:
            return "બીજો"
        elif number == 3:
            return "ત્રીજો"
        elif number == 4:
            return "ચોથો"
        elif number == 6:
            return "છઠ્ઠો"
        else:
            return cardinal + "મો"

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        if number == 1:
            return "૧લો"
        elif number == 2:
            return "૨જો"
        elif number == 3:
            return "૩જો"
        else:
            return str(number) + "મો"

    def to_year(self, val, longval=True):
        """Convert to year in Gujarati."""
        if val < 0:
            return "ઈસવીસન પૂર્વે " + self.to_cardinal(abs(val))
        else:
            return "સન " + self.to_cardinal(val)

    def to_currency(
        self, val, currency="INR", cents=True, separator=" અને ", adjective=False
    ):
        """Convert to currency in Gujarati."""
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
