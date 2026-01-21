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

from __future__ import print_function, unicode_literals

import re

from . import lang_PT


def negativeword(self):
    return self.negword


class Num2Word_PT_BR(lang_PT.Num2Word_PT):
    negword = 'menos '

    CURRENCY_FORMS = {
        'BRL': (('real', 'reais'), ('centavo', 'centavos')),
        'EUR': (('euro', 'euros'), ('cêntimo', 'cêntimos')),
        'USD': (('dólar', 'dólares'), ('centavo', 'centavos')),
    }

    def __init__(self):
        super(Num2Word_PT_BR, self).__init__()
        self.negword = 'menos '

    def setup(self):
        # First call parent setup
        super(Num2Word_PT_BR, self).setup()

        # Brazilian Portuguese uses different spelling for 16, 17, 19
        self.low_numwords = [
            "vinte", "dezenove", "dezoito", "dezessete", "dezesseis",
            "quinze", "catorze", "treze", "doze", "onze", "dez",
            "nove", "oito", "sete", "seis", "cinco", "quatro", "três", "dois",
            "um", "zero"
        ]

        # Override thousand separators for Brazilian Portuguese ordinals
        # Brazilian uses short scale: bilhão = 10^9, trilhão = 10^12
        self.thousand_separators = {
            3: "milésimo",
            6: "milionésimo",
            9: "bilionésimo",  # Brazilian billion = 10^9
            12: "trilionésimo",  # Brazilian trillion = 10^12
            15: "quatrilionésimo"  # Brazilian quadrillion = 10^15
        }

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum < 1000000:
                return (ntext, cnum * nnum)
            ctext = "um"
        elif cnum == 100 and nnum > 0 and nnum < 1000:
            # In Brazilian Portuguese, 100 + any number up to 999 becomes "cento"
            # But 100 * 1000 = 100000 stays as "cem mil"
            ctext = "cento"

        if nnum > cnum:
            # Multiplicative case (e.g., "dois mil")
            if (not nnum % 1000000) and cnum > 1:
                # Handle Brazilian scale for millions
                if nnum == 1000000:
                    ntext = "milhões"
                else:
                    ntext = ntext[:-4] + "lhões"

            if nnum == 100:
                ctext = self.hundreds[cnum]
                ntext = ""
            else:
                ntext = " " + ntext

            return (ctext + ntext, cnum * nnum)
        else:
            # Additive case (e.g., "vinte e dois")
            return ("%s e %s" % (ctext, ntext), cnum + nnum)

    def to_cardinal(self, value):
        # Handle negative numbers
        if value < 0:
            return "%s%s" % (self.negword, self.to_cardinal(-value))

        # Handle billions and trillions specially for Brazilian Portuguese short scale
        # Brazil uses: bilhão = 10^9, trilhão = 10^12 (short scale)
        # Parent PT uses: bilião = 10^12, trilião = 10^18 (European long scale)

        if value >= 1000000000:
            # Handle trillions (10^12)
            if value >= 1000000000000:
                trillions, remainder = divmod(value, 1000000000000)
                if trillions == 1:
                    result = "um trilhão"
                else:
                    # Recursively convert the number of trillions
                    result = "%s trilhões" % self.to_cardinal(trillions)

                if remainder:
                    if remainder >= 1000000000:
                        # Has billions
                        billions, rest = divmod(remainder, 1000000000)
                        if billions == 1:
                            result += ", um bilhão"
                        else:
                            result += ", %s bilhões" % self.to_cardinal(billions)
                        if rest:
                            # Call parent for the rest (millions and below)
                            rest_str = super(Num2Word_PT_BR, self).to_cardinal(rest)
                            # Fix "milião" to "milhão" if it appears
                            rest_str = rest_str.replace("milião", "milhão").replace("miliões", "milhões")
                            result += " e %s" % rest_str
                    else:
                        # No billions, just add remainder
                        remainder_str = super(Num2Word_PT_BR, self).to_cardinal(remainder)
                        # Fix "milião" to "milhão" if it appears
                        remainder_str = remainder_str.replace("milião", "milhão").replace("miliões", "milhões")
                        result += " e %s" % remainder_str
                return result

            # Handle billions (10^9)
            else:
                billions, remainder = divmod(value, 1000000000)
                if billions == 1:
                    result = "um bilhão"
                else:
                    # Recursively convert the number of billions
                    result = "%s bilhões" % self.to_cardinal(billions)

                if remainder:
                    remainder_str = super(Num2Word_PT_BR, self).to_cardinal(remainder)
                    # Fix "milião" to "milhão" if it appears
                    remainder_str = remainder_str.replace("milião", "milhão").replace("miliões", "milhões")
                    # Use comma if remainder starts with hundreds (i.e., >= 100000)
                    if remainder >= 100000:
                        result += ", %s" % remainder_str
                    else:
                        result += " e %s" % remainder_str
                return result
        else:
            # For values below 1 billion but above million, handle specially
            if value >= 1000000:
                millions, remainder = divmod(value, 1000000)
                if millions == 1:
                    result = "um milhão"
                else:
                    result = "%s milhões" % super(Num2Word_PT_BR, self).to_cardinal(millions)

                if remainder:
                    # Use our own to_cardinal for remainder to ensure proper formatting
                    remainder_str = self.to_cardinal(remainder)
                    # Use comma if remainder starts with hundreds (i.e., >= 100)
                    if remainder >= 100:
                        result += ", %s" % remainder_str
                    else:
                        result += " e %s" % remainder_str
                return result
            else:
                # For values below 1 million, use parent implementation
                result = super(Num2Word_PT_BR, self).to_cardinal(value)
                # Fix "milião" to "milhão" throughout (shouldn't happen but just in case)
                result = result.replace("milião", "milhão").replace("miliões", "milhões")

        # Transforms "mil e cento e catorze" into "mil, cento e catorze"
        for ext in (
                'mil', 'milhão', 'milhões', 'bilhão', 'bilhões',
                'trilhão', 'trilhões', 'quatrilhão', 'quatrilhões'):
            # Check if pattern is "thousand-word hundreds-word e something"
            if re.search('{} \\w*ento'.format(ext), result):
                result = re.sub(
                    '({}) (\\w*entos?)'.format(ext), r'\1, \2', result, count=1
                )

        return result

    def to_currency(self, val, currency='BRL', cents=True, separator=' e', adjective=False):
        from decimal import Decimal

        # Check if this is a whole number (integer or decimal with .00)
        if isinstance(val, Decimal):
            if val % 1 == 0:
                # Convert to integer if it's a whole number
                val = int(val)
        elif isinstance(val, float):
            if val == int(val):
                val = int(val)

        # Use parent class implementation with our currency forms
        result = super(Num2Word_PT_BR, self).to_currency(
            val, currency=currency, cents=cents, separator=separator, adjective=adjective
        )

        # For Brazilian Portuguese, we need to add "de" after millions/billions/trillions
        # when they are round numbers (no thousands/hundreds after)
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
                currency_str = cr1[1] if abs(val) != 1 and len(cr1) > 1 else cr1[0]
                # Add "de" for Brazilian terms (milhão/milhões, bilhão/bilhões, trilhão/trilhões)
                for ext in ('milhão', 'milhões', 'bilhão', 'bilhões', 'trilhão', 'trilhões'):
                    if re.match('.*{} (?={})'.format(ext, currency_str), result):
                        result = result.replace(
                            '{}'.format(ext), '{} de'.format(ext), 1
                        )
            except KeyError:
                pass  # Currency not in our forms, use parent's result as-is

        return result
