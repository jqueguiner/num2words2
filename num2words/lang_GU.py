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

from num2words.base import Num2Word_Base


class Num2Word_GU(Num2Word_Base):
    """
    Gujarati (GU) Num2Word class
    """

    _irregular_ordinals = {
        0: "શૂન્ય",
        1: "પહેલો",
        2: "બીજો",
        3: "ત્રીજો",
        4: "ચોથો",
        6: "છઠ્ઠો",
    }
    _irregular_ordinals_nums = {
        0: "૦",
        1: "૧મો",
        2: "૨જો",
        3: "૩જો",
        4: "૪થો",
        6: "૬ઠો",
    }
    _gujarati_digits = "૦૧૨૩૪૫૬૭૮૯"  # 0-9
    _digits_to_gujarati_digits = dict(zip(string.digits, _gujarati_digits))
    _regular_ordinal_suffix = "મો"

    def setup(self):
        self.low_numwords = [
            "નવ્યાણું",     # 99
            "અઠ્ઠાણું",     # 98
            "સત્યાણું",     # 97
            "છ્યાણું",      # 96
            "પંચાણું",      # 95
            "ચોરાણું",      # 94
            "ત્રાણું",      # 93
            "બાણું",        # 92
            "એક્યાણું",     # 91
            "નેવું",        # 90
            "નેવ્યાસી",     # 89
            "અઠ્ઠ્યાસી",    # 88
            "સત્યાસી",      # 87
            "છ્યાસી",       # 86
            "પંચાસી",       # 85
            "ચોર્યાસી",     # 84
            "ત્ર્યાસી",     # 83
            "બ્યાસી",       # 82
            "એક્યાસી",      # 81
            "એંસી",         # 80
            "ઓગણએંસી",     # 79
            "અઠ્ઠોતેર",     # 78
            "સત્તોતેર",     # 77
            "છોતેર",        # 76
            "પંચોતેર",      # 75
            "ચુંમોતેર",     # 74
            "તોતેર",        # 73
            "બોતેર",        # 72
            "એકોતેર",       # 71
            "સિત્તેર",      # 70
            "ઓગણસિત્તેર",   # 69
            "અડસઠ",        # 68
            "સડસઠ",        # 67
            "છાસઠ",        # 66
            "પાંસઠ",        # 65
            "ચોસઠ",        # 64
            "ત્રેસઠ",       # 63
            "બાસઠ",        # 62
            "એકસઠ",        # 61
            "સાઠ",          # 60
            "ઓગણસાઠ",      # 59
            "અઠ્ઠાવન",     # 58
            "સત્તાવન",     # 57
            "છપન",         # 56
            "પંચાવન",      # 55
            "ચોપન",        # 54
            "ત્રેપન",       # 53
            "બાવન",        # 52
            "એકાવન",       # 51
            "પચાસ",        # 50
            "ઓગણપચાસ",     # 49
            "અડતાળીસ",     # 48
            "સુડતાળીસ",    # 47
            "છેતાળીસ",     # 46
            "પાંતાળીસ",     # 45
            "ચુંમાળીસ",     # 44
            "ત્રેતાળીસ",    # 43
            "બેતાળીસ",     # 42
            "એકતાળીસ",     # 41
            "ચાળીસ",       # 40
            "ઓગણચાળીસ",    # 39
            "અડત્રીસ",      # 38
            "સાડત્રીસ",     # 37
            "છત્રીસ",       # 36
            "પાંત્રીસ",     # 35
            "ચોત્રીસ",      # 34
            "તેત્રીસ",      # 33
            "બત્રીસ",       # 32
            "એકત્રીસ",      # 31
            "ત્રીસ",        # 30
            "ઓગણત્રીસ",     # 29
            "અઠ્ઠાવીસ",    # 28
            "સત્તાવીસ",     # 27
            "છવીસ",        # 26
            "પચીસ",        # 25
            "ચોવીસ",       # 24
            "ત્રેવીસ",      # 23
            "બાવીસ",       # 22
            "એકવીસ",       # 21
            "વીસ",         # 20
            "ઓગણીસ",       # 19
            "અઢાર",        # 18
            "સત્તર",        # 17
            "સોળ",         # 16
            "પંદર",        # 15
            "ચૌદ",         # 14
            "તેર",          # 13
            "બાર",          # 12
            "અગિયાર",      # 11
            "દસ",           # 10
            "નવ",           # 9
            "આઠ",           # 8
            "સાત",          # 7
            "છ",            # 6
            "પાંચ",         # 5
            "ચાર",          # 4
            "ત્રણ",         # 3
            "બે",           # 2
            "એક",           # 1
            "શૂન્ય",        # 0
        ]

        self.mid_numwords = [(100, "સો")]
        self.high_numwords = [
            (11, "ખર્વ"),
            (9, "અબજ"),
            (7, "કરોડ"),
            (5, "લાખ"),
            (3, "હજાર"),
        ]
        self.pointword = "દશાંશ"
        self.negword = "માઇનસ "

    def set_high_numwords(self, high):
        for n, word in self.high_numwords:
            self.cards[10**n] = word

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return rtext, rnum
        elif lnum >= 100 > rnum:
            return "%s %s" % (ltext, rtext), lnum + rnum
        elif rnum > lnum:
            return "%s %s" % (ltext, rtext), lnum * rnum
        return "%s %s" % (ltext, rtext), lnum + rnum

    def to_ordinal(self, value):
        if value in self._irregular_ordinals:
            return self._irregular_ordinals[value]

        # regular Gujarati ordinals are derived from cardinals
        # by modifying the last member of the expression.
        cardinal = self.to_cardinal(value)
        return cardinal + self._regular_ordinal_suffix

    def _convert_to_gujarati_numerals(self, value):
        return "".join(map(self._digits_to_gujarati_digits.__getitem__,
                           str(value)))

    def to_ordinal_num(self, value):
        if value in self._irregular_ordinals_nums:
            return self._irregular_ordinals_nums[value]

        return self._convert_to_gujarati_numerals(value) \
            + self._regular_ordinal_suffix