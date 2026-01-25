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
from .utils import get_digits, splitbyx

ZERO = ("nulle",)

ONES = {
    1: ("viens",),
    2: ("divi",),
    3: ("trīs",),
    4: ("četri",),
    5: ("pieci",),
    6: ("seši",),
    7: ("septiņi",),
    8: ("astoņi",),
    9: ("deviņi",),
}

TENS = {
    0: ("desmit",),
    1: ("vienpadsmit",),
    2: ("divpadsmit",),
    3: ("trīspadsmit",),
    4: ("četrpadsmit",),
    5: ("piecpadsmit",),
    6: ("sešpadsmit",),
    7: ("septiņpadsmit",),
    8: ("astoņpadsmit",),
    9: ("deviņpadsmit",),
}

TWENTIES = {
    2: ("divdesmit",),
    3: ("trīsdesmit",),
    4: ("četrdesmit",),
    5: ("piecdesmit",),
    6: ("sešdesmit",),
    7: ("septiņdesmit",),
    8: ("astoņdesmit",),
    9: ("deviņdesmit",),
}

HUNDRED = ("simts", "simti", "simtu")

THOUSANDS = {
    1: ("tūkstotis", "tūkstoši", "tūkstošu"),
    2: ("miljons", "miljoni", "miljonu"),
    3: ("miljards", "miljardi", "miljardu"),
    4: ("triljons", "triljoni", "triljonu"),
    5: ("kvadriljons", "kvadriljoni", "kvadriljonu"),
    6: ("kvintiljons", "kvintiljoni", "kvintiljonu"),
    7: ("sikstiljons", "sikstiljoni", "sikstiljonu"),
    8: ("septiljons", "septiljoni", "septiljonu"),
    9: ("oktiljons", "oktiljoni", "oktiljonu"),
    10: ("nontiljons", "nontiljoni", "nontiljonu"),
}

GENERIC_DOLLARS = ("dolārs", "dolāri", "dolāru")
GENERIC_CENTS = ("cents", "centi", "centu")

GENERIC_KRONA = ("krona", "kronas", "kronu")
GENERIC_ERA = ("ēre", "ēras", "ēru")


class Num2Word_LV(Num2Word_Base):
    """
    Sadly we have a legal form (used in legal and finance documents):
    http://www.eiro.lv/files/upload/files/Eiro_rakstiba-1.pdf
    https://likumi.lv/doc.php?id=254741
    http://eur-lex.europa.eu/legal-content/LV/TXT/HTML/?uri=CELEX:31998R0974&from=LV

    Source: http://publications.europa.eu/code/lv/lv-5000500.htm
    """

    CURRENCY_FORMS = {
        "AUD": (GENERIC_DOLLARS, GENERIC_CENTS),
        "CAD": (GENERIC_DOLLARS, GENERIC_CENTS),
        # repalced by EUR
        "EEK": (GENERIC_KRONA, GENERIC_CENTS),
        "EUR": (("eiro", "eiro", "eiro"), GENERIC_CENTS),
        "EUR_LEGAL": (("euro", "euro", "euro"), GENERIC_CENTS),
        "GBP": (
            ("sterliņu mārciņa", "sterliņu mārciņas", "sterliņu mārciņu"),
            ("penss", "pensi", "pensu"),
        ),
        # replaced by EUR
        "LTL": (("lits", "liti", "litu"), GENERIC_CENTS),
        # replaced by EUR
        "LVL": (("lats", "lati", "latu"), ("santīms", "santīmi", "santīmu")),
        "USD": (GENERIC_DOLLARS, GENERIC_CENTS),
        "RUB": (("rublis", "rubļi", "rubļu"), ("kapeika", "kapeikas", "kapeiku")),
        "SEK": (GENERIC_KRONA, GENERIC_ERA),
        "NOK": (GENERIC_KRONA, GENERIC_ERA),
        "PLN": (("zlots", "zloti", "zlotu"), ("grasis", "graši", "grašu")),
    }

    CURRENCY_ADJECTIVES = {
        "AUD": "Austrālijas",
        "CAD": "Kanādas",
        "EEK": "Igaunijas",
        "USD": "ASV",
        "RUB": "Kreivijas",
        "SEK": "Zviedrijas",
        "NOK": "Norvēģijas",
    }

    def setup(self):
        self.negword = "mīnus"
        self.pointword = "komats"

    def to_cardinal(self, number):
        n = str(number).replace(",", ".")
        base_str, n = self.parse_minus(n)
        if "." in n:
            left, right = n.split(".")
            leading_zero_count = len(right) - len(right.lstrip("0"))
            decimal_part = (ZERO[0] + " ") * leading_zero_count + self._int2word(
                int(right)
            )
            return "%s%s %s %s" % (
                base_str,
                self._int2word(int(left)),
                self.pointword,
                decimal_part,
            )
        else:
            return "%s%s" % (base_str, self._int2word(int(n)))

    def pluralize(self, n, forms):
        form = 0 if (n % 10 == 1 and n % 100 != 11) else 1 if n != 0 else 2
        return forms[form]

    def to_currency(
        self, val, currency="EUR", cents=True, separator=",", adjective=False
    ):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_LV, self).to_currency(
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

            return ("%s %s %s" % (minus_str, money_str, currency_str)).strip()

        # For floats, use the parent class implementation
        return super(Num2Word_LV, self).to_currency(
            val,
            currency=currency,
            cents=cents,
            separator=separator,
            adjective=adjective,
        )

    def to_ordinal(self, number):
        """Convert to Latvian ordinal numbers."""
        try:
            num = int(number)
        except (ValueError, TypeError):
            return str(number)

        # Latvian ordinals
        ordinals = {
            1: "pirmais",
            2: "otrais",
            3: "trešais",
            4: "ceturtais",
            5: "piektais",
            6: "sestais",
            7: "septītais",
            8: "astotais",
            9: "devītais",
            10: "desmitais",
            11: "vienpadsmitais",
            12: "divpadsmitais",
            13: "trīspadsmitais",
            14: "četrpadsmitais",
            15: "piecpadsmitais",
            16: "sešpadsmitais",
            17: "septiņpadsmitais",
            18: "astoņpadsmitais",
            19: "deviņpadsmitais",
            20: "divdesmitais",
            30: "trīsdesmitais",
            40: "četrdesmitais",
            50: "piecdesmitais",
            60: "sešdesmitais",
            70: "septiņdesmitais",
            80: "astoņdesmitais",
            90: "deviņdesmitais",
            100: "simtais",
            1000: "tūkstošais",
        }

        if num in ordinals:
            return ordinals[num]

        # For other numbers, add 'ais' suffix to the cardinal
        # This is a simplified implementation
        cardinal = self.to_cardinal(num)
        # Remove trailing 's' if present and add 'ais'
        if cardinal.endswith("s"):
            return cardinal[:-1] + "ais"
        return cardinal + "ais"

    def _int2word(self, n):
        if n == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                if n3 == 1 and n2 == 0 and n1 > 0:
                    words.append(HUNDRED[2])
                elif n3 > 1:
                    words.append(ONES[n3][0])
                    words.append(HUNDRED[1])
                else:
                    words.append(HUNDRED[0])

            if n2 > 1:
                words.append(TWENTIES[n2][0])

            if n2 == 1:
                words.append(TENS[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                words.append(ONES[n1][0])

            if i > 0:
                words.append(self.pluralize(x, THOUSANDS[i]))

        return " ".join(words)
