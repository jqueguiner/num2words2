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

from .lang_EUR import Num2Word_EUR


class Num2Word_AF(Num2Word_EUR):
    CURRENCY_FORMS = {
        "ZAR": (("rand", "rand"), ("sent", "sent")),
        "EUR": (("euro", "euro"), ("sent", "sent")),
        "GBP": (("pond", "pond"), ("penny", "pence")),
        "USD": (("dollar", "dollar"), ("sent", "sent")),
        "CNY": (("yuan", "yuan"), ("jiao", "fen")),
    }

    GIGA_SUFFIX = "iljard"
    MEGA_SUFFIX = "iljoen"

    def setup(self):
        super(Num2Word_AF, self).setup()

        self.negword = "minus "
        self.pointword = "komma"

        # Error messages in Afrikaans
        self.errmsg_floatord = (
            "Kan nie die desimale getal %s as 'n ordinale getal behandel nie."
        )
        self.errmsg_nonnum = "Slegs getalle (tipe(%s)) kan na woorde omgeskakel word."
        self.errmsg_negord = (
            "Kan nie die negatiewe getal %s as 'n ordinale getal behandel nie."
        )
        self.errmsg_toobig = "Die getal %s moet minder as %s wees."
        self.exclude_title = []

        # High number words for very large numbers
        lows = ["non", "okt", "sept", "sext", "kwint", "kwadr", "tr", "b", "m"]
        units = [
            "",
            "un",
            "duo",
            "tre",
            "kwattuor",
            "kwin",
            "seks",
            "sept",
            "okto",
            "novem",
        ]
        tens = [
            "des",
            "vigint",
            "trigint",
            "kwadragint",
            "kwinquagint",
            "seksagint",
            "septuagint",
            "oktogint",
            "nonagint",
        ]

        self.high_numwords = ["send"] + self.gen_high_numwords(units, tens, lows)

        # Mid-range numbers (thousands, hundreds, tens)
        self.mid_numwords = [
            (1000, "duisend"),
            (100, "honderd"),
            (90, "negentig"),
            (80, "tagtig"),
            (70, "sewentig"),
            (60, "sestig"),
            (50, "vyftig"),
            (40, "veertig"),
            (30, "dertig"),
        ]

        # Low numbers (0-20)
        self.low_numwords = [
            "twintig",
            "negentien",
            "agttien",
            "sewentien",
            "sestien",
            "vyftien",
            "veertien",
            "dertien",
            "twaalf",
            "elf",
            "tien",
            "nege",
            "agt",
            "sewe",
            "ses",
            "vyf",
            "vier",
            "drie",
            "twee",
            "een",
            "nul",
        ]

        # Ordinal mappings
        self.ords = {
            "nul": "nulld",
            "een": "eerst",
            "twee": "tweed",
            "drie": "derd",
            "vier": "vierd",
            "vyf": "vyfd",
            "ses": "sesd",
            "sewe": "sewend",
            "agt": "agst",
            "nege": "negend",
            "tien": "tiend",
            "elf": "elfd",
            "twaalf": "twaalfd",
            # Compound endings
            "ig": "igst",
            "erd": "erdst",
            "end": "endst",
            "joen": "joenst",
            "rd": "rdst",
        }

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum == 100 or nnum == 1000:
                return ("een " + ntext, nnum)
            elif nnum < 10**6:
                return next
            ctext = "een"

        if nnum > cnum:
            if nnum >= 10**6:
                ctext += " "
            elif nnum == 100 or nnum == 1000:
                ctext += " "
            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "een"

                # Afrikaans compound formation: vier-en-dertig
                ntext = ntext + "-en-" + ctext
                ctext = ""
            elif cnum >= 10**6:
                ctext += " "
            elif cnum >= 100:
                ctext += " "
            val = cnum + nnum

        word = ctext + ntext
        return word, val

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outword = self.to_cardinal(value)

        # Handle special compound ordinals
        for key in self.ords:
            if outword.endswith(key):
                outword = outword[: len(outword) - len(key)] + self.ords[key]
                break

        return outword + "e"

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        # Afrikaans uses "de" for some ordinal numbers, "ste" for most
        if value in [2, 3, 4, 5, 6, 7, 8]:
            return str(value) + "de"
        else:
            return str(value) + "ste"

    def pluralize(self, n, forms):
        """
        Afrikaans pluralization rules - most currencies don't change form
        :param n: number
        :param forms: tuple of (singular, plural) forms
        :return: appropriate form
        """
        # Most Afrikaans currencies use the same form for singular and plural
        return forms[0]

    def to_currency(
        self, val, currency="ZAR", cents=True, separator=" en", adjective=False
    ):
        return super(Num2Word_AF, self).to_currency(
            val,
            currency=currency,
            cents=cents,
            separator=separator,
            adjective=adjective,
        )

    def to_year(self, val, longval=True):
        # Handle special year cases
        if val >= 2000:
            if val == 2000:
                return self.to_cardinal(val)
            elif val < 2010:
                # 2001-2009: "twee duisend een", etc.
                return self.to_cardinal(2000) + " " + self.to_cardinal(val - 2000)

            else:
                # 2010+: "twintig tien", "twintig elf", etc.
                century = val // 100
                year_part = val % 100
                if year_part == 0:
                    return self.to_cardinal(century) + " honderd"
                else:
                    return self.to_cardinal(century) + " " + self.to_cardinal(year_part)
        else:
            # Pre-2000 years: "negentien nege-en-negentig" not "negentien honderd nege-en-negentig"

            if val < 1000:
                return self.to_cardinal(val)
            elif not (val // 100) % 10:
                return self.to_cardinal(val)
            else:
                # Split as century + year
                century = val // 100
                year_part = val % 100
                if year_part == 0:
                    return self.to_cardinal(century) + " honderd"
                else:
                    return self.to_cardinal(century) + " " + self.to_cardinal(year_part)
