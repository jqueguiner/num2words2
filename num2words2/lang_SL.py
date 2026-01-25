# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.
# Copyright (c) 2015, Blaz Bregar. All Rights Reserved.

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

from .lang_EUR import Num2Word_EUR


class Num2Word_SL(Num2Word_EUR):
    GIGA_SUFFIX = "ilijard"
    MEGA_SUFFIX = "ilijon"

    CURRENCY_FORMS = {
        "EUR": (
            ("evro", "evra", "evre", "evrov"),
            ("cent", "centa", "cente", "centov"),
            "",
        ),
        "USD": (
            ("dolar", "dolarja", "dolarje", "dolarjev"),
            ("cent", "centa", "cente", "centov"),
            "",
        ),
    }

    def pluralize(self, n, forms):
        if n % 100 == 1:
            return forms[0]
        elif n % 100 == 2:
            return forms[1]
        elif n % 100 in [3, 4]:
            return forms[2]
        else:
            return forms[3]

    def setup(self):
        super(Num2Word_SL, self).setup()

        self.negword = "minus "
        self.pointword = "vejica"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.errmsg_toobig = "Number is too large to convert to words (abs(%s) > %s)."
        self.exclude_title = []

        self.mid_numwords = [
            (1000, "tisoč"),
            (900, "devetsto"),
            (800, "osemsto"),
            (700, "sedemsto"),
            (600, "šeststo"),
            (500, "petsto"),
            (400, "štiristo"),
            (300, "tristo"),
            (200, "dvesto"),
            (100, "sto"),
            (90, "devetdeset"),
            (80, "osemdeset"),
            (70, "sedemdeset"),
            (60, "šestdeset"),
            (50, "petdeset"),
            (40, "štirideset"),
            (30, "trideset"),
        ]
        self.low_numwords = [
            "dvajset",
            "devetnajst",
            "osemnajst",
            "sedemnajst",
            "šestnajst",
            "petnajst",
            "štirinajst",
            "trinajst",
            "dvanajst",
            "enajst",
            "deset",
            "devet",
            "osem",
            "sedem",
            "šest",
            "pet",
            "štiri",
            "tri",
            "dve",
            "ena",
            "nič",
        ]
        self.ords = {
            "ena": "prv",
            "dve": "drug",
            "tri": "tretj",
            "štiri": "četrt",
            "sedem": "sedm",
            "osem": "osm",
            "sto": "stot",
            "tisoč": "tisoč",
            "milijon": "milijont",
        }
        self.ordflag = False

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if ctext.endswith("dve") and self.ordflag and nnum <= 1000000:
            ctext = ctext[: len(ctext) - 1] + "a"

        if ctext == "dve" and not self.ordflag and nnum < 1000000000:
            ctext = "dva"

        if (
            (ctext.endswith("tri") or ctext.endswith("štiri"))
            and nnum == 1000000
            and not self.ordflag
        ):
            if ctext.endswith("štiri"):
                ctext = ctext[:-1]
            ctext = ctext + "je"

        if cnum >= 20 and cnum < 100 and nnum == 2:
            ntext = "dva"

        if ctext.endswith("ena") and nnum >= 1000:
            ctext = ctext[0:-1]

        if cnum == 1:
            if nnum < 10**6 or self.ordflag:
                return next
            ctext = ""

        if nnum > cnum:
            if nnum >= 10**6:
                if self.ordflag:
                    ntext += "t"

                elif cnum == 2:
                    if ntext.endswith("d"):
                        ntext += "i"
                    else:
                        ntext += "a"

                elif 2 < cnum < 5:
                    if ntext.endswith("d"):
                        ntext += "e"
                    elif not ntext.endswith("d"):
                        ntext += "i"

                elif ctext.endswith("en"):
                    if ntext.endswith("d") or ntext.endswith("n"):
                        ntext += ""

                elif ctext.endswith("dve") and ntext.endswith("n"):
                    ctext = ctext[:-1] + "a"
                    ntext += "a"

                elif ctext.endswith("je") and ntext.endswith("n"):
                    ntext += "i"

                else:
                    if ntext.endswith("d"):
                        ntext += "a"
                    elif ntext.endswith("n"):
                        ntext += ""
                    elif ntext.endswith("d"):
                        ntext += "e"
                    else:
                        ntext += "ov"

            if nnum >= 10**2 and self.ordflag is False and ctext:
                ctext += " "

            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                ntext, ctext = ctext, ntext + "in"
            elif cnum >= 10**2 and self.ordflag is False:
                ctext += " "
            val = cnum + nnum

        word = ctext + ntext
        return (word, val)

    def to_cardinal_float(self, value):
        from .compat import to_s

        pre, post = self.float2tuple(float(value))

        post_str = to_s(post)
        post_str = "0" * (self.precision - len(post_str)) + post_str

        out = [self.to_cardinal(pre)]
        if value < 0 and pre == 0:
            out = [self.negword.strip()] + out

        if self.precision:
            out.append(self.title(self.pointword))
            out.append(self.to_cardinal(int(post_str)))

        return " ".join(out)

    def to_ordinal(self, value):
        """Convert to Slovenian ordinal numbers."""
        self.verify_ordinal(value)  # This will raise TypeError for floats

        try:
            num = int(value)
        except (ValueError, TypeError):
            return str(value)

        # Simple ordinals mapping for common numbers
        ordinals = {
            1: "prvi",
            2: "drugi",
            3: "tretji",
            4: "četrti",
            5: "peti",
            6: "šesti",
            7: "sedmi",
            8: "osmi",
            9: "deveti",
            10: "deseti",
            11: "enajsti",
            12: "dvanajsti",
            13: "trinajsti",
            14: "štirinajsti",
            15: "petnajsti",
            16: "šestnajsti",
            17: "sedemnajsti",
            18: "osemnajsti",
            19: "devetnajsti",
            20: "dvajseti",
            30: "trideseti",
            40: "štirideseti",
            50: "petdeseti",
            60: "šestdeseti",
            70: "sedemdeseti",
            80: "osemdeseti",
            90: "devetdeseti",
            100: "stoti",
            1000: "tisoči",
        }

        if num in ordinals:
            return ordinals[num]

        # For complex ordinals, use the flag method
        self.verify_ordinal(value)
        self.ordflag = True
        outword = self.to_cardinal(value)
        self.ordflag = False
        for key in self.ords:
            if outword.endswith(key):
                outword = outword[: len(outword) - len(key)] + self.ords[key]
                break
        return outword + "i"

    # Is this correct??
    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "."

    def to_currency(
        self, val, currency="EUR", cents=True, separator=" in", adjective=False
    ):
        # Track if input was originally an integer
        is_integer_input = isinstance(val, int)

        # Handle parsing currency parts manually to avoid `is_int_with_cents` issue
        if is_integer_input:
            left = abs(val)
            right = 0
            is_negative = val < 0
        else:
            from decimal import Decimal

            from .currency import parse_currency_parts

            # Check if value has fractional cents
            decimal_val = Decimal(str(val))
            has_fractional_cents = (decimal_val * 100) % 1 != 0

            left, right, is_negative = parse_currency_parts(
                val, is_int_with_cents=False, keep_precision=has_fractional_cents
            )

        try:
            cr1_forms, cr2_forms, cur_separator = self.CURRENCY_FORMS[currency]
        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"'
                % (currency, self.__class__.__name__)
            )

        minus_str = "%s " % self.negword.strip() if is_negative else ""
        money_str = self.to_cardinal(left)

        # For integers, never show cents
        # For floats, always show cents (even if zero)
        if not is_integer_input:
            # Always show cents for floats
            # Handle fractional cents
            from decimal import Decimal

            if isinstance(right, Decimal):
                # Convert fractional cents (e.g., 65.3 cents)
                cents_str = self.to_cardinal_float(float(right)) if right > 0 else "nič"
            else:
                cents_str = self.to_cardinal(right) if right > 0 else "nič"
            if cur_separator:  # Only add separator if it's not empty
                return "%s%s %s%s %s %s" % (
                    minus_str,
                    money_str,
                    self.pluralize(left, cr1_forms),
                    cur_separator,
                    cents_str,
                    self.pluralize(right, cr2_forms),
                )
            else:
                return "%s%s %s %s %s" % (  # No separator
                    minus_str,
                    money_str,
                    self.pluralize(left, cr1_forms),
                    cents_str,
                    self.pluralize(right, cr2_forms),
                )
        else:
            # Integer: no cents
            return "%s%s %s" % (minus_str, money_str, self.pluralize(left, cr1_forms))

    def to_year(self, val, longval=True):
        return self.to_cardinal(val)
