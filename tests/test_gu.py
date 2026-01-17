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

# number, gujarati number, pronounced form
TEST_CASES_CARDINAL = (
    (0, "૦", "શૂન્ય"),
    (1, "૧", "એક"),
    (2, "૨", "બે"),
    (3, "૩", "ત્રણ"),
    (4, "૪", "ચાર"),
    (5, "૫", "પાંચ"),
    (6, "૬", "છ"),
    (7, "૭", "સાત"),
    (8, "૮", "આઠ"),
    (9, "૯", "નવ"),
    (10, "૧૦", "દસ"),
    (11, "૧૧", "અગિયાર"),
    (12, "૧૨", "બાર"),
    (13, "૧૩", "તેર"),
    (14, "૧૪", "ચૌદ"),
    (15, "૧૫", "પંદર"),
    (16, "૧૬", "સોળ"),
    (17, "૧૭", "સત્તર"),
    (18, "૧૮", "અઢાર"),
    (19, "૧૯", "ઓગણીસ"),
    (20, "૨૦", "વીસ"),
    (21, "૨૧", "એકવીસ"),
    (22, "૨૨", "બાવીસ"),
    (23, "૨૩", "ત્રેવીસ"),
    (24, "૨૪", "ચોવીસ"),
    (25, "૨૫", "પચીસ"),
    (26, "૨૬", "છવીસ"),
    (27, "૨૭", "સત્તાવીસ"),
    (28, "૨૮", "અઠ્ઠાવીસ"),
    (29, "૨૯", "ઓગણત્રીસ"),
    (30, "૩૦", "ત્રીસ"),
    (31, "૩૧", "એકત્રીસ"),
    (32, "૩૨", "બત્રીસ"),
    (33, "૩૩", "તેત્રીસ"),
    (34, "૩૪", "ચોત્રીસ"),
    (35, "૩૫", "પાંત્રીસ"),
    (36, "૩૬", "છત્રીસ"),
    (37, "૩૭", "સાડત્રીસ"),
    (38, "૩૮", "અડત્રીસ"),
    (39, "૩૯", "ઓગણચાળીસ"),
    (40, "૪૦", "ચાળીસ"),
    (41, "૪૧", "એકતાળીસ"),
    (42, "૪૨", "બેતાળીસ"),
    (43, "૪૩", "ત્રેતાળીસ"),
    (44, "૪૪", "ચુંમાળીસ"),
    (45, "૪૫", "પાંતાળીસ"),
    (46, "૪૬", "છેતાળીસ"),
    (47, "૪૭", "સુડતાળીસ"),
    (48, "૪૮", "અડતાળીસ"),
    (49, "૪૯", "ઓગણપચાસ"),
    (50, "૫૦", "પચાસ"),
    (51, "૫૧", "એકાવન"),
    (52, "૫૨", "બાવન"),
    (53, "૫૩", "ત્રેપન"),
    (54, "૫૪", "ચોપન"),
    (55, "૫૫", "પંચાવન"),
    (56, "૫૬", "છપન"),
    (57, "૫૭", "સત્તાવન"),
    (58, "૫૮", "અઠ્ઠાવન"),
    (59, "૫૯", "ઓગણસાઠ"),
    (60, "૬૦", "સાઠ"),
    (61, "૬૧", "એકસઠ"),
    (62, "૬૨", "બાસઠ"),
    (63, "૬૩", "ત્રેસઠ"),
    (64, "૬૪", "ચોસઠ"),
    (65, "૬૫", "પાંસઠ"),
    (66, "૬૬", "છાસઠ"),
    (67, "૬૭", "સડસઠ"),
    (68, "૬૮", "અડસઠ"),
    (69, "૬૯", "ઓગણસિત્તેર"),
    (70, "૭૦", "સિત્તેર"),
    (71, "૭૧", "એકોતેર"),
    (72, "૭૨", "બોતેર"),
    (73, "૭૩", "તોતેર"),
    (74, "૭૪", "ચુંમોતેર"),
    (75, "૭૫", "પંચોતેર"),
    (76, "૭૬", "છોતેર"),
    (77, "૭૭", "સત્તોતેર"),
    (78, "૭૮", "અઠ્ઠોતેર"),
    (79, "૭૯", "ઓગણએંસી"),
    (80, "૮૦", "એંસી"),
    (81, "૮૧", "એક્યાસી"),
    (82, "૮૨", "બ્યાસી"),
    (83, "૮૩", "ત્ર્યાસી"),
    (84, "૮૪", "ચોર્યાસી"),
    (85, "૮૫", "પંચાસી"),
    (86, "૮૬", "છ્યાસી"),
    (87, "૮૭", "સત્યાસી"),
    (88, "૮૮", "અઠ્ઠ્યાસી"),
    (89, "૮૯", "નેવ્યાસી"),
    (90, "૯૦", "નેવું"),
    (91, "૯૧", "એક્યાણું"),
    (92, "૯૨", "બાણું"),
    (93, "૯૩", "ત્રાણું"),
    (94, "૯૪", "ચોરાણું"),
    (95, "૯૫", "પંચાણું"),
    (96, "૯૬", "છ્યાણું"),
    (97, "૯૭", "સત્યાણું"),
    (98, "૯૮", "અઠ્ઠાણું"),
    (99, "૯૯", "નવ્યાણું"),
    (100, "૧૦૦", "એક સો"),
    (101, "૧૦૧", "એક સો એક"),
    (200, "૨૦૦", "બે સો"),
    (300, "૩૦૦", "ત્રણ સો"),
    (400, "૪૦૦", "ચાર સો"),
    (500, "૫૦૦", "પાંચ સો"),
    (600, "૬૦૦", "છ સો"),
    (700, "૭૦૦", "સાત સો"),
    (800, "૮૦૦", "આઠ સો"),
    (900, "૯૦૦", "નવ સો"),
    (1000, "૧૦૦૦", "એક હજાર"),
    (2000, "૨૦૦૦", "બે હજાર"),
    (10000, "૧૦૦૦૦", "દસ હજાર"),
    (100000, "૧૦૦૦૦૦", "એક લાખ"),
    (1000000, "૧૦૦૦૦૦૦", "દસ લાખ"),
    (10000000, "૧૦૦૦૦૦૦૦", "એક કરોડ"),
    (100000000, "૧૦૦૦૦૦૦૦૦", "દસ કરોડ"),
    (1000000000, "૧૦૦૦૦૦૦૦૦૦", "એક અબજ"),
    (10000000000, "૧૦૦૦૦૦૦૦૦૦૦", "દસ અબજ"),
    (100000000000, "૧૦૦૦૦૦૦૦૦૦૦૦", "એક ખર્વ"),
    (1000000000000, "૧૦૦૦૦૦૦૦૦૦૦૦૦", "દસ ખર્વ"),
    (1234, "૧૨૩૪", "એક હજાર બે સો ચોત્રીસ"),
    (12345, "૧૨૩૪૫", "બાર હજાર ત્રણ સો પાંતાળીસ"),
    (123456, "૧૨૩૪૫૬", "એક લાખ ત્રેવીસ હજાર ચાર સો છપન"),
    (1234567, "૧૨૩૪૫૬૭", "બાર લાખ ચોત્રીસ હજાર પાંચ સો સડસઠ"),
    (12345678, "૧૨૩૪૫૬૭૮", "એક કરોડ ત્રેવીસ લાખ પાંતાળીસ હજાર છ સો અઠ્ઠોતેર"),
    (123456789, "૧૨૩૪૫૬૭૮૯", "બાર કરોડ ચોત્રીસ લાખ છપન હજાર સાત સો નેવ્યાસી"),
    (1234567890, "૧૨૩૪૫૬૭૮૯૦", "એક અબજ ત્રેવીસ કરોડ પાંતાળીસ લાખ સડસઠ હજાર આઠ સો નેવું"),
)

