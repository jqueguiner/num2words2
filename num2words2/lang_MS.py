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

from decimal import Decimal

from .base import Num2Word_Base
from .currency import parse_currency_parts


class Num2Word_MS(Num2Word_Base):
    CURRENCY_FORMS = {
        "MYR": (("ringgit", "ringgit"), ("sen", "sen")),
        "SGD": (("dolar", "dolar"), ("sen", "sen")),
        "USD": (("dolar", "dolar"), ("sen", "sen")),
        "EUR": (("euro", "euro"), ("sen", "sen")),
        "GBP": (("paun", "paun"), ("peni", "peni")),
        "IDR": (("rupiah", "rupiah"), ("sen", "sen")),
        "BND": (("dolar", "dolar"), ("sen", "sen")),
    }

    def __init__(self):
        super(Num2Word_MS, self).__init__()

        self.ones = [
            "",
            "satu",
            "dua",
            "tiga",
            "empat",
            "lima",
            "enam",
            "tujuh",
            "lapan",
            "sembilan",
        ]

        self.tens = [
            "",
            "sepuluh",
            "dua puluh",
            "tiga puluh",
            "empat puluh",
            "lima puluh",
            "enam puluh",
            "tujuh puluh",
            "lapan puluh",
            "sembilan puluh",
        ]

        self.teens = {
            11: "sebelas",
            12: "dua belas",
            13: "tiga belas",
            14: "empat belas",
            15: "lima belas",
            16: "enam belas",
            17: "tujuh belas",
            18: "lapan belas",
            19: "sembilan belas",
        }

        self.scale = {
            100: "ratus",
            1000: "ribu",
            1000000: "juta",
            1000000000: "bilion",
            1000000000000: "trilion",
        }

        self.ordinals = [
            "",
            "pertama",
            "kedua",
            "ketiga",
            "keempat",
            "kelima",
            "keenam",
            "ketujuh",
            "kelapan",
            "kesembilan",
            "kesepuluh",
        ]

        self.negword = "negatif "
        self.pointword = "titik"

    def _setup(self):
        super(Num2Word_MS, self)._setup()

    def _int_to_word(self, n):
        """
        Converts a number to words in Malay.
        """
        if n == 0:
            return "kosong"

        parts = []

        # Handle trillions
        if n >= 1000000000000:
            trillions = n // 1000000000000
            if trillions == 1:
                parts.append("satu trilion")
            else:
                parts.append(self._int_to_word(trillions) + " trilion")
            n %= 1000000000000

        # Handle billions
        if n >= 1000000000:
            billions = n // 1000000000
            if billions == 1:
                parts.append("satu bilion")
            else:
                parts.append(self._int_to_word(billions) + " bilion")
            n %= 1000000000

        # Handle millions
        if n >= 1000000:
            millions = n // 1000000
            if millions == 1:
                parts.append("satu juta")
            else:
                parts.append(self._int_to_word(millions) + " juta")
            n %= 1000000

        # Handle thousands
        if n >= 1000:
            thousands = n // 1000
            if thousands == 1:
                parts.append("seribu")
            else:
                parts.append(self._int_to_word(thousands) + " ribu")
            n %= 1000

        # Handle hundreds
        if n >= 100:
            hundreds = n // 100
            if hundreds == 1:
                parts.append("seratus")
            else:
                parts.append(self.ones[hundreds] + " ratus")
            n %= 100

        # Handle special case for teens (11-19)
        if 10 < n < 20:
            parts.append(self.teens[n])
        else:
            # Handle tens
            if n >= 10:
                if n == 10:
                    parts.append("sepuluh")
                else:
                    tens_val = n // 10
                    parts.append(self.tens[tens_val])
                n %= 10

            # Handle ones
            if n > 0:
                parts.append(self.ones[n])

        return " ".join(parts)

    def _int_to_cardinal(self, n):
        if n == 0:
            return "kosong"

        if n < 0:
            return self.negword + self._int_to_word(-n)

        return self._int_to_word(n)

    def _int_to_ordinal(self, n):
        """Convert to ordinal number."""
        if n == 0:
            return "kosong"

        # Special cases for first ten ordinals
        if n <= 10:
            return self.ordinals[n]

        # For other numbers, use "ke-" prefix
        return "ke-" + self._int_to_cardinal(n)

    def to_cardinal(self, n):
        try:
            if isinstance(n, str):
                n = int(n)

            return self._int_to_cardinal(n)
        except BaseException:
            return self._int_to_cardinal(int(n))

    def to_ordinal(self, n):
        try:
            if isinstance(n, str):
                n = int(n)

            return self._int_to_ordinal(n)
        except BaseException:
            return self._int_to_ordinal(int(n))

    def to_ordinal_num(self, n):
        try:
            if isinstance(n, str):
                n = int(n)

            # In Malay, ordinal numbers use "ke-" prefix
            return "ke-" + str(n)
        except BaseException:
            return "ke-" + str(n)

    def to_currency(self, n, currency="MYR"):
        try:
            # Check if value has fractional cents
            decimal_val = Decimal(str(n))
            has_fractional_cents = (decimal_val * 100) % 1 != 0

            left, right, is_negative = parse_currency_parts(n)

            if currency not in self.CURRENCY_FORMS:
                raise NotImplementedError(
                    'Currency code "%s" not implemented for "%s"'
                    % (currency, self.__class__.__name__)
                )

            cr_major, cr_minor = self.CURRENCY_FORMS[currency]

            result = []

            if is_negative:
                result.append(self.negword.strip())

            left_words = self._int_to_cardinal(left)
            result.append(left_words)
            result.append(cr_major[0])

            # Handle cents if non-zero
            if right > 0:
                if has_fractional_cents:
                    # For fractional cents, use float representation
                    fractional_cents = right / 100.0
                    right_words = self.to_cardinal(fractional_cents)
                else:
                    right_words = self._int_to_cardinal(right)
                result.append(right_words)
                result.append(cr_minor[0])

            return " ".join(result)
        except NotImplementedError:
            raise
        except BaseException:
            return str(n) + " " + currency

    def to_year(self, n):
        """Convert to year representation."""
        if n < 1000:
            return self._int_to_cardinal(n)
        elif n < 2000:
            # Years like 1999 -> "seribu sembilan ratus sembilan puluh
            # sembilan"
            return self._int_to_cardinal(n)
        else:
            # Years like 2023 -> "dua ribu dua puluh tiga"
            return self._int_to_cardinal(n)
