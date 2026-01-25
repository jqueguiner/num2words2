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

from .lang_EUR import Num2Word_EUR


class Num2Word_DE(Num2Word_EUR):
    CURRENCY_FORMS = {
        "EUR": (("Euro", "Euro"), ("Cent", "Cent")),
        "GBP": (("Pfund", "Pfund"), ("Penny", "Pence")),
        "USD": (("Dollar", "Dollar"), ("Cent", "Cent")),
        "CNY": (("Yuan", "Yuan"), ("Jiao", "Fen")),
        "DEM": (("Mark", "Mark"), ("Pfennig", "Pfennig")),
        "CHF": (("Schweizer Franken", "Schweizer Franken"), ("Rappen", "Rappen")),
        "JPY": (("Yen", "Yen"), ("Sen", "Sen")),
    }

    GIGA_SUFFIX = "illiarde"
    MEGA_SUFFIX = "illion"

    def setup(self):
        self.negword = "minus "
        self.pointword = "Komma"
        # "Cannot treat float %s as ordinal."
        self.errmsg_floatord = (
            "Die Gleitkommazahl %s kann nicht in eine Ordnungszahl "
            + "konvertiert werden."
        )
        # "type(((type(%s)) ) not in [long, int, float]"
        self.errmsg_nonnum = (
            "Nur Zahlen (type(%s)) können in Wörter konvertiert werden."
        )
        # "Cannot treat negative num %s as ordinal."
        self.errmsg_negord = (
            "Die negative Zahl %s kann nicht in eine Ordnungszahl "
            + "konvertiert werden."
        )
        # "abs(%s) must be less than %s."
        self.errmsg_toobig = "Die Zahl %s muss kleiner als %s sein."
        self.exclude_title = []

        lows = ["Non", "Okt", "Sept", "Sext", "Quint", "Quadr", "Tr", "B", "M"]
        units = [
            "",
            "un",
            "duo",
            "tre",
            "quattuor",
            "quin",
            "sex",
            "sept",
            "okto",
            "novem",
        ]
        tens = [
            "dez",
            "vigint",
            "trigint",
            "quadragint",
            "quinquagint",
            "sexagint",
            "septuagint",
            "oktogint",
            "nonagint",
        ]
        self.high_numwords = ["zent"] + self.gen_high_numwords(units, tens, lows)
        self.mid_numwords = [
            (1000, "tausend"),
            (100, "hundert"),
            (90, "neunzig"),
            (80, "achtzig"),
            (70, "siebzig"),
            (60, "sechzig"),
            (50, "f\xfcnfzig"),
            (40, "vierzig"),
            (30, "drei\xdfig"),
        ]
        self.low_numwords = [
            "zwanzig",
            "neunzehn",
            "achtzehn",
            "siebzehn",
            "sechzehn",
            "f\xfcnfzehn",
            "vierzehn",
            "dreizehn",
            "zw\xf6lf",
            "elf",
            "zehn",
            "neun",
            "acht",
            "sieben",
            "sechs",
            "f\xfcnf",
            "vier",
            "drei",
            "zwei",
            "eins",
            "null",
        ]
        self.ords = {
            "eins": "ers",
            "drei": "drit",
            "acht": "ach",
            "sieben": "sieb",
            "ig": "igs",
            "ert": "erts",
            "end": "ends",
            "ion": "ions",
            "nen": "ns",
            "rde": "rds",
            "rden": "rds",
        }

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum == 100 or nnum == 1000:
                return ("ein" + ntext, nnum)
            elif nnum < 10**6:
                return next
            ctext = "eine"

        if nnum > cnum:
            if nnum >= 10**6:
                if cnum > 1:
                    if ntext.endswith("e"):
                        ntext += "n"
                    else:
                        ntext += "en"
                ctext += " "
            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "ein"
                ntext, ctext = ctext, ntext + "und"
            elif cnum >= 10**6:
                ctext += " "
            val = cnum + nnum

        word = ctext + ntext
        return (word, val)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outword = self.to_cardinal(value).lower()
        for key in self.ords:
            if outword.endswith(key):
                outword = outword[: len(outword) - len(key)] + self.ords[key]
                break

        res = outword + "te"

        # Exception: "hundertste" is usually preferred over "einhundertste"
        if res == "eintausendste" or res == "einhundertste":
            res = res.replace("ein", "", 1)
        # ... similarly for "millionste" etc.
        res = re.sub(r"eine ([a-z]+(illion|illiard)ste)$", lambda m: m.group(1), res)
        # Ordinals involving "Million" etc. are written without a space.
        # see https://de.wikipedia.org/wiki/Million#Sprachliches
        res = re.sub(r" ([a-z]+(illion|illiard)ste)$", lambda m: m.group(1), res)

        return res

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "."

    def to_currency(
        self, val, currency="EUR", cents=True, separator=" und", adjective=False
    ):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_DE, self).to_currency(
                    val,
                    currency=currency,
                    cents=cents,
                    separator=separator,
                    adjective=adjective,
                )

            minus_str = self.negword if val < 0 else ""
            abs_val = abs(val)
            money_str = self.to_cardinal(abs_val)

            # Proper pluralization for currency
            if abs_val == 1:
                currency_str = cr1[0] if isinstance(cr1, tuple) else cr1
            else:
                currency_str = (
                    cr1[1]
                    if isinstance(cr1, tuple) and len(cr1) > 1
                    else (cr1[0] if isinstance(cr1, tuple) else cr1)
                )

            return ("%s%s %s" % (minus_str, money_str, currency_str)).strip()

        # For floats, use the parent class implementation
        return super(Num2Word_DE, self).to_currency(
            val,
            currency=currency,
            cents=cents,
            separator=separator,
            adjective=adjective,
        )

    def to_year(self, val, longval=True):
        val = int(val)  # Ensure integer
        if val < 1000 or val > 2999:
            # For years outside common range, use cardinal
            return self.to_cardinal(val)

        # For years 1000-2999, use special formatting
        if val < 2000:
            # 1000-1999: use "hundert" format (e.g. "neunzehnhundert")
            century = val // 100
            remainder = val % 100
            if remainder == 0:
                return self.to_cardinal(century) + "hundert"
            else:
                return (
                    self.to_cardinal(century) + "hundert" + self.to_cardinal(remainder)
                )
        else:
            # 2000-2999: use regular cardinal
            return self.to_cardinal(val)