# number, gujarati numeric notation, pronounced form
TEST_CASES_ORDINAL = (
    (0, "૦", "શૂન્ય"),
    (1, "૧મો", "પહેલો"),
    (2, "૨જો", "બીજો"),
    (3, "૩જો", "ત્રીજો"),
    (4, "૪થો", "ચોથો"),
    (5, "૫મો", "પાંચમો"),
    (6, "૬ઠો", "છઠ્ઠો"),
    (7, "૭મો", "સાતમો"),
    (8, "૮મો", "આઠમો"),
    (9, "૯મો", "નવમો"),
    (10, "૧૦મો", "દસમો"),
    (11, "૧૧મો", "અગિયારમો"),
    (12, "૧૨મો", "બારમો"),
    (13, "૧૩મો", "તેરમો"),
    (14, "૧૪મો", "ચૌદમો"),
    (15, "૧૫મો", "પંદરમો"),
    (16, "૧૬મો", "સોળમો"),
    (17, "૧૭મો", "સત્તરમો"),
    (18, "૧૮મો", "અઢારમો"),
    (19, "૧૯મો", "ઓગણીસમો"),
    (20, "૨૦મો", "વીસમો"),
    (21, "૨૧મો", "એકવીસમો"),
    (30, "૩૦મો", "ત્રીસમો"),
    (40, "૪૦મો", "ચાળીસમો"),
    (50, "૫૦મો", "પચાસમો"),
    (60, "૬૦મો", "સાઠમો"),
    (70, "૭૦મો", "સિત્તેરમો"),
    (80, "૮૦મો", "એંસીમો"),
    (90, "૯૦મો", "નેવુંમો"),
    (100, "૧૦૦મો", "એક સોમો"),
    (1000, "૧૦૦૦મો", "એક હજારમો"),
    (100000, "૧૦૦૦૦૦મો", "એક લાખમો"),
    (10000000, "૧૦૦૦૦૦૦૦મો", "એક કરોડમો"),
)


