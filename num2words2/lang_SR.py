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
from .currency import parse_currency_parts
from .utils import get_digits, splitbyx

ZERO = ('нула',)

ONES = {
    1: ('један', 'једна'),
    2: ('два', 'две'),
    3: ('три', 'три'),
    4: ('четири', 'четири'),
    5: ('пет', 'пет'),
    6: ('шест', 'шест'),
    7: ('седам', 'седам'),
    8: ('осам', 'осам'),
    9: ('девет', 'девет'),
}

TENS = {
    0: ('десет',),
    1: ('једанаест',),
    2: ('дванаест',),
    3: ('тринаест',),
    4: ('четрнаест',),
    5: ('петнаест',),
    6: ('шеснаест',),
    7: ('седамнаест',),
    8: ('осамнаест',),
    9: ('деветнаест',),
}

TWENTIES = {
    2: ('двадесет',),
    3: ('тридесет',),
    4: ('четрдесет',),
    5: ('педесет',),
    6: ('шездесет',),
    7: ('седамдесет',),
    8: ('осамдесет',),
    9: ('деведесет',),
}

HUNDREDS = {
    1: ('сто',),
    2: ('двеста',),
    3: ('триста',),
    4: ('четиристо',),
    5: ('петсто',),
    6: ('шесто',),
    7: ('седамсто',),
    8: ('осамсто',),
    9: ('деветсто',),
}

SCALE = {
    0: ('', '', '', False),
    1: ('хиљада', 'хиљаде', 'хиљада', True),  # 10^3
    2: ('милион', 'милиона', 'милиона', False),  # 10^6
    3: ('милијарда', 'милијарде', 'милијарди', True),  # 10^9 - using long scale
    4: ('билион', 'билиона', 'билиона', False),  # 10^12
    5: ('билијарда', 'билијарде', 'билијарди', True),  # 10^15
    6: ('трилион', 'трилиона', 'трилиона', False),  # 10^18
    7: ('трилијарда', 'трилијарде', 'трилијарди', True),  # 10^21
    8: ('квадрилион', 'квадрилиона', 'квадрилиона', False),  # 10^24
    9: ('квадрилијарда', 'квадрилијарде', 'квадрилијарди', True),  # 10^27
    10: ('квинтилион', 'квинтилиона', 'квинтилиона', False),  # 10^30
}


class Num2Word_SR(Num2Word_Base):
    CURRENCY_FORMS = {
        'RUB': (
            ('rublja', 'rublje', 'rublji', True),
            ('kopejka', 'kopejke', 'kopejki', True)
        ),
        'EUR': (
            ('evro', 'evra', 'evra', False),
            ('cent', 'centa', 'centi', False)
        ),
        'RSD': (
            ('dinar', 'dinara', 'dinara', False),
            ('para', 'pare', 'para', True)
        ),
    }

    def setup(self):
        self.negword = "минус"
        self.pointword = "запета"

    def to_cardinal(self, number, feminine=False):
        n = str(number).replace(',', '.')
        if '.' in n:
            is_negative = n.startswith('-')
            abs_n = n[1:] if is_negative else n
            left, right = abs_n.split('.')
            leading_zero_count = len(right) - len(right.lstrip('0'))
            decimal_part = ((ZERO[0] + ' ') * leading_zero_count +
                            self._int2word(int(right), feminine))
            result = u'%s %s %s' % (
                self._int2word(int(left), feminine),
                self.pointword,
                decimal_part
            )
            if is_negative:
                result = self.negword + ' ' + result
            return result
        else:
            return self._int2word(int(n), feminine)

    def pluralize(self, number, forms):
        if number % 100 < 10 or number % 100 > 20:
            if number % 10 == 1:
                form = 0
            elif 1 < number % 10 < 5:
                form = 1
            else:
                form = 2
        else:
            form = 2
        return forms[form]

    def to_ordinal(self, number):
        """Convert to Serbian ordinal numbers (Cyrillic)."""
        try:
            num = int(number)
        except (ValueError, TypeError):
            return str(number)

        # Serbian ordinals in Cyrillic
        ordinals = {
            1: 'први',
            2: 'други',
            3: 'трећи',
            4: 'четврти',
            5: 'пети',
            6: 'шести',
            7: 'седми',
            8: 'осми',
            9: 'девети',
            10: 'десети',
            11: 'једанаести',
            12: 'дванаести',
            13: 'тринаести',
            14: 'четрнаести',
            15: 'петнаести',
            16: 'шеснаести',
            17: 'седамнаести',
            18: 'осамнаести',
            19: 'деветнаести',
            20: 'двадесети',
            30: 'тридесети',
            40: 'четрдесети',
            50: 'педесети',
            60: 'шездесети',
            70: 'седамдесети',
            80: 'осамдесети',
            90: 'деведесети',
            100: 'стоти',
            1000: 'хиљадити',
        }

        if num in ordinals:
            return ordinals[num]

        # For other numbers, add 'и' suffix to the cardinal
        # This is a simplified implementation
        cardinal = self.to_cardinal(num)
        return cardinal + 'и'

    def _cents_verbose(self, number, currency):
        return self._int2word(
            number,
            self.CURRENCY_FORMS[currency][1][-1]
        )

    def _int2word(self, number, feminine=False):
        if number < 0:
            return ' '.join([self.negword, self._int2word(abs(number))])

        if number == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(number), 3))
        chunk_len = len(chunks)
        for chunk in chunks:
            chunk_len -= 1
            digit_right, digit_mid, digit_left = get_digits(chunk)

            if digit_left > 0:
                words.append(HUNDREDS[digit_left][0])

            if digit_mid > 1:
                words.append(TWENTIES[digit_mid][0])

            if digit_mid == 1:
                words.append(TENS[digit_right][0])
            elif digit_right > 0:
                # Skip 'један' for thousands (1000, 1001, etc.)
                if not (chunk_len > 0 and chunk == 1):
                    is_feminine = feminine or SCALE[chunk_len][-1]
                    gender_idx = int(is_feminine)
                    words.append(
                        ONES[digit_right][gender_idx]
                    )

            if chunk_len > 0 and chunk != 0:
                words.append(self.pluralize(chunk, SCALE[chunk_len]))

        return ' '.join(words)

    def to_currency(self, val, currency='RSD', cents=True, separator=',',
                    adjective=False):
        # Handle integers specially - no cents
        if isinstance(val, int):
            # Get major currency part only
            left, right, is_negative = parse_currency_parts(val, is_int_with_cents=False)
            words = []
            if is_negative:
                words.append('минус')
            words.append(self.to_cardinal(left))

            # Add currency name based on the number
            if left % 10 == 1 and left % 100 != 11:
                words.append('динар')
            elif 2 <= left % 10 <= 4 and not (12 <= left % 100 <= 14):
                words.append('динара')
            else:
                words.append('динара')

            return ' '.join(words)

        # For floats, use parent implementation
        return super().to_currency(val, currency=currency, cents=cents,
                                   separator=separator, adjective=adjective)
