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


# Sinhala language support
class Num2Word_SI(Num2Word_Base):
    CURRENCY_FORMS = {
        'LKR': (('රුපියල්', 'රුපියල්'), ('සත', 'සත')),
        'USD': (('dollar', 'dollars'), ('cent', 'cents')),
        'EUR': (('euro', 'euros'), ('cent', 'cents')),
    }

    def setup(self):
        self.negword = "minus "
        self.pointword = "point"
        self.ones = ['', 'එක', 'දෙක', 'තුන', 'හතර', 'පහ', 'හය', 'හත', 'අට', 'නවය']
        self.tens = ['', 'දහය', 'විස්ස', 'තිහ', 'හතළිහ', 'පනහ', 'හැට', 'හැත්තෑව', 'අසූව', 'අනූව']
        self.hundred = 'සියය'
        self.thousand = 'දහස'
        self.lakh = 'ලක්ෂය'
        self.crore = 'කෝටිය'

    def to_cardinal(self, number):
        """Convert a number to its word representation in Sinhala."""
        n = str(number).strip()

        if n.startswith('-'):
            n = n[1:]
            ret = self.negword
        else:
            ret = ""

        if '.' in n:
            left, right = n.split('.', 1)
            ret += self._int_to_word(int(left)) + " " + self.pointword + " "
            for digit in right:
                ret += self._int_to_word(int(digit)) + " "
            return ret.strip()
        else:
            return (ret + self._int_to_word(int(n))).strip()

    def _int_to_word(self, number):
        """Convert an integer to its word representation in Sinhala."""
        if number == 0:
            return self.ones[0] if self.ones[0] else "බිංදුව"

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
            if hundreds_val == 1:
                result = self.hundred
            else:
                result = self.ones[hundreds_val] + " " + self.hundred
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000:
            thousands_val = number // 1000
            remainder = number % 1000
            if thousands_val == 1:
                result = self.thousand
            else:
                result = self._int_to_word(thousands_val) + " " + self.thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 10000000:
            lakh_val = number // 100000
            remainder = number % 100000
            if lakh_val == 1:
                result = self.lakh
            else:
                result = self._int_to_word(lakh_val) + " " + self.lakh
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:
            crore_val = number // 10000000
            remainder = number % 10000000
            if crore_val == 1:
                result = self.crore
            else:
                result = self._int_to_word(crore_val) + " " + self.crore
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:
            return str(number)  # Fallback for very large numbers

    def to_ordinal(self, number):
        """Convert to ordinal in Sinhala."""
        # Basic implementation with වැනි suffix
        return self.to_cardinal(number) + " වැනි"

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return str(number) + "."

    def to_year(self, val, longval=True):
        """Convert to year."""
        return self.to_cardinal(val)

    def to_currency(self, val, currency='LKR', cents=True, separator=' ', adjective=False):
        """Convert to currency in Sinhala."""
        is_negative = False
        if val < 0:
            is_negative = True
            val = abs(val)

        parts = str(val).split('.')
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, '0')) if len(parts) > 1 and parts[1] else 0

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS['LKR'])

        left_str = self.to_cardinal(left)
        result = left_str + " " + (cr1[1] if left != 1 else cr1[0])

        if cents and right:
            cents_str = self.to_cardinal(right)
            result += separator + cents_str + " " + (cr2[1] if right != 1 else cr2[0])

        return (self.negword if is_negative else "") + result
