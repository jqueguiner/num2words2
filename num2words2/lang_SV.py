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

from __future__ import division, print_function, unicode_literals

from . import lang_EUR


class Num2Word_SV(lang_EUR.Num2Word_EUR):
    GIGA_SUFFIX = "iljarder"
    MEGA_SUFFIX = "iljoner"

    def set_high_numwords(self, high):
        cap = 3 + 6 * len(high)

        for word, n in zip(high, range(cap, 3, -6)):
            if self.GIGA_SUFFIX:
                self.cards[10 ** n] = word + self.GIGA_SUFFIX

            if self.MEGA_SUFFIX:
                self.cards[10 ** (n - 3)] = word + self.MEGA_SUFFIX

    def setup(self):
        super(Num2Word_SV, self).setup()

        self.negword = "minus "
        self.pointword = "komma"
        self.exclude_title = ["och", "komma", "minus"]

        self.mid_numwords = [(1000, "tusen"), (100, "hundra"),
                             (90, "nittio"), (80, "åttio"), (70, "sjuttio"),
                             (60, "sextio"), (50, "femtio"), (40, "förtio"),
                             (30, "trettio")]
        self.low_numwords = ["tjugo", "nitton", "arton", "sjutton",
                             "sexton", "femton", "fjorton", "tretton",
                             "tolv", "elva", "tio", "nio", "åtta",
                             "sju", "sex", "fem", "fyra", "tre", "två",
                             "ett", "noll"]
        self.ords = {"noll": "nollte",
                     "ett": "första",
                     "två": "andra",
                     "tre": "tredje",
                     "fyra": "fjärde",
                     "fem": "femte",
                     "sex": "sjätte",
                     "sju": "sjunde",
                     "åtta": "åttonde",
                     "nio": "nionde",
                     "tio": "tionde",
                     "elva": "elfte",
                     "tolv": "tolfte",
                     "tjugo": "tjugonde"}

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif 100 > lnum > rnum:
            return ("%s%s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100 > rnum:
            return ("%s%s" % (ltext, rtext), lnum + rnum)
        elif rnum >= 1000000 and lnum == 1:
            return ("%s %s" % ('en', rtext[:-2]), lnum + rnum)
        elif rnum >= 1000000 and lnum > 1:
            return ("%s %s" % (ltext, rtext), lnum + rnum)
        elif rnum > lnum:
            # Special case: Swedish doesn't use "ett" before "hundra" in compounds
            if lnum == 100 and rnum == 1000:
                return ("hundratusen", 100000)
            return ("%s%s" % (ltext, rtext), lnum * rnum)
        return ("%s %s" % (ltext, rtext), lnum + rnum)

    def to_currency(self, val, currency='EUR', cents=True, separator=',',
                    adjective=False):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_SV, self).to_currency(
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
        return super(Num2Word_SV, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastword = outwords[-1]
        ending_length = 0
        try:
            lastword_ending = self.ords[lastword[-4:]]
            ending_length = 4
        except KeyError:
            try:
                lastword_ending = self.ords[lastword[-3:]]
                ending_length = 3
            except KeyError:
                lastword_ending = "de"
        if lastword_ending == 'de':
            lastword_first_part = self.title(lastword)[:]
        else:
            lastword_first_part = self.title(lastword)[:-ending_length]
        lastword_correct = lastword_first_part + lastword_ending
        outwords[-1] = lastword_correct
        return " ".join(outwords)

    def to_ordinal_num(self, value):
        """Convert to abbreviated ordinal form in Swedish"""
        # Swedish uses :e, :a, :de, :te etc. for ordinals
        if value == 1 or value == 2:
            return str(value) + ':a'
        elif str(value).endswith(('1', '2')) and value not in (11, 12):
            return str(value) + ':a'
        elif str(value).endswith(('3', '4', '5', '6', '7', '8', '9', '0')):
            return str(value) + ':e'
        else:
            return str(value) + ':e'

    def to_year(self, val, longval=True):
        """Convert number to year representation in Swedish"""
        if val < 0:
            # BC years
            return self.to_cardinal(-val) + " f.Kr."
        elif val < 1000:
            # Years before 1000
            return self.to_cardinal(val)
        elif val < 2000:
            # Years 1000-1999: typically "nittonhundra" style
            century = val // 100
            remainder = val % 100
            if remainder == 0:
                return self.to_cardinal(century) + "hundra"
            else:
                return self.to_cardinal(century) + "hundra" + self.to_cardinal(remainder)
        else:
            # Years 2000+: typically "tvåtusen" style
            return self.to_cardinal(val)
