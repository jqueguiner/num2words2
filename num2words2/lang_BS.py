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


# Bosnian language support (Latin script)
class Num2Word_BS(Num2Word_Base):
    CURRENCY_FORMS = {
        'BAM': (('marka', 'marke', 'maraka'), ('feninga', 'feninga', 'feninga')),
        'EUR': (('euro', 'eura', 'eura'), ('cent', 'centa', 'centi')),
        'USD': (('dolar', 'dolara', 'dolara'), ('cent', 'centa', 'centi')),
    }

    def setup(self):
        self.negword = "minus "
        self.pointword = "zarez"

        # Bosnian numbers in Latin script
        self.ones = [
            '', 'jedan', 'dva', 'tri', 'četiri',
            'pet', 'šest', 'sedam', 'osam', 'devet'
        ]

        self.tens = [
            '', 'deset', 'dvadeset', 'trideset', 'četrdeset',
            'pedeset', 'šezdeset', 'sedamdeset', 'osamdeset', 'devedeset'
        ]

        self.scale = {
            100: ('sto', 'stotine', 'stotina'),
            1000: ('hiljada', 'hiljade', 'hiljada'),
            1000000: ('milion', 'miliona', 'miliona'),
            1000000000: ('milijarda', 'milijarde', 'milijardi'),
            1000000000000: ('bilion', 'biliona', 'biliona'),
        }

    def to_cardinal(self, number):
        """Convert a number to its word representation in Bosnian."""
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
        """Convert an integer to its word representation in Bosnian."""
        if number == 0:
            return "nula"

        if number < 0:
            return self.negword + self._int_to_word(abs(number))
        elif number < 10:
            return self.ones[number]
        elif number == 10:
            return self.tens[1]
        elif number < 20:
            return self.ones[number - 10] + "aest"
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
                result = "sto"
            elif hundreds_val == 2:
                result = "dvjesto"
            elif hundreds_val == 3 or hundreds_val == 4:
                result = self.ones[hundreds_val] + "sto"
            else:
                result = self.ones[hundreds_val] + "sto"
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000:
            thousands_val = number // 1000
            remainder = number % 1000
            if thousands_val == 1:
                result = "hiljada"
            elif thousands_val < 5:
                result = self._int_to_word(thousands_val) + " hiljade"
            else:
                result = self._int_to_word(thousands_val) + " hiljada"
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:
            millions_val = number // 1000000
            remainder = number % 1000000
            if millions_val == 1:
                result = "milion"
            else:
                result = self._int_to_word(millions_val) + " miliona"
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:
            return str(number)  # Fallback for very large numbers

    def to_ordinal(self, number):
        """Convert to ordinal in Bosnian."""
        # Basic implementation with ordinal suffix
        if number == 1:
            return "prvi"
        elif number == 2:
            return "drugi"
        elif number == 3:
            return "treći"
        else:
            return self.to_cardinal(number) + "."

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return str(number) + "."

    def to_year(self, val, longval=True):
        """Convert to year in Bosnian."""
        return self.to_cardinal(val)

    def to_currency(self, val, currency='BAM', cents=True, separator=' ', adjective=False):
        """Convert to currency in Bosnian."""
        is_negative = False
        if val < 0:
            is_negative = True
            val = abs(val)

        parts = str(val).split('.')
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, '0')) if len(parts) > 1 and parts[1] else 0

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS['BAM'])

        left_str = self._int_to_word(left)
        # Select correct form based on number
        if left == 1:
            currency_word = cr1[0]
        elif left % 10 in [2, 3, 4] and left % 100 not in [12, 13, 14]:
            currency_word = cr1[1]
        else:
            currency_word = cr1[2]
        result = left_str + " " + currency_word

        if cents and right:
            cents_str = self._int_to_word(right)
            # Select correct form for cents
            if right == 1:
                cents_word = cr2[0]
            elif right % 10 in [2, 3, 4] and right % 100 not in [12, 13, 14]:
                cents_word = cr2[1]
            else:
                cents_word = cr2[2]
            result += separator + cents_str + " " + cents_word

        if is_negative:
            result = self.negword + result

        return result.strip()
