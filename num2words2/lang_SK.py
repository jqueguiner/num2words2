# -*- coding: utf-8 -*-
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
from .utils import get_digits, splitbyx

ZERO = ('nula',)

ONES = {
    1: ('jeden', 'jeden', set()),
    2: ('dva', 'dve', {1, 3, 5, 7, 9}),
    3: ('tri', 'tri', set()),
    4: ('štyri', 'štyri', set()),
    5: ('päť', 'päť', set()),
    6: ('šesť', 'šesť', set()),
    7: ('sedem', 'sedem', set()),
    8: ('osem', 'osem', set()),
    9: ('deväť', 'deväť', set()),
}

TENS = {
    0: ('desať',),
    1: ('jedenásť',),
    2: ('dvanásť',),
    3: ('trinásť',),
    4: ('štrnásť',),
    5: ('pätnásť',),
    6: ('šestnásť',),
    7: ('sedemnásť',),
    8: ('osemnásť',),
    9: ('devätnásť',),
}

TWENTIES = {
    2: ('dvadsať',),
    3: ('tridsať',),
    4: ('štyridsať',),
    5: ('päťdesiat',),
    6: ('šesťdesiat',),
    7: ('sedemdesiat',),
    8: ('osemdesiat',),
    9: ('deväťdesiat',),
}

HUNDREDS = {
    1: ('sto',),
    2: ('dvesto',),
    3: ('tristo',),
    4: ('štyristo',),
    5: ('päťsto',),
    6: ('šesťsto',),
    7: ('sedemsto',),
    8: ('osemsto',),
    9: ('deväťsto',),
}

THOUSANDS = {
    1: ('tisíc', 'tisíc', 'tisíc'),  # 10^3
    2: ('milión', 'milióny', 'miliónov'),  # 10^6
    3: ('miliarda', 'miliardy', 'miliárd'),  # 10^9
    4: ('bilión', 'bilióny', 'biliónov'),  # 10^12
    5: ('biliarda', 'biliardy', 'biliárd'),  # 10^15
    6: ('trilión', 'trilióny', 'triliónov'),  # 10^18
    7: ('triliarda', 'triliardy', 'triliárd'),  # 10^21
    8: ('kvadrilión', 'kvadrilióny', 'kvadriliónov'),  # 10^24
    9: ('kvadriliarda', 'kvadriliardy', 'kvadriliárd'),  # 10^27
    10: ('kvintilión', 'kvintillióny', 'kvintiliónov'),  # 10^30
}


class Num2Word_SK(Num2Word_Base):
    CURRENCY_FORMS = {
        'EUR': (
            ('euro', 'eurá', 'eur'), ('cent', 'centy', 'centov')
        ),
        'CZK': (
            ('koruna', 'koruny', 'korún'), ('halier', 'haliere', 'halierov')
        ),
        'USD': (
            ('dolár', 'doláre', 'dolárov'), ('cent', 'centy', 'centov')
        ),
    }

    def setup(self):
        self.negword = "mínus"
        self.pointword = "celých"

    def to_cardinal(self, number):
        n = str(number).replace(',', '.')
        if '.' in n:
            is_negative = n.startswith('-')
            abs_n = n[1:] if is_negative else n
            left, right = abs_n.split('.')
            leading_zero_count = len(right) - len(right.lstrip('0'))
            decimal_part = ((ZERO[0] + ' ') * leading_zero_count +
                            self._int2word(int(right)))
            result = u'%s %s %s' % (
                self._int2word(int(left)),
                self.pointword,
                decimal_part
            )
            if is_negative:
                result = self.negword + ' ' + result
            return result
        else:
            # Handle negative integers
            is_negative = n.startswith('-')
            if is_negative:
                abs_n = n[1:]
                result = self._int2word(int(abs_n))
                return self.negword + ' ' + result
            else:
                return self._int2word(int(n))

    def pluralize(self, n, forms):
        if n == 1:
            form = 0
        elif 0 < n < 5:
            form = 1
        else:
            form = 2
        return forms[form]

    def to_currency(self, val, currency='EUR', cents=True, separator=',',
                    adjective=False):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_SK, self).to_currency(
                    val, currency=currency, cents=cents, separator=separator,
                    adjective=adjective)

            minus_str = self.negword if val < 0 else ""
            abs_val = abs(val)
            money_str = self.to_cardinal(abs_val)

            # Proper pluralization for currency
            if abs_val == 1:
                currency_str = cr1[0] if isinstance(cr1, tuple) else cr1
            else:
                currency_str = cr1[1] if isinstance(cr1, tuple) and len(cr1) > 1 else (cr1[0] if isinstance(cr1, tuple) else cr1)

            return (u'%s %s %s' % (minus_str, money_str, currency_str)).strip()

        # For floats, use the parent class implementation
        return super(Num2Word_SK, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)

    def to_ordinal(self, number):
        """Convert to Slovak ordinal numbers."""
        try:
            num = int(number)
        except (ValueError, TypeError):
            return str(number)

        # Slovak ordinals
        ordinals = {
            1: 'prvý',
            2: 'druhý',
            3: 'tretí',
            4: 'štvrtý',
            5: 'piaty',
            6: 'šiesty',
            7: 'siedmy',
            8: 'ôsmy',
            9: 'deviaty',
            10: 'desiaty',
            11: 'jedenásty',
            12: 'dvanásty',
            13: 'trinásty',
            14: 'štrnásty',
            15: 'pätnásty',
            16: 'šestnásty',
            17: 'sedemnásty',
            18: 'osemnásty',
            19: 'devätnásty',
            20: 'dvadsiaty',
            30: 'tridsiaty',
            40: 'štyridsiaty',
            50: 'päťdesiaty',
            60: 'šesťdesiaty',
            70: 'sedemdesiaty',
            80: 'osemdesiaty',
            90: 'deväťdesiaty',
            100: 'stý',
            1000: 'tisíci',
        }

        if num in ordinals:
            return ordinals[num]

        # For other numbers, add 'ý' suffix to the cardinal
        # This is a simplified implementation
        cardinal = self.to_cardinal(num)
        return cardinal + 'ý'

    def _int2word(self, n):
        if n == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            word_chunk = []

            if n3 > 0:
                word_chunk.append(HUNDREDS[n3][0])

            if n2 > 1:
                word_chunk.append(TWENTIES[n2][0])

            if n2 == 1:
                word_chunk.append(TENS[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                if n2 == 0 and n3 == 0 and i in ONES[n1][2]:
                    word_chunk.append(ONES[n1][1])
                else:
                    word_chunk.append(ONES[n1][0])
            if i > 0:
                word_chunk.append(self.pluralize(x, THOUSANDS[i]))
            words.append(' '.join(word_chunk))

        return ' '.join(words)
