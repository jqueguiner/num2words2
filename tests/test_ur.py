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

from unittest import TestCase

from num2words import num2words

# number, urdu number, pronounced form
TEST_CASES_CARDINAL = (
    (0, u"۰", u"صفر"),
    (1, u"۱", u"ایک"),
    (2, u"۲", u"دو"),
    (3, u"۳", u"تین"),
    (4, u"۴", u"چار"),
    (5, u"۵", u"پانچ"),
    (6, u"۶", u"چھ"),
    (7, u"۷", u"سات"),
    (8, u"۸", u"آٹھ"),
    (9, u"۹", u"نو"),
    (10, u"۱۰", u"دس"),
    (11, u"۱۱", u"گیارہ"),
    (12, u"۱۲", u"بارہ"),
    (13, u"۱۳", u"تیرہ"),
    (14, u"۱۴", u"چودہ"),
    (15, u"۱۵", u"پندرہ"),
    (16, u"۱۶", u"سولہ"),
    (17, u"۱۷", u"سترہ"),
    (18, u"۱۸", u"اٹھارہ"),
    (19, u"۱۹", u"انیس"),
    (20, u"۲۰", u"بیس"),
    (21, u"۲۱", u"اکیس"),
    (22, u"۲۲", u"بائیس"),
    (23, u"۲۳", u"تیئیس"),
    (24, u"۲۴", u"چوبیس"),
    (25, u"۲۵", u"پچیس"),
    (26, u"۲۶", u"چھبیس"),
    (27, u"۲۷", u"ستائیس"),
    (28, u"۲۸", u"اٹھائیس"),
    (29, u"۲۹", u"انتیس"),
    (30, u"۳۰", u"تیس"),
    (31, u"۳۱", u"اکتیس"),
    (32, u"۳۲", u"بتیس"),
    (33, u"۳۳", u"تینتیس"),
    (34, u"۳۴", u"چونتیس"),
    (35, u"۳۵", u"پینتیس"),
    (36, u"۳۶", u"چھتیس"),
    (37, u"۳۷", u"سینتیس"),
    (38, u"۳۸", u"اڑتیس"),
    (39, u"۳۹", u"انتالیس"),
    (40, u"۴۰", u"چالیس"),
    (41, u"۴۱", u"اکتالیس"),
    (42, u"۴۲", u"بیالیس"),
    (43, u"۴۳", u"تینتالیس"),
    (44, u"۴۴", u"چوالیس"),
    (45, u"۴۵", u"پینتالیس"),
    (46, u"۴۶", u"چھیالیس"),
    (47, u"۴۷", u"سینتالیس"),
    (48, u"۴۸", u"اڑتالیس"),
    (49, u"۴۹", u"انچاس"),
    (50, u"۵۰", u"پچاس"),
    (51, u"۵۱", u"اکاون"),
    (52, u"۵۲", u"باون"),
    (53, u"۵۳", u"ترپن"),
    (54, u"۵۴", u"چون"),
    (55, u"۵۵", u"پچپن"),
    (56, u"۵۶", u"چھپن"),
    (57, u"۵۷", u"ستاون"),
    (58, u"۵۸", u"اٹھاون"),
    (59, u"۵۹", u"انساٹھ"),
    (60, u"۶۰", u"ساٹھ"),
    (61, u"۶۱", u"اکساٹھ"),
    (62, u"۶۲", u"باساٹھ"),
    (63, u"۶۳", u"ترساٹھ"),
    (64, u"۶۴", u"چونساٹھ"),
    (65, u"۶۵", u"پینساٹھ"),
    (66, u"۶۶", u"چھیاساٹھ"),
    (67, u"۶۷", u"سڑساٹھ"),
    (68, u"۶۸", u"اڑساٹھ"),
    (69, u"۶۹", u"انہتر"),
    (70, u"۷۰", u"ستر"),
    (71, u"۷۱", u"اکہتر"),
    (72, u"۷۲", u"بہتر"),
    (73, u"۷۳", u"تہتر"),
    (74, u"۷۴", u"چوہتر"),
    (75, u"۷۵", u"پچہتر"),
    (76, u"۷۶", u"چھہتر"),
    (77, u"۷۷", u"ستہتر"),
    (78, u"۷۸", u"اٹھہتر"),
    (79, u"۷۹", u"اناسی"),
    (80, u"۸۰", u"اسی"),
    (81, u"۸۱", u"اکیاسی"),
    (82, u"۸۲", u"بیاسی"),
    (83, u"۸۳", u"تراسی"),
    (84, u"۸۴", u"چوراسی"),
    (85, u"۸۵", u"پچاسی"),
    (86, u"۸۶", u"چھیاسی"),
    (87, u"۸۷", u"ستاسی"),
    (88, u"۸۸", u"اٹھاسی"),
    (89, u"۸۹", u"نواسی"),
    (90, u"۹۰", u"نوے"),
    (91, u"۹۱", u"اکیانوے"),
    (92, u"۹۲", u"بانوے"),
    (93, u"۹۳", u"ترانوے"),
    (94, u"۹۴", u"چورانوے"),
    (95, u"۹۵", u"پچانوے"),
    (96, u"۹۶", u"چھیانوے"),
    (97, u"۹۷", u"ستانوے"),
    (98, u"۹۸", u"اٹھانوے"),
    (99, u"۹۹", u"ننانوے"),
    (100, u"۱۰۰", u"ایک سو"),
    (101, u"۱۰۱", u"ایک سو ایک"),
    (110, u"۱۱۰", u"ایک سو دس"),
    (125, u"۱۲۵", u"ایک سو پچیس"),
    (150, u"۱۵۰", u"ایک سو پچاس"),
    (200, u"۲۰۰", u"دو سو"),
    (300, u"۳۰۰", u"تین سو"),
    (400, u"۴۰۰", u"چار سو"),
    (500, u"۵۰۰", u"پانچ سو"),
    (600, u"۶۰۰", u"چھ سو"),
    (700, u"۷۰۰", u"سات سو"),
    (800, u"۸۰۰", u"آٹھ سو"),
    (900, u"۹۰۰", u"نو سو"),
    (999, u"۹۹۹", u"نو سو ننانوے"),
    (1000, u"۱۰۰۰", u"ایک ہزار"),
    (1001, u"۱۰۰۱", u"ایک ہزار ایک"),
    (1100, u"۱۱۰۰", u"ایک ہزار ایک سو"),
    (2000, u"۲۰۰۰", u"دو ہزار"),
    (3000, u"۳۰۰۰", u"تین ہزار"),
    (9999, u"۹۹۹۹", u"نو ہزار نو سو ننانوے"),
    (10000, u"۱۰۰۰۰", u"دس ہزار"),
    (50000, u"۵۰۰۰۰", u"پچاس ہزار"),
    (100000, u"۱۰۰۰۰۰", u"ایک لاکھ"),
    (200000, u"۲۰۰۰۰۰", u"دو لاکھ"),
    (500000, u"۵۰۰۰۰۰", u"پانچ لاکھ"),
    (1000000, u"۱۰۰۰۰۰۰", u"دس لاکھ"),
    (2500000, u"۲۵۰۰۰۰۰", u"پچیس لاکھ"),
    (10000000, u"۱۰۰۰۰۰۰۰", u"ایک کروڑ"),
    (50000000, u"۵۰۰۰۰۰۰۰", u"پانچ کروڑ"),
    (100000000, u"۱۰۰۰۰۰۰۰۰", u"دس کروڑ"),
    (1000000000, u"۱۰۰۰۰۰۰۰۰۰", u"ایک ارب"),
    (10000000000, u"۱۰۰۰۰۰۰۰۰۰۰", u"دس ارب"),
    (100000000000, u"۱۰۰۰۰۰۰۰۰۰۰۰", u"ایک کھرب"),
    (1000000000000, u"۱۰۰۰۰۰۰۰۰۰۰۰۰", u"دس کھرب"),
    # Complex numbers
    (1234, u"۱۲۳۴", u"ایک ہزار دو سو چونتیس"),
    (12345, u"۱۲۳۴۵", u"بارہ ہزار تین سو پینتالیس"),
    (123456, u"۱۲۳۴۵۶", u"ایک لاکھ تیئیس ہزار چار سو چھپن"),
    (1234567, u"۱۲۳۴۵۶۷", u"بارہ لاکھ چونتیس ہزار پانچ سو سڑساٹھ"),
    (12345678, u"۱۲۳۴۵۶۷۸", u"ایک کروڑ تیئیس لاکھ پینتالیس ہزار چھ سو اٹھہتر"),
    (567890123, u"۵۶۷۸۹۰۱۲۳", u"چھپن کروڑ اٹھہتر لاکھ نوے ہزار ایک سو تیئیس"),
    (113345, u"۱۱۳۳۴۵", u"ایک لاکھ تیرہ ہزار تین سو پینتالیس"),
)

