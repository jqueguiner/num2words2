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


# Marathi language support
class Num2Word_MR(Num2Word_Base):
    CURRENCY_FORMS = {
        'INR': (('रुपया', 'रुपये'), ('पैसा', 'पैसे')),
        'USD': (('डॉलर', 'डॉलर'), ('सेंट', 'सेंट्स')),
        'EUR': (('युरो', 'युरो'), ('सेंट', 'सेंट्स')),
        'GBP': (('पाउंड', 'पाउंड'), ('पेन्स', 'पेन्स')),
    }

    def setup(self):
        self.negword = "ऋण "
        self.pointword = "दशांश"

    def to_cardinal(self, number):
        """Convert a number to its word representation in Marathi."""
        n = str(number).strip()

        if n.startswith('-'):
            n = n[1:]
            ret = self.negword
        else:
            ret = ""

        if '.' in n:
            left, right = n.split('.', 1)
            ret += self._int_to_word(int(left)) + " " + self.pointword + " "
            ret += " ".join(self._int_to_word(int(d)) for d in right)
            return ret.strip()
        else:
            return (ret + self._int_to_word(int(n))).strip()

    def _int_to_word(self, number):
        """Convert an integer to its word representation in Marathi."""
        if number == 0:
            return "शून्य"

        # Marathi number words
        ones = ["", "एक", "दोन", "तीन", "चार", "पाच", "सहा", "सात", "आठ", "नऊ"]
        tens = ["", "दहा", "वीस", "तीस", "चाळीस", "पन्नास", "साठ", "सत्तर", "ऐंशी", "नव्वद"]
        teens = ["दहा", "अकरा", "बारा", "तेरा", "चौदा", "पंधरा", "सोळा", "सतरा", "अठरा", "एकोणीस"]

        if number < 0:
            return self.negword + self._int_to_word(abs(number))
        elif number < 10:
            return ones[number]
        elif number < 20:
            return teens[number - 10]
        elif number < 100:
            result = tens[number // 10]
            if number % 10:
                if number // 10 == 2:  # Special case for 20s
                    result = "एक" + tens[2] if number == 21 else ones[number % 10] + tens[2]
                elif number // 10 == 9 and number % 10 == 9:  # 99
                    result = "नव्याण्णव"
                else:
                    result += " " + ones[number % 10] if number % 10 else ""
            return result
        elif number < 1000:
            result = ones[number // 100] + "शे"
            remainder = number % 100
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000:  # Indian lakh system
            result = self._int_to_word(number // 1000) + " हजार"
            remainder = number % 1000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 10000000:  # 1 crore
            result = self._int_to_word(number // 100000) + " लाख"
            remainder = number % 100000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:  # Less than 100 crore
            result = self._int_to_word(number // 10000000) + " कोटी"
            remainder = number % 10000000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000000000:  # Arab
            result = self._int_to_word(number // 1000000000) + " अब्ज"
            remainder = number % 1000000000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:  # Kharab
            result = self._int_to_word(number // 100000000000) + " खर्व"
            remainder = number % 100000000000
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result

    def to_ordinal(self, number):
        """Convert to ordinal in Marathi."""
        # Special ordinals
        if number == 1:
            return "पहिला"
        elif number == 2:
            return "दुसरा"
        elif number == 3:
            return "तिसरा"
        elif number == 4:
            return "चौथा"
        elif number == 5:
            return "पाचवा"
        elif number == 6:
            return "सहावा"
        elif number == 7:
            return "सातवा"
        elif number == 8:
            return "आठवा"
        elif number == 9:
            return "नववा"
        elif number == 10:
            return "दहावा"
        else:
            cardinal = self.to_cardinal(number)
            return cardinal + "वा"

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        if number == 1:
            return "१ला"
        elif number == 2:
            return "२रा"
        elif number == 3:
            return "३रा"
        elif number == 4:
            return "४था"
        else:
            return str(number) + "वा"

    def to_year(self, val, longval=True):
        """Convert to year in Marathi."""
        if val < 0:
            return "इसवीसन पूर्व " + self.to_cardinal(abs(val))
        else:
            return "सन " + self.to_cardinal(val)

    def to_currency(self, val, currency='INR', cents=True, separator=' आणि ', adjective=False):
        """Convert to currency in Marathi."""
        is_negative = False
        if val < 0:
            is_negative = True
            val = abs(val)

        parts = str(val).split('.')
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, '0')) if len(parts) > 1 and parts[1] else 0

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS['INR'])

        left_str = self._int_to_word(left)
        result = left_str + " " + (cr1[1] if left != 1 else cr1[0])

        if cents and right:
            cents_str = self._int_to_word(right)
            result += separator + cents_str + " " + (cr2[1] if right != 1 else cr2[0])

        if is_negative:
            result = self.negword + result

        return result.strip()