class Num2WordsGUTest(TestCase):
    def test_cardinal(self):
        for number, _, words in TEST_CASES_CARDINAL:
            self.assertEqual(
                num2words(number, lang="gu"),
                words,
                msg="failing number %s" % number,
            )

    def test_negative_cardinal(self):
        self.assertEqual(num2words(-42, lang="gu"), "માઇનસ બેતાળીસ")
        self.assertEqual(num2words(-100, lang="gu"), "માઇનસ એક સો")

    def test_float_cardinal(self):
        self.assertEqual(num2words(12.5, lang="gu"), "બાર દશાંશ પાંચ")
        self.assertEqual(num2words(12.51, lang="gu"), "બાર દશાંશ પાંચ એક")
        self.assertEqual(num2words(0.5, lang="gu"), "શૂન્ય દશાંશ પાંચ")

    def test_ordinal(self):
        for number, _, words in TEST_CASES_ORDINAL:
            self.assertEqual(
                num2words(number, lang="gu", ordinal=True),
                words,
                msg="failing number %s" % number,
            )

    def test_ordinal_num(self):
        for number, numeric_notation, _ in TEST_CASES_ORDINAL:
            self.assertEqual(
                num2words(number, lang="gu", to="ordinal_num"),
                numeric_notation,
                msg="failing number %s" % number,
            )

    # Test Gujarati numeric input
    def test_gujarati_numeric_input(self):
        for number, gujarati_number, words in TEST_CASES_CARDINAL:
            self.assertEqual(
                num2words(gujarati_number, lang="gu"),
                words,
                msg="failing number %s" % number,
            )

    def test_negative_decimals(self):
        # Comprehensive test for negative decimals including -0.4
        self.assertEqual(num2words(-0.4, lang="gu"), "માઇનસ શૂન્ય દશાંશ ચાર")
        self.assertEqual(num2words(-0.5, lang="gu"), "માઇનસ શૂન્ય દશાંશ પાંચ")
        self.assertEqual(num2words(-1.4, lang="gu"), "માઇનસ એક દશાંશ ચાર")

    def test_zero_combinations(self):
        self.assertEqual(num2words(0, lang="gu"), "શૂન્ય")
        self.assertEqual(num2words(101, lang="gu"), "એક સો એક")
        self.assertEqual(num2words(1001, lang="gu"), "એક હજાર એક")
        self.assertEqual(num2words(1010, lang="gu"), "એક હજાર દસ")

    def test_large_numbers(self):
        self.assertEqual(num2words(1000000000000, lang="gu"), "દસ ખર્વ")
        self.assertEqual(num2words(999999999999, lang="gu"), "નવ ખર્વ નવ્યાણું અબજ નવ્યાણું કરોડ નવ્યાણું લાખ નવ્યાણું હજાર નવ સો નવ્યાણું")

    def test_hundreds_combinations(self):
        self.assertEqual(num2words(105, lang="gu"), "એક સો પાંચ")
        self.assertEqual(num2words(205, lang="gu"), "બે સો પાંચ")
        self.assertEqual(num2words(999, lang="gu"), "નવ સો નવ્યાણું")

    def test_thousands_combinations(self):
        self.assertEqual(num2words(1005, lang="gu"), "એક હજાર પાંચ")
        self.assertEqual(num2words(2005, lang="gu"), "બે હજાર પાંચ")
        self.assertEqual(num2words(10005, lang="gu"), "દસ હજાર પાંચ")