# number, urdu numeric notation, pronounced form
TEST_CASES_ORDINAL = (
    (0, u"۰", u"صفر"),  # zero is used in cardinal form
    (1, u"۱م", u"پہلا"),
    (2, u"۲م", u"دوسرا"),
    (3, u"۳م", u"تیسرا"),
    (4, u"۴م", u"چوتھا"),
    (5, u"۵واں", u"پانچواں"),
    (6, u"۶ٹھا", u"چھٹا"),
    (7, u"۷واں", u"ساتواں"),
    (8, u"۸واں", u"آٹھواں"),
    (9, u"۹واں", u"نوواں"),
    (10, u"۱۰واں", u"دسواں"),
    (11, u"۱۱واں", u"گیارہواں"),
    (12, u"۱۲واں", u"بارہواں"),
    (13, u"۱۳واں", u"تیرہواں"),
    (14, u"۱۴واں", u"چودہواں"),
    (15, u"۱۵واں", u"پندرہواں"),
    (16, u"۱۶واں", u"سولہواں"),
    (17, u"۱۷واں", u"سترہواں"),
    (18, u"۱۸واں", u"اٹھارہواں"),
    (19, u"۱۹واں", u"انیسواں"),
    (20, u"۲۰واں", u"بیسواں"),
    (21, u"۲۱واں", u"اکیسواں"),
    (22, u"۲۲واں", u"بائیسواں"),
    (23, u"۲۳واں", u"تیئیسواں"),
    (24, u"۲۴واں", u"چوبیسواں"),
    (25, u"۲۵واں", u"پچیسواں"),
    (26, u"۲۶واں", u"چھبیسواں"),
    (27, u"۲۷واں", u"ستائیسواں"),
    (28, u"۲۸واں", u"اٹھائیسواں"),
    (29, u"۲۹واں", u"انتیسواں"),
    (30, u"۳۰واں", u"تیسواں"),
    (31, u"۳۱واں", u"اکتیسواں"),
    (32, u"۳۲واں", u"بتیسواں"),
    (33, u"۳۳واں", u"تینتیسواں"),
    (34, u"۳۴واں", u"چونتیسواں"),
    (35, u"۳۵واں", u"پینتیسواں"),
    (36, u"۳۶واں", u"چھتیسواں"),
    (37, u"۳۷واں", u"سینتیسواں"),
    (38, u"۳۸واں", u"اڑتیسواں"),
    (39, u"۳۹واں", u"انتالیسواں"),
    (40, u"۴۰واں", u"چالیسواں"),
    (50, u"۵۰واں", u"پچاسواں"),
    (60, u"۶۰واں", u"ساٹھواں"),
    (70, u"۷۰واں", u"سترواں"),
    (80, u"۸۰واں", u"اسیواں"),
    (90, u"۹۰واں", u"نوےواں"),
    (100, u"۱۰۰واں", u"ایک سوواں"),
    (1000, u"۱۰۰۰واں", u"ایک ہزارواں"),
    (100000, u"۱۰۰۰۰۰واں", u"ایک لاکھواں"),
    (1000000, u"۱۰۰۰۰۰۰واں", u"دس لاکھواں"),
    (10000000, u"۱۰۰۰۰۰۰۰واں", u"ایک کروڑواں"),
    (100000000, u"۱۰۰۰۰۰۰۰۰واں", u"دس کروڑواں"),
    (1000000000, u"۱۰۰۰۰۰۰۰۰۰واں", u"ایک اربواں"),
    (10000000000, u"۱۰۰۰۰۰۰۰۰۰۰واں", u"دس اربواں"),
    (100000000000, u"۱۰۰۰۰۰۰۰۰۰۰۰واں", u"ایک کھربواں"),
    (1000000000000, u"۱۰۰۰۰۰۰۰۰۰۰۰۰واں", u"دس کھربواں"),
)


