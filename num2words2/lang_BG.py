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


class Num2Word_BG(Num2Word_Base):
    CURRENCY_FORMS = {
        'BGN': (
            ('лев', 'лева'), ('стотинка', 'стотинки')
        ),
        'EUR': (
            ('евро', 'евро'), ('цент', 'цента')
        ),
        'USD': (
            ('долар', 'долара'), ('цент', 'цента')
        ),
        'GBP': (
            ('паунд', 'паунда'), ('пени', 'пенса')
        ),
        'JPY': (
            ('йена', 'йени'), ('сен', 'сена')
        ),
    }

    def __init__(self):
        super(Num2Word_BG, self).__init__()

        self.ones = {
            0: 'нула',
            1: 'едно',
            2: 'две',
            3: 'три',
            4: 'четири',
            5: 'пет',
            6: 'шест',
            7: 'седем',
            8: 'осем',
            9: 'девет'
        }

        self.ones_masculine = {
            1: 'един',
            2: 'два'
        }

        self.ones_feminine = {
            1: 'една',
            2: 'две'
        }

        self.tens = {
            10: 'десет',
            11: 'единадесет',
            12: 'дванадесет',
            13: 'тринадесет',
            14: 'четиринадесет',
            15: 'петнадесет',
            16: 'шестнадесет',
            17: 'седемнадесет',
            18: 'осемнадесет',
            19: 'деветнадесет',
            20: 'двадесет',
            30: 'тридесет',
            40: 'четиридесет',
            50: 'петдесет',
            60: 'шестдесет',
            70: 'седемдесет',
            80: 'осемдесет',
            90: 'деветдесет'
        }

        self.scale = {
            100: ('сто', 'ста'),
            1000: ('хиляда', 'хиляди'),
            1000000: ('милион', 'милиона'),
            1000000000: ('милиард', 'милиарда'),
            1000000000000: ('трилион', 'трилиона')
        }

        self.ordinals = {
            1: 'първи',
            2: 'втори',
            3: 'трети',
            4: 'четвърти',
            5: 'пети',
            6: 'шести',
            7: 'седми',
            8: 'осми',
            9: 'девети',
            10: 'десети',
            11: 'единадесети',
            12: 'дванадесети',
            13: 'тринадесети',
            14: 'четиринадесети',
            15: 'петнадесети',
            16: 'шестнадесети',
            17: 'седемнадесети',
            18: 'осемнадесети',
            19: 'деветнадесети',
            20: 'двадесети',
            30: 'тридесети',
            40: 'четиридесети',
            50: 'петдесети',
            60: 'шестдесети',
            70: 'седемдесети',
            80: 'осемдесети',
            90: 'деветдесети',
            100: 'стотен',
            1000: 'хиляден'
        }

        self.negword = "минус "
        self.pointword = "точка"

    def _setup(self):
        super(Num2Word_BG, self)._setup()

    def _int_to_word(self, n, masculine=False, feminine=False):
        """
        Converts a number to words in Bulgarian.
        Args:
            n: integer to convert
            masculine: whether to use masculine form for ones
            feminine: whether to use feminine form for ones
        """
        if n == 0:
            return self.ones[0]

        parts = []

        # Handle billions
        if n >= 1000000000:
            billions = n // 1000000000
            if billions == 1:
                parts.append('един милиард')
            elif billions == 2:
                parts.append('два милиарда')
            else:
                parts.append(self._int_to_word(billions) + ' милиарда')
            n %= 1000000000

        # Handle millions
        if n >= 1000000:
            millions = n // 1000000
            if millions == 1:
                parts.append('един милион')
            elif millions == 2:
                parts.append('два милиона')
            else:
                parts.append(self._int_to_word(millions) + ' милиона')
            n %= 1000000

        # Handle thousands
        if n >= 1000:
            thousands = n // 1000
            if thousands == 1:
                parts.append('хиляда')
            elif thousands == 2:
                parts.append('две хиляди')
            else:
                parts.append(self._int_to_word(thousands) + ' хиляди')
            n %= 1000

        # Handle hundreds
        if n >= 100:
            hundreds = n // 100
            if hundreds == 1:
                parts.append('сто')
            elif hundreds == 2:
                parts.append('двеста')
            elif hundreds == 3:
                parts.append('триста')
            else:
                parts.append(self.ones[hundreds] + 'стотин')
            n %= 100

        # Handle tens and ones
        if n >= 20:
            tens = (n // 10) * 10
            parts.append(self.tens[tens])
            n %= 10
            if n > 0:
                parts.append('и')
                if feminine and n in self.ones_feminine:
                    parts.append(self.ones_feminine[n])
                elif masculine and n in self.ones_masculine:
                    parts.append(self.ones_masculine[n])
                else:
                    parts.append(self.ones[n])
        elif n >= 10:
            parts.append(self.tens[n])
        elif n > 0:
            if feminine and n in self.ones_feminine:
                parts.append(self.ones_feminine[n])
            elif masculine and n in self.ones_masculine:
                parts.append(self.ones_masculine[n])
            else:
                parts.append(self.ones[n])

        return ' '.join(parts)

    def _int_to_cardinal(self, n):
        if n == 0:
            return self.ones[0]

        if n < 0:
            return self.negword + self._int_to_word(-n)

        return self._int_to_word(n, masculine=True)

    def _int_to_ordinal(self, n):
        if n in self.ordinals:
            return self.ordinals[n]

        # For complex numbers, form ordinal by adding -ти/-ен to cardinal
        cardinal = self._int_to_cardinal(n)

        # Handle different endings
        if cardinal.endswith('един'):
            return cardinal[:-4] + 'първи'
        elif cardinal.endswith('два'):
            return cardinal[:-3] + 'втори'
        elif cardinal.endswith('три'):
            return cardinal[:-3] + 'трети'
        elif cardinal.endswith('т'):
            return cardinal + 'и'
        else:
            return cardinal + 'ти'

    def to_cardinal(self, n):
        try:
            if isinstance(n, str):
                n = float(n)

            # Handle floats with decimal places
            if isinstance(n, float) and n != int(n):
                pre, post = self.float2tuple(n)

                # Handle negative decimals
                if n < 0:
                    result = self.negword
                    pre = abs(pre)
                else:
                    result = ""

                # Integer part
                result += self._int_to_cardinal(pre)

                # Decimal part
                if self.precision > 0:
                    result += " " + self.pointword

                    # Convert post to string with proper padding
                    post_str = str(post)
                    post_str = '0' * (self.precision - len(post_str)) + post_str

                    # Say each digit individually
                    for digit in post_str:
                        result += " " + self.ones[int(digit)]

                return result.strip()

            # For integers
            if n < 0:
                return self.negword + self.to_cardinal(-n)

            return self._int_to_cardinal(int(n))
        except BaseException:
            return self._int_to_cardinal(int(n))

    def to_ordinal(self, n):
        try:
            if isinstance(n, str):
                n = int(n)

            return self._int_to_ordinal(n)
        except BaseException:
            return self._int_to_ordinal(int(n))

    def to_ordinal_num(self, n):
        try:
            if isinstance(n, str):
                n = int(n)

            # Bulgarian ordinal suffixes
            if n % 100 in [11, 12, 13, 14, 15, 16, 17, 18, 19]:
                return str(n) + '-ти'
            elif n % 10 == 1:
                return str(n) + '-ви'
            elif n % 10 == 2:
                return str(n) + '-ри'
            elif n % 10 in [7, 8]:
                return str(n) + '-ми'
            else:
                return str(n) + '-ти'
        except BaseException:
            return str(n) + '-ти'

    def to_currency(self, val, currency='BGN', cents=True, separator=' и',
                    adjective=False):
        """Convert a number to currency words."""
        # Track if input was originally an integer
        is_integer_input = isinstance(val, int)

        # Check if value has fractional cents
        if not is_integer_input:
            from decimal import Decimal
            decimal_val = Decimal(str(val))
            has_fractional_cents = (decimal_val * 100) % 1 != 0
        else:
            has_fractional_cents = False

        left, right, is_negative = parse_currency_parts(val, is_int_with_cents=False,
                                                        keep_precision=has_fractional_cents)

        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]
        except KeyError:
            raise NotImplementedError(
                'Currency "%s" not implemented for "%s"' % (
                    currency, self.__class__.__name__))

        minus_str = "минус " if is_negative else ""
        money_str = self._int_to_cardinal(left)

        # Determine currency form based on the number
        if left == 1:
            currency_str = cr1[0]  # singular
        else:
            currency_str = cr1[1]  # plural

        # For integers, don't show cents
        if is_integer_input:
            return "%s%s %s" % (minus_str, money_str, currency_str)

        # For floats, always show cents (even if zero)
        if cents:
            # Handle fractional cents
            from decimal import Decimal
            if isinstance(right, Decimal):
                # Convert fractional cents (e.g., 65.3 cents)
                cents_str = self.to_cardinal(float(right)) if right > 0 else self.ones[0]
            else:
                cents_str = self._int_to_cardinal(right) if right > 0 else self.ones[0]
        else:
            cents_str = str(float(right) if isinstance(right, Decimal) else right)

        # Determine cents form
        if right == 1:
            cents_currency = cr2[0]  # singular
        else:
            cents_currency = cr2[1]  # plural

        return "%s%s %s%s %s %s" % (
            minus_str, money_str, currency_str,
            separator, cents_str, cents_currency)

    def to_year(self, n):
        if n < 1000:
            return self._int_to_cardinal(n)
        elif n < 2000:
            # Years like 1999 -> "хиляда деветстотин деветдесет и девет"
            thousands = n // 1000
            remainder = n % 1000
            if thousands == 1:
                result = 'хиляда'
            else:
                result = self._int_to_cardinal(thousands) + ' хиляди'

            if remainder > 0:
                result += ' ' + self._int_to_cardinal(remainder)
            return result
        else:
            # Years like 2023 -> "две хиляди двадесет и три"
            return self._int_to_cardinal(n)
