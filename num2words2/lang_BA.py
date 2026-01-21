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


# Bashkir language support
class Num2Word_BA(Num2Word_Base):
    CURRENCY_FORMS = {
        'RUB': (('һум', 'һум'), ('тин', 'тин')),
        'USD': (('доллар', 'доллар'), ('цент', 'цент')),
        'EUR': (('евро', 'евро'), ('цент', 'цент')),
    }

    def setup(self):
        self.negword = "минус "
        self.pointword = "өтөр"

    def to_cardinal(self, number):
        """Convert a number to its word representation in Bashkir."""
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
            return ret
        else:
            return ret + self._int_to_word(int(n))

    def _int_to_word(self, number):
        """Convert an integer to its word representation in Bashkir."""
        if number == 0:
            return "нуль"

        ones = ["", "бер", "ике", "өс", "дүрт", "биш", "алты", "ете", "һигеҙ", "туғыҙ"]
        tens = ["", "", "егерме", "утыҙ", "ҡырҡ", "илле", "алтмыш", "етмеш", "һикһән", "туҡһан"]
        teens = ["ун", "ун бер", "ун ике", "ун өс", "ун дүрт", "ун биш", "ун алты", "ун ете", "ун һигеҙ", "ун туғыҙ"]

        if number < 10:
            return ones[number]
        elif number < 20:
            return teens[number - 10]
        elif number < 100:
            return tens[number // 10] + (" " + ones[number % 10] if number % 10 else "")
        elif number < 1000:
            return ones[number // 100] + " йөҙ" + (" " + self._int_to_word(number % 100) if number % 100 else "")
        elif number < 1000000:
            return self._int_to_word(number // 1000) + " мең" + (" " + self._int_to_word(number % 1000) if number % 1000 else "")
        elif number < 1000000000:
            return self._int_to_word(number // 1000000) + " миллион" + (" " + self._int_to_word(number % 1000000) if number % 1000000 else "")
        else:
            return self._int_to_word(number // 1000000000) + " миллиард" + (" " + self._int_to_word(number % 1000000000) if number % 1000000000 else "")

    def to_ordinal(self, number):
        """Convert to ordinal."""
        cardinal = self.to_cardinal(number)
        return cardinal + "-се"

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return str(number) + "-се"

    def to_year(self, val, longval=True):
        """Convert to year."""
        return self.to_cardinal(val) + " йыл"

    def to_currency(self, val, currency='RUB', cents=True, separator=' һәм ', adjective=False):
        """Convert to currency."""
        try:
            left, right, is_negative = self.parse_currency(val)
        except AttributeError:
            is_negative = False
            if val < 0:
                is_negative = True
                val = abs(val)

            left, right = self._split_currency(val)

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS['RUB'])

        left_str = self._int_to_word(int(left))
        cents_str = self._int_to_word(int(right)) if cents and right else ""

        result = left_str + " " + cr1[0]

        if cents_str:
            result += separator + cents_str + " " + cr2[0]

        return self.negword + result if is_negative else result

    def _split_currency(self, n):
        """Split currency into whole and fraction parts."""
        parts = str(n).split('.')
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, '0')) if len(parts) > 1 and parts[1] else 0
        return left, right