class Num2WordsURTest(TestCase):
    def test_cardinal(self):
        for number, _, words in TEST_CASES_CARDINAL:
            self.assertEqual(
                num2words(number, lang="ur"),
                words,
                msg="failing number %s" % number,
            )

    def test_negative_cardinal(self):
        self.assertEqual(num2words(-42, lang="ur"), u"منفی بیالیس")
        self.assertEqual(num2words(-1, lang="ur"), u"منفی ایک")
        self.assertEqual(num2words(-100, lang="ur"), u"منفی ایک سو")

    def test_float_cardinal(self):
        self.assertEqual(num2words(12.5, lang="ur"), u"بارہ نقطہ پانچ")
        self.assertEqual(num2words(12.51, lang="ur"), u"بارہ نقطہ پانچ ایک")
        self.assertEqual(num2words(0.5, lang="ur"), u"صفر نقطہ پانچ")
        self.assertEqual(num2words(123.45, lang="ur"), u"ایک سو تیئیس نقطہ چار پانچ")

    def test_ordinal(self):
        for number, _, words in TEST_CASES_ORDINAL:
            self.assertEqual(
                num2words(number, lang="ur", ordinal=True),
                words,
                msg="failing number %s" % number,
            )

    def test_ordinal_num(self):
        for number, numeric_notation, _ in TEST_CASES_ORDINAL:
            self.assertEqual(
                num2words(number, lang="ur", to="ordinal_num"),
                numeric_notation,
                msg="failing number %s" % number,
            )

    # Test Urdu numeric input (Persian-Arabic numerals)
    def test_urdu_numeric_input(self):
        for number, urdu_number, words in TEST_CASES_CARDINAL:
            self.assertEqual(
                num2words(urdu_number, lang="ur"),
                words,
                msg="failing number %s" % number,
            )

    def test_negative_decimals(self):
        # Comprehensive test for negative decimals including edge cases
        self.assertEqual(num2words(-0.4, lang="ur"), "منفی صفر نقطہ چار")
        self.assertEqual(num2words(-0.5, lang="ur"), "منفی صفر نقطہ پانچ")
        self.assertEqual(num2words(-1.4, lang="ur"), "منفی ایک نقطہ چار")
        self.assertEqual(num2words(-12.34, lang="ur"), "منفی بارہ نقطہ تین چار")

    def test_large_numbers(self):
        # Test very large numbers to ensure proper handling
        self.assertEqual(num2words(9999999999999, lang="ur"), 
                         u"ننانوے کھرب ننانوے ارب ننانوے کروڑ ننانوے لاکھ ننانوے ہزار نو سو ننانوے")
        
    def test_edge_cases(self):
        # Test specific edge cases
        self.assertEqual(num2words(101, lang="ur"), u"ایک سو ایک")
        self.assertEqual(num2words(1001, lang="ur"), u"ایک ہزار ایک")
        self.assertEqual(num2words(100001, lang="ur"), u"ایک لاکھ ایک")
        self.assertEqual(num2words(10000001, lang="ur"), u"ایک کروڑ ایک")

    def test_teen_numbers(self):
        # Test all teen numbers (11-19) for accuracy
        expected_teens = [
            u"گیارہ", u"بارہ", u"تیرہ", u"چودہ", u"پندرہ",
            u"سولہ", u"سترہ", u"اٹھارہ", u"انیس"
        ]
        for i, expected in enumerate(expected_teens, 11):
            self.assertEqual(num2words(i, lang="ur"), expected,
                           msg="failing teen number %s" % i)

    def test_tens_numbers(self):
        # Test all tens numbers (20-90) for accuracy
        expected_tens = [
            u"بیس", u"تیس", u"چالیس", u"پچاس", 
            u"ساٹھ", u"ستر", u"اسی", u"نوے"
        ]
        for i, expected in enumerate(expected_tens, 2):
            self.assertEqual(num2words(i * 10, lang="ur"), expected,
                           msg="failing tens number %s" % (i * 10))

    def test_hundreds_numbers(self):
        # Test hundreds (100-900) for accuracy
        expected_hundreds = [
            u"ایک سو", u"دو سو", u"تین سو", u"چار سو", u"پانچ سو",
            u"چھ سو", u"سات سو", u"آٹھ سو", u"نو سو"
        ]
        for i, expected in enumerate(expected_hundreds, 1):
            self.assertEqual(num2words(i * 100, lang="ur"), expected,
                           msg="failing hundreds number %s" % (i * 100))