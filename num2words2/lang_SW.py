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


class Num2Word_SW(Num2Word_Base):
    CURRENCY_FORMS = {
        'TZS': (('shilingi', 'shilingi'), ('senti', 'senti')),  # Tanzanian Shilling
        'KES': (('shilingi', 'shilingi'), ('senti', 'senti')),  # Kenyan Shilling
        'UGX': (('shilingi', 'shilingi'), ('senti', 'senti')),  # Ugandan Shilling

        'USD': (('dola', 'dola'), ('senti', 'senti')),          # US Dollar
        'EUR': (('yuro', 'yuro'), ('senti', 'senti')),          # Euro
        'GBP': (('pauni', 'pauni'), ('peni', 'peni')),          # British Pound
    }

    def setup(self):
        self.negword = "hasi "
        self.pointword = "nukta"

        # High-level numwords for large numbers
        self.high_numwords = ["trilioni"]

        self.mid_numwords = [
            (1000000000, "bilioni"),
            (1000000, "milioni"),
            (100000, "laki"),
            (1000, "elfu"),
            (100, "mia"),
            (90, "tisini"),
            (80, "themanini"),
            (70, "sabini"),
            (60, "sitini"),
            (50, "hamsini"),
            (40, "arobaini"),
            (30, "thelathini"),
            (20, "ishirini")
        ]

        self.low_numwords = [
            "kumi na tisa",  # 19
            "kumi na nane",  # 18
            "kumi na saba",  # 17
            "kumi na sita",  # 16
            "kumi na tano",  # 15
            "kumi na nne",   # 14
            "kumi na tatu",  # 13
            "kumi na mbili",  # 12
            "kumi na moja",  # 11
            "kumi",          # 10
            "tisa",          # 9
            "nane",          # 8
            "saba",          # 7
            "sita",          # 6
            "tano",          # 5
            "nne",           # 4
            "tatu",          # 3
            "mbili",         # 2
            "moja",          # 1
            "sifuri"         # 0
        ]

        # Ordinal mappings
        self.ordinal_words = {
            "moja": "kwanza",
            "mbili": "pili",
            "tatu": "tatu",
            "nne": "nne",
            "tano": "tano",
            "sita": "sita",
            "saba": "saba",
            "nane": "nane",
            "tisa": "tisa",
            "kumi": "kumi",
        }

    def set_high_numwords(self, high):
        """Set high numwords for large numbers."""
        cap = 9 + 9 * len(high)
        for word, n in zip(high, range(cap, 8, -9)):
            self.cards[10 ** n] = word

    def merge(self, lpair, rpair):
        """Merge two number parts using Swahili grammar rules."""
        ltext, lnum = lpair
        rtext, rnum = rpair

        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif 100 > lnum > rnum:
            return ("%s na %s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100 > rnum:
            return ("%s na %s" % (ltext, rtext), lnum + rnum)
        elif rnum >= 1000000:
            # For millions/billions: "milioni moja", "bilioni mbili", etc.
            return ("%s %s" % (rtext, ltext), lnum * rnum)
        elif rnum >= 1000:
            # For thousands: "elfu moja", "elfu mbili", etc.
            if lnum < 1000:
                return ("%s %s" % (rtext, ltext), lnum * rnum)
            else:
                # When combining with other thousands, use "na"
                return ("%s na %s" % (ltext, rtext), lnum + rnum)
        elif rnum >= 100:
            # For hundreds: "mia moja", "mia mbili", etc.
            if lnum < 100:
                return ("%s %s" % (rtext, ltext), lnum * rnum)
            else:
                # When combining with other hundreds or larger, use "na"
                return ("%s na %s" % (ltext, rtext), lnum + rnum)
        elif rnum > lnum:
            return ("%s %s" % (ltext, rtext), lnum * rnum)
        return ("%s na %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal(self, value):
        """Convert number to ordinal form."""
        self.verify_ordinal(value)
        cardinal_text = self.to_cardinal(value)

        # Check if we have a special ordinal form
        if cardinal_text in self.ordinal_words:
            return f"wa {self.ordinal_words[cardinal_text]}"

        # For ordinals, prefix with "wa" (of/the)
        return f"wa {cardinal_text}"

    def to_ordinal_num(self, value):
        """Convert number to ordinal number format."""
        self.verify_ordinal(value)
        return f"{value}."

    def to_year(self, value, **kwargs):
        """Convert number to year format."""
        return self.to_cardinal(value)

    def pluralize(self, number, forms):
        """Handle pluralization - Swahili doesn't change form much."""
        # Swahili typically doesn't change the noun form for plurals
        # So we return the singular form for both cases
        return forms[0] if len(forms) > 0 else forms

    def _money_verbose(self, number, currency):
        """Convert money amount to verbose format."""
        return self.to_cardinal(number)

    def _cents_verbose(self, number, currency):
        """Convert cents amount to verbose format."""
        return self.to_cardinal(number)

    def to_currency(self, val, currency='TZS', cents=True, separator=' na',
                    adjective=False):
        """
        Convert number to currency format in Swahili.
        """
        # Import the parse function from the base currency module
        # Check if value has fractional cents
        from decimal import Decimal

        from .currency import parse_currency_parts
        decimal_val = Decimal(str(val))
        has_fractional_cents = (decimal_val * 100) % 1 != 0

        # For Swahili, treat integers as whole currency units, not cents
        left, right, is_negative = parse_currency_parts(val, is_int_with_cents=False,
                                                        keep_precision=has_fractional_cents)

        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]
        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"' %
                (currency, self.__class__.__name__))

        minus_str = "%s " % self.negword.strip() if is_negative else ""
        money_str = self.to_cardinal(left)

        # Check if input is explicitly a decimal number or has non-zero cents
        has_decimal = isinstance(val, float) or str(val).find('.') != -1

        # Only include cents if there are actual cents or explicitly decimal
        if has_decimal or right > 0:
            # Handle fractional cents
            from decimal import Decimal
            if isinstance(right, Decimal):
                # Convert fractional cents (e.g., 65.3 cents)
                cents_str = self.to_cardinal_float(float(right)) if cents else str(float(right))
            else:
                cents_str = self.to_cardinal(right) if cents else "%02d" % right
            return u'%s%s %s%s %s %s' % (
                minus_str,
                money_str,
                self.pluralize(left, cr1),
                separator,
                cents_str,
                self.pluralize(right, cr2)
            )
        else:
            return u'%s%s %s' % (
                minus_str,
                money_str,
                self.pluralize(left, cr1)
            )
