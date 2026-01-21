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


class Num2Word_TA(Num2Word_Base):
    CURRENCY_FORMS = {
        'INR': (
            ('ரூபாய்', 'ரூபாய்'), ('பைசா', 'பைசா')
        ),
        'LKR': (
            ('ரூபாய்', 'ரூபாய்'), ('சதம்', 'சதம்')
        ),
        'USD': (
            ('டாலர்', 'டாலர்'), ('சென்ட்', 'சென்ட்')
        ),
        'EUR': (
            ('யூரோ', 'யூரோ'), ('சென்ட்', 'சென்ட்')
        ),
        'GBP': (
            ('பவுண்ட்', 'பவுண்ட்'), ('பென்னி', 'பென்னி')
        ),
        'SGD': (
            ('டாலர்', 'டாலர்'), ('சென்ட்', 'சென்ட்')
        ),
        'MYR': (
            ('ரிங்கிட்', 'ரிங்கிட்'), ('சென்', 'சென்')
        ),
    }

    def __init__(self):
        super(Num2Word_TA, self).__init__()

        self.ones = [
            '',
            'ஒன்று',
            'இரண்டு',
            'மூன்று',
            'நான்கு',
            'ஐந்து',
            'ஆறு',
            'ஏழு',
            'எட்டு',
            'ஒன்பது'
        ]

        self.tens = [
            '',
            'பத்து',
            'இருபது',
            'முப்பது',
            'நாற்பது',
            'ஐம்பது',
            'அறுபது',
            'எழுபது',
            'எண்பது',
            'தொண்ணூறு'
        ]

        self.teens = {
            11: 'பதினொன்று',
            12: 'பன்னிரண்டு',
            13: 'பதின்மூன்று',
            14: 'பதினான்கு',
            15: 'பதினைந்து',
            16: 'பதினாறு',
            17: 'பதினேழு',
            18: 'பதினெட்டு',
            19: 'பத்தொன்பது'
        }

        self.hundreds_special = {
            100: 'நூறு',
            200: 'இருநூறு',
            300: 'முன்னூறு',
            400: 'நானூறு',
            500: 'ஐநூறு',
            600: 'அறுநூறு',
            700: 'எழுநூறு',
            800: 'எண்ணூறு',
            900: 'தொள்ளாயிரம்'
        }

        self.scale = {
            1000: 'ஆயிரம்',
            100000: 'இலட்சம்',
            10000000: 'கோடி',
            1000000000000: 'டிரில்லியன்'
        }

        self.ordinals = {
            1: 'முதல்',
            2: 'இரண்டாம்',
            3: 'மூன்றாம்',
            4: 'நான்காம்',
            5: 'ஐந்தாம்',
            6: 'ஆறாம்',
            7: 'ஏழாம்',
            8: 'எட்டாம்',
            9: 'ஒன்பதாம்',
            10: 'பத்தாம்'
        }

        self.negword = "கழித்தல் "
        self.pointword = "புள்ளி"

    def _setup(self):
        super(Num2Word_TA, self)._setup()

    def _int_to_word(self, n):
        """
        Converts a number to words in Tamil.
        Uses Indian numbering system (lakh/crore).
        """
        if n == 0:
            return 'பூஜ்ஜியம்'

        parts = []

        # Handle crores (1 crore = 10,000,000)
        if n >= 10000000:
            crores = n // 10000000
            if crores == 1:
                parts.append('ஒரு கோடி')
            else:
                parts.append(self._int_to_word(crores) + ' கோடி')
            n %= 10000000

        # Handle lakhs (1 lakh = 100,000)
        if n >= 100000:
            lakhs = n // 100000
            if lakhs == 1:
                parts.append('ஒரு இலட்சம்')
            else:
                parts.append(self._int_to_word(lakhs) + ' இலட்சம்')
            n %= 100000

        # Handle thousands
        if n >= 1000:
            thousands = n // 1000
            if thousands == 1:
                parts.append('ஆயிரம்')
            else:
                parts.append(self._int_to_word(thousands) + ' ஆயிரம்')
            n %= 1000

        # Handle hundreds with special forms
        if n >= 100:
            hundreds_val = (n // 100) * 100
            if hundreds_val in self.hundreds_special:
                parts.append(self.hundreds_special[hundreds_val])
            else:
                parts.append(self.ones[n // 100] + ' நூறு')
            n %= 100

        # Handle special case for teens (11-19)
        if 10 < n < 20:
            parts.append(self.teens[n])
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
            return 'பூஜ்ஜியம்'

        if n < 0:
            return self.negword + self._int_to_word(-n)

        return self._int_to_word(n)

    def _int_to_ordinal(self, n):
        """Convert to ordinal number."""
        if n == 0:
            return 'பூஜ்ஜியம்'

        # Special cases for first ten ordinals
        if n in self.ordinals:
            return self.ordinals[n]

        # For other numbers, add "-ஆவது" suffix
        return self._int_to_cardinal(n) + 'ஆவது'

    def to_cardinal(self, n):
        try:
            if isinstance(n, str):
                n = int(n)

            return self._int_to_cardinal(n)
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

            # In Tamil, ordinal numbers use "-ஆவது" suffix
            # But for numeric form, use -வது
            return str(n) + '-வது'
        except BaseException:
            return str(n) + '-வது'

    def to_currency(self, n, currency='INR'):
        try:
            # Check if value has fractional cents
            from decimal import Decimal
            decimal_val = Decimal(str(n))
            has_fractional_cents = (decimal_val * 100) % 1 != 0

            left, right, is_negative = parse_currency_parts(n, is_int_with_cents=False,
                                                            keep_precision=has_fractional_cents)

            if currency not in self.CURRENCY_FORMS:
                raise NotImplementedError(
                    'Currency code "%s" not implemented for "%s"' %
                    (currency, self.__class__.__name__))

            cr_major, cr_minor = self.CURRENCY_FORMS[currency]

            result = []

            if is_negative:
                result.append(self.negword.strip())

            left_words = self._int_to_cardinal(left)
            result.append(left_words)
            result.append(cr_major[0])

            # Handle paise/cents if non-zero
            if right > 0:
                # Handle fractional paise
                from decimal import Decimal
                if isinstance(right, Decimal):
                    # Convert fractional paise (e.g., 65.3 paise)
                    right_words = self.to_cardinal(float(right))
                else:
                    right_words = self._int_to_cardinal(right)
                result.append(right_words)
                result.append(cr_minor[0])

            return ' '.join(result)
        except NotImplementedError:
            raise
        except BaseException:
            return str(n) + ' ' + currency

    def to_year(self, n):
        """Convert to year representation."""
        if n < 1000:
            return self._int_to_cardinal(n)
        elif n < 2000:
            # Years like 1999 -> "ஆயிரத்து தொள்ளாயிரத்து தொண்ணூற்று ஒன்பது"
            thousands = n // 1000
            remainder = n % 1000
            result = 'ஆயிரத்து'
            if remainder > 0:
                result += ' ' + self._int_to_cardinal(remainder)
            return result
        else:
            # Years like 2023 -> "இரண்டாயிரத்து இருபத்து மூன்று"
            thousands = n // 1000
            remainder = n % 1000
            result = self._int_to_cardinal(thousands) + ' ஆயிரத்து'
            if remainder > 0:
                result += ' ' + self._int_to_cardinal(remainder)
            return result
