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


class Num2Word_DA(lang_EUR.Num2Word_EUR):
    GIGA_SUFFIX = "illiarder"
    MEGA_SUFFIX = "illioner"

    CURRENCY_FORMS = {
        'DKK': (('krone', 'kroner'), ('øre', 'øre')),
        'EUR': (('euro', 'euro'), ('cent', 'cent')),
        'USD': (('dollar', 'dollars'), ('cent', 'cent')),
        'GBP': (('pund', 'pund'), ('penny', 'pence')),
        'SEK': (('krone', 'kroner'), ('øre', 'øre')),
        'NOK': (('krone', 'kroner'), ('øre', 'øre')),
    }

    def setup(self):
        super(Num2Word_DA, self).setup()

        self.negword = "minus "
        self.pointword = "komma"
        self.exclude_title = ["og", "komma", "minus"]

        self.mid_numwords = [(1000, "tusind"), (100, "hundrede"),
                             (90, "halvfems"), (80, "firs"),
                             (70, "halvfjerds"), (60, "treds"),
                             (50, "halvtreds"), (40, "fyrre"), (30, "tredive")]
        self.low_numwords = ["tyve", "nitten", "atten", "sytten",
                             "seksten", "femten", "fjorten", "tretten",
                             "tolv", "elleve", "ti", "ni", "otte",
                             "syv", "seks", "fem", "fire", "tre", "to",
                             "et", "nul"]
        self.ords = {"nul": "nul",
                     "et": "f\xf8rste",
                     "to": "anden",
                     "tre": "tredje",
                     "fire": "fjerde",
                     "fem": "femte",
                     "seks": "sjette",
                     "syv": "syvende",
                     "otte": "ottende",
                     "ni": "niende",
                     "ti": "tiende",
                     "elleve": "ellevte",
                     "tolv": "tolvte",
                     "tretten": "trett",
                     "fjorten": "fjort",
                     "femten": "femt",
                     "seksten": "sekst",
                     "sytten": "sytt",
                     "atten": "att",
                     "nitten": "nitt",
                     "tyve": "tyv"}
        self.ordflag = False

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next
        if next[1] == 100 or next[1] == 1000:
            lst = list(next)
            # Special handling: don't concat "et" directly for 10000
            if cnum == 10 and nnum == 1000:
                # 10 * 1000 = "ti tusind" with space
                return ("ti tusind", 10000)
            elif cnum == 100 and nnum == 1000:
                # 100 * 1000 = "ethundrede tusind" with space
                return ("ethundrede tusind", 100000)
            lst[0] = 'et' + lst[0]
            next = tuple(lst)

        if cnum == 1:
            if nnum < 10 ** 6 or self.ordflag:
                return next
            ctext = "en"
        if nnum > cnum:
            if nnum >= 10 ** 6:
                ctext += " "
            val = cnum * nnum
        else:
            if cnum >= 100 and cnum < 1000:
                ctext += " og "
            elif cnum >= 1000 and cnum <= 100000:
                ctext += "e og "
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "en"
                ntext, ctext = ctext, ntext + "og"
            elif cnum >= 10 ** 6:
                ctext += " "
            val = cnum + nnum
        word = ctext + ntext
        return (word, val)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        self.ordflag = True
        outword = self.to_cardinal(value)
        self.ordflag = False
        for key in self.ords:
            if outword.endswith(key):
                outword = outword[:len(outword) - len(key)] + self.ords[key]
                break
        if value % 100 >= 30 and value % 100 <= 39 or value % 100 == 0:
            outword += "te"
        elif value % 100 > 12 or value % 100 == 0:
            outword += "ende"
        return outword

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        vaerdte = (0, 1, 5, 6, 11, 12)
        if value % 100 >= 30 and value % 100 <= 39 or value % 100 in vaerdte:
            return str(value) + "te"
        elif value % 100 == 2:
            return str(value) + "en"
        return str(value) + "ende"

    def to_currency(self, val, currency='DKK', cents=True, separator=',',
                    adjective=False, longval=True):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_DA, self).to_currency(
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
        return super(Num2Word_DA, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)

    def to_year(self, val, longval=True):
        if val == 1:
            return 'en'
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="hundrede", longval=longval)
