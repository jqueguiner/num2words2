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


class Num2Word_UR(Num2Word_Base):
    """
    Urdu (UR) Num2Word class
    """

    _irregular_ordinals = {
        0: "صفر",
        1: "پہلا",
        2: "دوسرا",
        3: "تیسرا",
        4: "چوتھا",
        6: "چھٹا",
    }
    _irregular_ordinals_nums = {
        0: "۰",
        1: "۱م",
        2: "۲م",
        3: "۳م",
        4: "۴م",
        6: "۶ٹھا",
    }
    _urdu_digits = "۰۱۲۳۴۵۶۷۸۹"  # 0-9 in Persian-Arabic numerals
    _digits_to_urdu_digits = dict(zip(string.digits, _urdu_digits))
    _regular_ordinal_suffix = "واں"

    def setup(self):
        # Numbers from 99 down to 0, following the same pattern as Hindi
        self.low_numwords = [
            "ننانوے",      # 99
            "اٹھانوے",     # 98
            "ستانوے",      # 97
            "چھیانوے",     # 96
            "پچانوے",      # 95
            "چورانوے",     # 94
            "ترانوے",      # 93
            "بانوے",       # 92
            "اکیانوے",     # 91
            "نوے",         # 90
            "نواسی",       # 89
            "اٹھاسی",      # 88
            "ستاسی",       # 87
            "چھیاسی",      # 86
            "پچاسی",       # 85
            "چوراسی",      # 84
            "تراسی",       # 83
            "بیاسی",       # 82
            "اکیاسی",      # 81
            "اسی",         # 80
            "اناسی",       # 79
            "اٹھہتر",      # 78
            "ستہتر",       # 77
            "چھہتر",       # 76
            "پچہتر",       # 75
            "چوہتر",       # 74
            "تہتر",        # 73
            "بہتر",        # 72
            "اکہتر",       # 71
            "ستر",         # 70
            "انہتر",       # 69
            "اڑساٹھ",      # 68
            "سڑساٹھ",      # 67
            "چھیاساٹھ",    # 66
            "پینساٹھ",     # 65
            "چونساٹھ",     # 64
            "ترساٹھ",      # 63
            "باساٹھ",      # 62
            "اکساٹھ",      # 61
            "ساٹھ",        # 60
            "انساٹھ",      # 59
            "اٹھاون",      # 58
            "ستاون",       # 57
            "چھپن",        # 56
            "پچپن",        # 55
            "چون",         # 54
            "ترپن",        # 53
            "باون",        # 52
            "اکاون",       # 51
            "پچاس",        # 50
            "انچاس",       # 49
            "اڑتالیس",     # 48
            "سینتالیس",    # 47
            "چھیالیس",     # 46
            "پینتالیس",    # 45
            "چوالیس",      # 44
            "تینتالیس",    # 43
            "بیالیس",      # 42
            "اکتالیس",     # 41
            "چالیس",       # 40
            "انتالیس",     # 39
            "اڑتیس",       # 38
            "سینتیس",      # 37
            "چھتیس",       # 36
            "پینتیس",      # 35
            "چونتیس",      # 34
            "تینتیس",      # 33
            "بتیس",        # 32
            "اکتیس",       # 31
            "تیس",         # 30
            "انتیس",       # 29
            "اٹھائیس",     # 28
            "ستائیس",      # 27
            "چھبیس",       # 26
            "پچیس",        # 25
            "چوبیس",       # 24
            "تیئیس",       # 23
            "بائیس",       # 22
            "اکیس",        # 21
            "بیس",         # 20
            "انیس",        # 19
            "اٹھارہ",      # 18
            "سترہ",        # 17
            "سولہ",        # 16
            "پندرہ",       # 15
            "چودہ",        # 14
            "تیرہ",        # 13
            "بارہ",        # 12
            "گیارہ",       # 11
            "دس",          # 10
            "نو",          # 9
            "آٹھ",         # 8
            "سات",         # 7
            "چھ",          # 6
            "پانچ",        # 5
            "چار",         # 4
            "تین",         # 3
            "دو",          # 2
            "ایک",         # 1
            "صفر",         # 0
        ]

        self.mid_numwords = [(100, "سو")]
        # Using Indian numbering system: lakh (100,000) and crore (10,000,000)
        self.high_numwords = [
            (11, "کھرب"),       # 100 billion
            (9, "ارب"),         # 1 billion
            (7, "کروڑ"),        # 10 million (crore)
            (5, "لاکھ"),        # 100 thousand (lakh)
            (3, "ہزار"),        # 1000
        ]
        self.pointword = "نقطہ"
        self.negword = "منفی "

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

        # Regular Urdu ordinals are derived from cardinals
        # by modifying the last member of the expression.
        cardinal = self.to_cardinal(value)
        return cardinal + self._regular_ordinal_suffix

    def _convert_to_urdu_numerals(self, value):
        return "".join(map(self._digits_to_urdu_digits.__getitem__,
                           str(value)))

    def to_ordinal_num(self, value):
        if value in self._irregular_ordinals_nums:
            return self._irregular_ordinals_nums[value]

        return self._convert_to_urdu_numerals(value) \
            + self._regular_ordinal_suffix