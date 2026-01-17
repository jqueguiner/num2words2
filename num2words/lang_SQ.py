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


class Num2Word_SQ(Num2Word_Base):
    CURRENCY_FORMS = {
        'ALL': (('lek', 'lekë'), ('qindarkë', 'qindarkë')),
        'EUR': (('euro', 'euro'), ('cent', 'centë')),
        'USD': (('dollar', 'dollarë'), ('cent', 'centë')),
        'GBP': (('paund', 'paund'), ('peni', 'pence')),
        'CHF': (('frank zviceran', 'franka zvicer'), ('centim', 'centimë')),
        'JPY': (('jen', 'jenë'), ('sen', 'senë')),
        'RUB': (('rubël', 'rubla'), ('kopek', 'kopekë')),
    }

    def setup(self):
        self.negword = "minus "
        self.pointword = "presje"
        self.exclude_title = ["e", "presje", "minus"]

        self.high_numwords = ["trilion", "miliard", "milion"]
        
        self.mid_numwords = [
            (1000, "mijë"),
            (100, "qind"),
            (90, "nëntëdhjetë"),
            (80, "tetëdhjetë"),
            (70, "shtatëdhjetë"),
            (60, "gjashtëdhjetë"),
            (50, "pesëdhjetë"),
            (40, "dyzet"),
            (30, "tridhjetë"),
            (20, "njëzet"),
        ]
        
        self.low_numwords = [
            "nëntëmbëdhjetë",  # 19
            "tetëmbëdhjetë",   # 18
            "shtatëmbëdhjetë", # 17
            "gjashtëmbëdhjetë",# 16
            "pesëmbëdhjetë",   # 15
            "katërmbëdhjetë",  # 14
            "trembëdhjetë",    # 13
            "dymbëdhjetë",     # 12
            "njëmbëdhjetë",    # 11
            "dhjetë",          # 10
            "nëntë",           # 9
            "tetë",            # 8
            "shtatë",          # 7
            "gjashtë",         # 6
            "pesë",            # 5
            "katër",           # 4
            "tre",             # 3
            "dy",              # 2
            "një",             # 1
            "zero"             # 0
        ]

        # Ordinal forms
        self.ordinal_forms = {
            0: "i zeroi",
            1: "i pari",
            2: "i dyti", 
            3: "i treti",
            4: "i katërti",
            5: "i pesti",
            6: "i gjashti",
            7: "i shtati",
            8: "i teti",
            9: "i nënti",
            10: "i dhjeti",
            20: "i njezeti",
            100: "i një qindi",
            1000: "i një mijti",
        }

    def set_high_numwords(self, high):
        max = 3 + 3 * len(high)
        for word, n in zip(high, range(max, 3, -3)):
            self.cards[10 ** n] = word

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum == 1000:
                return ("një mijë", 1000)
            if nnum == 100:
                return ("një qind", 100)
            if nnum < 100:
                return next
            ctext = "një"

        if nnum > cnum:
            if nnum >= 1000000:
                return ("%s %s" % (ctext, ntext), cnum * nnum)
            elif nnum >= 1000:
                return ("%s %s" % (ctext, ntext), cnum * nnum)
            elif nnum == 100:
                return ("%s %s" % (ctext, ntext), cnum * nnum)

        if nnum < cnum:
            if cnum >= 1000:
                # For thousands, always use "e" connector for smaller numbers
                return ("%s e %s" % (ctext, ntext), cnum + nnum)
            elif cnum >= 100:
                # For hundreds, use "e" for anything smaller
                return ("%s e %s" % (ctext, ntext), cnum + nnum)
            else:
                # For tens (20, 30, etc.), use "e" for units
                if cnum >= 20 and nnum < 10:
                    return ("%s e %s" % (ctext, ntext), cnum + nnum)
                return ("%s%s" % (ctext, ntext), cnum + nnum)

        return ("%s %s" % (ctext, ntext), cnum + nnum)

    def to_cardinal(self, value):
        if value == 0:
            return 'zero'

        result = super(Num2Word_SQ, self).to_cardinal(value)
        return result

    def to_ordinal(self, value):
        if value in self.ordinal_forms:
            return self.ordinal_forms[value]

        # For compound ordinals, use pattern "i + cardinal + suffix"
        if value <= 10:
            return self.ordinal_forms.get(value, "i " + self.to_cardinal(value))
        elif value == 20:
            return "i njezeti"
        elif value == 100:
            return "i një qindi"
        elif value == 1000:
            return "i një mijti"
        else:
            # For other numbers, use pattern
            cardinal = self.to_cardinal(value)
            return "i " + cardinal

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        
        # Albanian ordinal suffixes based on ending
        if value % 10 == 1 and value % 100 != 11:
            suffix = "-shi"
        elif value % 10 == 2 and value % 100 != 12:
            suffix = "-ri"
        elif value % 10 == 3 and value % 100 != 13:
            suffix = "-ti"
        else:
            suffix = "-ti"
            
        return str(value) + suffix

    def pluralize(self, n, forms):
        """Albanian plural rules"""
        if not forms:
            return ''
            
        if len(forms) == 1:
            return forms[0]
            
        if len(forms) >= 2:
            # In Albanian, use singular for 1, plural for everything else
            if n == 1:
                return forms[0]
            else:
                return forms[1]
                
        return forms[0]

    def to_currency(self, val, currency='ALL', cents=True, separator=',',
                    adjective=False):
        """
        Convert a value to Albanian currency format.
        """
        result = []
        is_negative = val < 0
        val = abs(val)

        if currency in self.CURRENCY_FORMS:
            if isinstance(val, float):
                # Handle decimal values
                whole = int(val)
                cents_value = int(round((val - whole) * 100))
            else:
                whole = int(val)
                cents_value = 0

            # Add the main currency
            if whole > 0:
                result.append(self.to_cardinal(whole))
                result.append(self.pluralize(whole, self.CURRENCY_FORMS[currency][0]))

            # Add cents if present and cents=True
            if cents_value > 0 and cents:
                if whole > 0:
                    # Join the main currency part first, then add separator
                    main_part = ' '.join(result)
                    result = [main_part + separator]
                result.append(self.to_cardinal(cents_value))
                result.append(self.pluralize(cents_value, self.CURRENCY_FORMS[currency][1]))

            if is_negative:
                result.insert(0, self.negword.strip())

            return ' '.join(result)
        else:
            # Fallback for unknown currency
            return self.to_cardinal(val)

    def to_year(self, value, **kwargs):
        """Convert number to year format (same as cardinal for Albanian)."""
        return self.to_cardinal(value)