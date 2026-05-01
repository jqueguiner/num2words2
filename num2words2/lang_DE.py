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
    # Feminine grammatical-gender currencies need the numeral 'eine' (not
    # 'ein'/'eins') when the value ends in 1. Issue #69.
    FEMININE_CURRENCIES = {"DEM", "INR"}

    CURRENCY_FORMS = {
        "EUR": (("Euro", "Euro"), ("Cent", "Cent")),
        "GBP": (("Pfund", "Pfund"), ("Penny", "Pence")),
        "USD": (("Dollar", "Dollar"), ("Cent", "Cent")),
        "CAD": (("Dollar", "Dollar"), ("Cent", "Cent")),
        "AUD": (("Dollar", "Dollar"), ("Cent", "Cent")),
        "NZD": (("Dollar", "Dollar"), ("Cent", "Cent")),
        "HKD": (("Dollar", "Dollar"), ("Cent", "Cent")),
        "CNY": (("Yuan", "Yuan"), ("Jiao", "Fen")),
        "DEM": (("Mark", "Mark"), ("Pfennig", "Pfennig")),
        "CHF": (("Schweizer Franken", "Schweizer Franken"), ("Rappen", "Rappen")),
        "JPY": (("Yen", "Yen"), ("Sen", "Sen")),
        "INR": (("Rupie", "Rupien"), ("Paisa", "Paisa")),
        "RUB": (("Rubel", "Rubel"), ("Kopeke", "Kopeken")),
        "KRW": (("Won", "Won"), ("Jeon", "Jeon")),
        "MXN": (("Peso", "Pesos"), ("Centavo", "Centavos")),
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
        # German ordinals are written without spaces, even in compound
        # forms like 'einemillionerste'. Issue #59 ports
        # savoirfairelinux/num2words#357.
        res = re.sub(r"eine (million|milliard|billion|billiard)", r"ein\1", res)
        res = res.replace(" ", "")

        return res

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "."

    def to_fraction(self, numerator, denominator):
        """German fractions: capitalised noun, invariant plural.

        ``1/3`` → "ein Drittel"; ``2/3`` → "zwei Drittel" (no -s plural).
        ``1/2`` → "ein halb"; ``2/2`` → "zwei halbe" (adjectival).
        Numerator uses the apocopated ``ein`` rather than the cardinal
        ``eins`` since the fraction is a noun phrase. Issue #584.
        """
        if denominator == 0:
            raise ZeroDivisionError("denominator must not be zero")
        if denominator == 1 or numerator == 0:
            return self.to_cardinal(numerator)
        is_negative = (numerator < 0) ^ (denominator < 0)
        abs_n = abs(int(numerator))
        abs_d = abs(int(denominator))

        # Common denominators with their idiomatic noun. Plural is
        # invariant for these — "zwei Drittel" not "zwei Drittels".
        de_frac = {
            3: "Drittel",
            4: "Viertel",
            5: "Fünftel",
            6: "Sechstel",
            7: "Siebtel",
            8: "Achtel",
            9: "Neuntel",
            10: "Zehntel",
            11: "Elftel",
            12: "Zwölftel",
        }
        if abs_d == 2:
            den_word = "halb" if abs_n == 1 else "halbe"
        elif abs_d in de_frac:
            den_word = de_frac[abs_d]
        elif abs_d < 20:
            stem = self.to_cardinal(abs_d)
            den_word = stem + "tel"
            den_word = den_word[0].upper() + den_word[1:]
        else:
            # 20+ → cardinal + 'stel' (zwanzigstel, hundertstel, ...).
            stem = self.to_cardinal(abs_d)
            # Drop the redundant 'ein' prefix on round powers of ten:
            # 100 reads as 'einhundert' standalone but 'Hundertstel' as
            # a fraction noun; same for 'eintausend' → 'Tausendstel'.
            for prefix in ("einhundert", "eintausend", "einemillion", "einemilliarde"):
                if stem.startswith(prefix) and stem == prefix:
                    stem = stem[3:]  # drop 'ein'
                    break
            den_word = stem + "stel"
            den_word = den_word[0].upper() + den_word[1:]

        num_word = "ein" if abs_n == 1 else self.to_cardinal(abs_n)
        sign = "%s " % self.negword.strip() if is_negative else ""
        return sign + num_word + " " + den_word

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

            # German feminine-currency rule: when the currency word is
            # feminine and the number ends in 'mod 100 == 1', the numeral
            # takes the feminine form 'eine' instead of 'ein'/'eins'.
            # Issue #69 ports savoirfairelinux/num2words#462.
            if currency in self.FEMININE_CURRENCIES and abs_val % 100 == 1:
                if money_str.endswith("eins"):
                    money_str = money_str[:-4] + "eine"
                elif money_str.endswith("ein"):
                    money_str = money_str + "e"

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
