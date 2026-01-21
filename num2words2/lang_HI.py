# -*- encoding: utf-8 -*-
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

import string

from num2words2.base import Num2Word_Base


class Num2Word_HI(Num2Word_Base):
    """
    Hindi (HI) Num2Word class
    """

    CURRENCY_FORMS = {
        'INR': (('रुपया', 'रुपये'), ('पैसा', 'पैसे')),
        'USD': (('डॉलर', 'डॉलर'), ('सेंट', 'सेंट')),
        'EUR': (('यूरो', 'यूरो'), ('सेंट', 'सेंट')),
    }

    _irregular_ordinals = {
        0: "शून्य",
        1: "पहला",
        2: "दूसरा",
        3: "तीसरा",
        4: "चौथा",
        6: "छठा",
    }
    _irregular_ordinals_nums = {
        0: "०",
        1: "१ला",
        2: "२रा",
        3: "३रा",
        4: "४था",
        6: "६ठा",
    }
    _hindi_digits = "०१२३४५६७८९"  # 0-9
    _digits_to_hindi_digits = dict(zip(string.digits, _hindi_digits))
    _regular_ordinal_suffix = "वाँ"

    def setup(self):
        # Note: alternative forms are informal
        self.low_numwords = [
            "निन्यानवे",
            "अट्ठानवे",
            "सत्तानवे",  # alternative "सतानवे"
            "छियानवे",
            "पचानवे",
            "चौरानवे",
            "तिरानवे",
            "बानवे",
            "इक्यानवे",
            "नब्बे",
            "नवासी",
            "अट्ठासी",
            "सतासी",
            "छियासी",
            "पचासी",
            "चौरासी",
            "तिरासी",
            "बयासी",
            "इक्यासी",
            "अस्सी",
            "उनासी",  # alternative "उन्नासी"
            "अठहत्तर",  # alternative "अठहतर"
            "सतहत्तर",  # alternative "सतहतर"
            "छिहत्तर",  # alternative "छिहतर"
            "पचहत्तर",  # alternative "पचहतर"
            "चौहत्तर",  # alternative "चौहतर"
            "तिहत्तर",  # alternative "तिहतर"
            "बहत्तर",  # alternative "बहतर"
            "इकहत्तर",  # alternative "इकहतर"
            "सत्तर",
            "उनहत्तर",  # alternative "उनहतर"
            "अड़सठ",  # alternative "अड़सठ"
            "सड़सठ",  # alternative "सड़सठ"
            "छियासठ",
            "पैंसठ",
            "चौंसठ",
            "तिरसठ",
            "बासठ",
            "इकसठ",
            "साठ",
            "उनसठ",
            "अट्ठावन",  # alternative "अठावन"
            "सत्तावन",  # alternative "सतावन"
            "छप्पन",
            "पचपन",
            "चौवन",
            "तिरेपन",  # alternative "तिरपन"
            "बावन",
            "इक्यावन",
            "पचास",
            "उनचास",
            "अड़तालीस",  # alternative "अड़तालीस"
            "सैंतालीस",
            "छियालीस",  # alternative "छयालिस"
            "पैंतालीस",
            "चौवालीस",  # alternative "चवालीस"
            "तैंतालीस",  # alternative "तैतालीस"
            "बयालीस",
            "इकतालीस",
            "चालीस",
            "उनतालीस",
            "अड़तीस",  # alternative "अड़तीस"
            "सैंतीस",
            "छत्तीस",  # alternative "छतीस"
            "पैंतीस",
            "चौंतीस",
            "तैंतीस",
            "बत्तीस",  # alternative "बतीस"
            "इकत्तीस",  # alternative "इकतीस"
            "तीस",
            "उनतीस",
            "अट्ठाईस",  # alternative "अट्ठाइस"
            "सत्ताईस",  # alternative "सताइस"
            "छब्बीस",
            "पच्चीस",
            "चौबीस",
            "तेईस",  # alternative "तेइस"
            "बाईस",
            "इक्कीस",  # alternative "इकीस"
            "बीस",
            "उन्नीस",
            "अट्ठारह",  # alternative "अठारह"
            "सत्रह",
            "सोलह",
            "पंद्रह",
            "चौदह",
            "तेरह",
            "बारह",
            "ग्यारह",
            "दस",
            "नौ",
            "आठ",
            "सात",
            "छः",  # alternative "छह"
            "पाँच",  # alternative "पांच"
            "चार",
            "तीन",
            "दो",
            "एक",
            "शून्य",
        ]

        self.mid_numwords = [(100, "सौ")]
        self.high_numwords = [
            (11, "ख़रब"),
            (9, "अरब"),
            (7, "करोड़"),  # alternative "करोड़"
            (5, "लाख"),
            (3, "हज़ार"),  # alternative "हज़ार"
        ]
        self.pointword = "दशमलव"
        self.negword = "माइनस "

    def set_high_numwords(self, high):
        for n, word in self.high_numwords:
            self.cards[10**n] = word

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        # Remove "एक" prefix for certain major units (but keep for हज़ार)
        if lnum == 1 and rnum in [100, 100000, 10000000]:  # सौ, लाख, करोड़ (but not हज़ार)
            return rtext, rnum
        elif lnum == 1 and rnum < 100:
            return rtext, rnum
        elif lnum >= 100 > rnum:
            return "%s %s" % (ltext, rtext), lnum + rnum
        elif rnum > lnum:
            return "%s %s" % (ltext, rtext), lnum * rnum
        return "%s %s" % (ltext, rtext), lnum + rnum

    def pluralize(self, count, forms):
        """Return the proper plural form for Hindi"""
        if count == 1:
            return forms[0]
        return forms[1] if len(forms) > 1 else forms[0]

    def to_currency(self, val, currency='INR', cents=True, separator=',',
                    adjective=False):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_HI, self).to_currency(
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
        return super(Num2Word_HI, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)

    def to_ordinal(self, value):
        if value in self._irregular_ordinals:
            return self._irregular_ordinals[value]

        # regular Hindi ordinals are derived from cardinals
        # by modifying the last member of the expression.
        cardinal = self.to_cardinal(value)
        return cardinal + self._regular_ordinal_suffix

    def _convert_to_hindi_numerals(self, value):
        return "".join(map(self._digits_to_hindi_digits.__getitem__,
                           str(value)))

    def to_ordinal_num(self, value):
        if value in self._irregular_ordinals_nums:
            return self._irregular_ordinals_nums[value]

        return self._convert_to_hindi_numerals(value) \
            + self._regular_ordinal_suffix
