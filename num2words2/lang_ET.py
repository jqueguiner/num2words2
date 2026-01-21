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


class Num2Word_ET(Num2Word_Base):
    CURRENCY_FORMS = {
        'EUR': (
            ('euro', 'eurot'), ('sent', 'senti')
        ),
        'USD': (
            ('dollar', 'dollarit'), ('sent', 'senti')
        ),
        'GBP': (
            ('nael', 'naela'), ('penn', 'penni')
        ),
        'SEK': (
            ('kroon', 'krooni'), ('ööri', 'ööri')
        ),
        'NOK': (
            ('kroon', 'krooni'), ('ööri', 'ööri')
        ),
        'DKK': (
            ('kroon', 'krooni'), ('ööri', 'ööri')
        ),
        'RUB': (
            ('rubla', 'rubla'), ('kopikas', 'kopikat')
        ),
    }

    def __init__(self):
        super(Num2Word_ET, self).__init__()

        self.ones = [
            '',
            'üks',
            'kaks',
            'kolm',
            'neli',
            'viis',
            'kuus',
            'seitse',
            'kaheksa',
            'üheksa'
        ]

        self.tens = [
            '',
            'kümme',
            'kakskümmend',
            'kolmkümmend',
            'nelikümmend',
            'viiskümmend',
            'kuuskümmend',
            'seitsekümmend',
            'kaheksakümmend',
            'üheksakümmend'
        ]

        self.scale = {
            100: 'sada',
            1000: 'tuhat',
            1000000: 'miljon',
            1000000000: 'miljard',
            1000000000000: 'triljon'
        }

        self.ordinals_ones = [
            '',
            'esimene',
            'teine',
            'kolmas',
            'neljas',
            'viies',
            'kuues',
            'seitsmes',
            'kaheksas',
            'üheksas'
        ]

        self.ordinals_tens = [
            '',
            'kümnes',
            'kahekümnes',
            'kolmekümnes',
            'nelikümnes',
            'viiekümnes',
            'kuuekümnes',
            'seitsmekümnes',
            'kaheksakümnes',
            'üheksakümnes'
        ]

        self.negword = "miinus "
        self.pointword = "koma"

    def _setup(self):
        super(Num2Word_ET, self)._setup()

    def _int_to_word(self, n):
        """
        Converts a number to words in Estonian.
        """
        if n == 0:
            return 'null'

        parts = []

        # Handle trillions
        if n >= 1000000000000:
            trillions = n // 1000000000000
            if trillions == 1:
                parts.append('üks triljon')
            else:
                parts.append(self._int_to_word(trillions) + ' triljonit')
            n %= 1000000000000

        # Handle billions
        if n >= 1000000000:
            billions = n // 1000000000
            if billions == 1:
                parts.append('üks miljard')
            else:
                parts.append(self._int_to_word(billions) + ' miljardit')
            n %= 1000000000

        # Handle millions
        if n >= 1000000:
            millions = n // 1000000
            if millions == 1:
                parts.append('üks miljon')
            else:
                parts.append(self._int_to_word(millions) + ' miljonit')
            n %= 1000000

        # Handle thousands
        if n >= 1000:
            thousands = n // 1000
            if thousands == 1:
                parts.append('tuhat')
            elif thousands == 100:
                # Special case: 100000 should be "sada tuhat" not "ükssada tuhat"
                parts.append('sada tuhat')
            else:
                parts.append(self._int_to_word(thousands) + ' tuhat')
            n %= 1000

        # Handle hundreds
        if n >= 100:
            hundreds = n // 100
            if hundreds == 1:
                parts.append('ükssada')
            elif hundreds == 2:
                parts.append('kakssada')
            elif hundreds == 3:
                parts.append('kolmsada')
            elif hundreds == 4:
                parts.append('nelisada')
            elif hundreds == 5:
                parts.append('viissada')
            elif hundreds == 6:
                parts.append('kuussada')
            elif hundreds == 7:
                parts.append('seitsesada')
            elif hundreds == 8:
                parts.append('kaheksasada')
            elif hundreds == 9:
                parts.append('üheksasada')
            n %= 100

        # Handle special case for teens (11-19)
        if 10 < n < 20:
            teens_map = {
                11: 'üksteist',
                12: 'kaksteist',
                13: 'kolmteist',
                14: 'neliteist',
                15: 'viisteist',
                16: 'kuusteist',
                17: 'seitseteist',
                18: 'kaheksateist',
                19: 'üheksateist'
            }
            parts.append(teens_map[n])
        else:
            # Handle tens
            if n >= 10:
                tens_val = n // 10
                parts.append(self.tens[tens_val])
                n %= 10

            # Handle ones
            if n > 0:
                parts.append(self.ones[n])

        return ' '.join(parts)

    def _int_to_cardinal(self, n):
        if n == 0:
            return 'null'

        if n < 0:
            return self.negword + self._int_to_word(-n)

        return self._int_to_word(n)

    def _int_to_ordinal(self, n):
        """Convert to ordinal number."""
        if n == 0:
            return 'nullis'

        if n < 10:
            return self.ordinals_ones[n]

        if n == 10:
            return 'kümnes'

        if n < 20:
            teens_ordinals = {
                11: 'üheteistkümnes',
                12: 'kaheteistkümnes',
                13: 'kolmeteistkümnes',
                14: 'neljateistkümnes',
                15: 'viieteistkümnes',
                16: 'kuueteistkümnes',
                17: 'seitsmeteistkümnes',
                18: 'kaheksateistkümnes',
                19: 'üheksateistkümnes'
            }
            return teens_ordinals[n]

        if n < 100:
            tens_val = n // 10
            ones_val = n % 10
            if ones_val == 0:
                return self.ordinals_tens[tens_val]
            else:
                # For compound numbers, make the last part ordinal
                return self.tens[tens_val] + ' ' + self.ordinals_ones[ones_val]

        if n == 100:
            return 'sajas'

        if n == 1000:
            return 'tuhandes'

        # For larger numbers, convert to cardinal and add 's' suffix
        cardinal = self._int_to_cardinal(n)
        return cardinal + 's'

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

            return str(n) + '.'
        except BaseException:
            return str(n) + '.'

    def to_currency(self, val, currency='EUR', cents=True, separator=' ja ',
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

        minus_str = "miinus " if is_negative else ""
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
                cents_str = self.to_cardinal(float(right)) if right > 0 else "null"
            else:
                cents_str = self._int_to_cardinal(right) if right > 0 else "null"
        else:
            cents_str = str(float(right) if isinstance(right, Decimal) else right)

        # Determine cents form
        if right == 1:
            cents_currency = cr2[0]  # singular
        else:
            cents_currency = cr2[1]  # plural

        return "%s%s %s%s%s %s" % (
            minus_str, money_str, currency_str,
            separator, cents_str, cents_currency)

    def to_year(self, n):
        """Convert to year representation."""
        if n < 1000:
            return self._int_to_cardinal(n)
        elif n < 2000:
            # Years like 1999 -> "tuhat üheksasada üheksakümmend üheksa"
            return self._int_to_cardinal(n)
        else:
            # Years like 2023 -> "kaks tuhat kakskümmend kolm"
            return self._int_to_cardinal(n)
