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


class Num2Word_AZ(Num2Word_Base):
    DIGITS = {
        0: "sıfır",
        1: "bir",
        2: "iki",
        3: "üç",
        4: "dörd",
        5: "beş",
        6: "altı",
        7: "yeddi",
        8: "səkkiz",
        9: "doqquz",
    }

    DECIMALS = {
        1: "on",
        2: "iyirmi",
        3: "otuz",
        4: "qırx",
        5: "əlli",
        6: "altmış",
        7: "yetmiş",
        8: "səksən",
        9: "doxsan",
    }

    POWERS_OF_TEN = {
        2: "yüz",
        3: "min",
        6: "milyon",
        9: "milyard",
        12: "trilyon",
        15: "katrilyon",
        18: "kentilyon",
        21: "sekstilyon",
        24: "septilyon",
        27: "oktilyon",
        30: "nonilyon",
        33: "desilyon",
        36: "undesilyon",
        39: "dodesilyon",
        42: "tredesilyon",
        45: "katordesilyon",
        48: "kendesilyon",
        51: "seksdesilyon",
        54: "septendesilyon",
        57: "oktodesilyon",
        60: "novemdesilyon",
        63: "vigintilyon",
    }

    VOWELS = "aıoueəiöü"
    VOWEL_TO_CARDINAL_SUFFIX_MAP = {
        **dict.fromkeys(["a", "ı"], "ıncı"),
        **dict.fromkeys(["e", "ə", "i"], "inci"),
        **dict.fromkeys(["o", "u"], "uncu"),
        **dict.fromkeys(["ö", "ü"], "üncü"),
    }

    VOWEL_TO_CARDINAL_NUM_SUFFIX_MAP = {
        **dict.fromkeys(["a", "ı"], "cı"),
        **dict.fromkeys(["e", "ə", "i"], "ci"),
        **dict.fromkeys(["o", "u"], "cu"),
        **dict.fromkeys(["ö", "ü"], "cü"),
    }

    CURRENCY_INTEGRAL = ("manat", "manat")
    CURRENCY_FRACTION = ("qəpik", "qəpik")
    CURRENCY_FORMS = {
        "AZN": (CURRENCY_INTEGRAL, CURRENCY_FRACTION),
        "EUR": (("avro", "avro"), ("sent", "sent")),
        "USD": (("dollar", "dollar"), ("sent", "sent")),
    }

    def setup(self):
        super().setup()

        self.negword = "mənfi"
        self.pointword = "nöqtə"

    def to_cardinal(self, value):
        value_str = str(value)
        parts = value_str.split(".")
        integral_part = parts[0]
        fraction_part = parts[1] if len(parts) > 1 else ""

        if integral_part.startswith("-"):
            integral_part = integral_part[1:]  # ignore minus sign here

        integral_part_in_words = self.int_to_word(integral_part)
        fraction_part_in_words = (
            ""
            if not fraction_part
            else self.int_to_word(fraction_part, leading_zeros=True)
        )

        value_in_words = integral_part_in_words
        if fraction_part:
            value_in_words = " ".join(
                [integral_part_in_words, self.pointword, fraction_part_in_words]
            )

        if value < 0:
            value_in_words = " ".join([self.negword, value_in_words])

        return value_in_words

    def to_ordinal(self, value):
        assert int(value) == value

        cardinal = self.to_cardinal(value)
        last_vowel = self._last_vowel(cardinal)
        assert last_vowel is not None
        suffix = self.VOWEL_TO_CARDINAL_SUFFIX_MAP[last_vowel]

        if cardinal.endswith(tuple(self.VOWELS)):
            cardinal = cardinal[:-1]

        ordinal = "".join([cardinal, suffix])

        return ordinal

    def to_ordinal_num(self, value):
        assert int(value) == value

        cardinal = self.to_cardinal(value)
        last_vowel = self._last_vowel(cardinal)
        assert last_vowel is not None
        suffix = self.VOWEL_TO_CARDINAL_NUM_SUFFIX_MAP[last_vowel]
        ordinal_num = "-".join([str(value), suffix])

        return ordinal_num

    def to_year(self, value):
        assert int(value) == value

        year = self.to_cardinal(abs(value))
        if value < 0:
            year = " ".join(["e.ə.", year])

        return year

    def pluralize(self, n, forms):
        form = 0 if n == 1 else 1
        return forms[form]

    def int_to_word(self, num_str, leading_zeros=False):
        words = []
        reversed_str = list(reversed(num_str))

        for index, digit in enumerate(reversed_str):
            digit_int = int(digit)
            # calculate remainder after dividing index by 3
            # because number is parsed by three digit chunks
            remainder_to_3 = index % 3
            if remainder_to_3 == 0:
                if index > 0:
                    if set(reversed_str[index : index + 3]) != {"0"}:
                        words.insert(0, self.POWERS_OF_TEN[index])
                if digit_int > 0:
                    # we say "min" not "bir min"
                    if not (digit_int == 1 and index == 3):
                        words.insert(0, self.DIGITS[digit_int])
            elif remainder_to_3 == 1:
                if digit_int != 0:
                    words.insert(0, self.DECIMALS[digit_int])
            else:  # remainder is 2
                if digit_int > 0:
                    words.insert(0, self.POWERS_OF_TEN[2])  # "yüz"
                if digit_int > 1:
                    words.insert(0, self.DIGITS[digit_int])

        if num_str == "0":
            words.append(self.DIGITS[0])

        if leading_zeros:
            zeros_count = len(num_str) - len(str(int(num_str)))
            words[:0] = zeros_count * [self.DIGITS[0]]

        return " ".join(words)

    def _last_vowel(self, value):
        for char in value[::-1]:
            if char in self.VOWELS:
                return char
