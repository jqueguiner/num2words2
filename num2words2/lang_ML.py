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


# Malayalam language support
class Num2Word_ML(Num2Word_Base):
    CURRENCY_FORMS = {
        'INR': (('രൂപ', 'രൂപ'), ('പൈസ', 'പൈസ')),
        'USD': (('dollar', 'dollars'), ('cent', 'cents')),
        'EUR': (('euro', 'euros'), ('cent', 'cents')),
    }

    def setup(self):
        self.negword = "മൈനസ് "
        self.pointword = "പോയിന്റ്"
        self.ones = ['', 'ഒന്ന്', 'രണ്ട്', 'മൂന്ന്', 'നാല്', 'അഞ്ച്', 'ആറ്', 'ഏഴ്', 'എട്ട്', 'ഒൻപത്']
        self.tens = ['', 'പത്ത്', 'ഇരുപത്', 'മുപ്പത്', 'നാല്പത്', 'അമ്പത്', 'അറുപത്', 'എഴുപത്', 'എൺപത്', 'തൊണ്ണൂറ്']
        self.teens = ['പത്ത്', 'പതിനൊന്ന്', 'പന്ത്രണ്ട്', 'പതിമൂന്ന്', 'പതിനാല്', 'പതിനഞ്ച്', 'പതിനാറ്', 'പതിനേഴ്', 'പതിനെട്ട്', 'പത്തൊൻപത്']
        self.hundred = "നൂറ്"
        self.thousand = "ആയിരം"
        self.lakh = "ലക്ഷം"
        self.crore = "കോടി"
        self.zero = "പൂജ്യം"

    def to_cardinal(self, number):
        """Convert a number to its word representation in Malayalam."""
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
        """Convert an integer to its word representation in Malayalam."""
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
        """Convert to ordinal in Malayalam.

        Malayalam ordinals use '-ാം' (-aam) suffix for most numbers.
        Special forms exist for first few ordinals.
        """
        if number == 1:
            return "ഒന്നാം"  # first
        elif number == 2:
            return "രണ്ടാം"  # second
        elif number == 3:
            return "മൂന്നാം"  # third
        elif number == 4:
            return "നാലാം"  # fourth
        elif number == 5:
            return "അഞ്ചാം"  # fifth
        else:
            # For other numbers, add -ാം suffix
            cardinal = self.to_cardinal(number)
            return cardinal + "ാം"

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return str(number) + "."

    def to_year(self, val, longval=True):
        """Convert to year in Malayalam."""
        if val < 0:
            return "BC " + self.to_cardinal(abs(val))
        else:
            return "" + self.to_cardinal(val)

    def to_currency(self, val, currency='INR', cents=True, separator=' ', adjective=False):
        """Convert to currency in Malayalam."""
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
