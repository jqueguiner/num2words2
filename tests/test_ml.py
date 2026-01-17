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

# Test cases for Malayalam cardinal numbers
TEST_CASES_CARDINAL = (
    (0, "പൂജ്യം"),
    (1, "ഒന്ന്"),
    (2, "രണ്ട്"),
    (3, "മൂന്ന്"),
    (4, "നാല്"),
    (5, "അഞ്ച്"),
    (6, "ആറ്"),
    (7, "ഏഴ്"),
    (8, "എട്ട്"),
    (9, "ഒമ്പത്"),
    (10, "പത്ത്"),
    (11, "പതിനൊന്ന്"),
    (12, "പന്ത്രണ്ട്"),
    (13, "പതിമൂന്ന്"),
    (14, "പതിനാല്"),
    (15, "പതിനഞ്ച്"),
    (16, "പതിനാറ്"),
    (17, "പതിനേഴ്"),
    (18, "പതിനെട്ട്"),
    (19, "പത്തൊമ്പത്"),
    (20, "ഇരുപത്"),
    (21, "ഇരുപത്തിയൊന്ന്"),
    (22, "ഇരുപത്തിരണ്ട്"),
    (23, "ഇരുപത്തിയമൂന്ന്"),
    (24, "ഇരുപത്തിനാല്"),
    (25, "ഇരുപത്തിയഞ്ച്"),
    (26, "ഇരുപത്തിയാറ്"),
    (27, "ഇരുപത്തിയേഴ്"),
    (28, "ഇരുപത്തിയെട്ട്"),
    (29, "ഇരുപത്തൊമ്പത്"),
    (30, "മുപ്പത്"),
    (31, "മുപ്പത്തിയൊന്ന്"),
    (32, "മുപ്പത്തിരണ്ട്"),
    (33, "മുപ്പത്തിയമൂന്ന്"),
    (34, "മുപ്പത്തിനാല്"),
    (35, "മുപ്പത്തിയഞ്ച്"),
    (36, "മുപ്പത്തിയാറ്"),
    (37, "മുപ്പത്തിയേഴ്"),
    (38, "മുപ്പത്തിയെട്ട്"),
    (39, "മുപ്പത്തൊമ്പത്"),
    (40, "നാല്പത്"),
    (41, "നാല്പത്തിയൊന്ന്"),
    (42, "നാല്പത്തിരണ്ട്"),
    (43, "നാല്പത്തിയമൂന്ന്"),
    (44, "നാല്പത്തിനാല്"),
    (45, "നാല്പത്തിയഞ്ച്"),
    (46, "നാല്പത്തിയാറ്"),
    (47, "നാല്പത്തിയേഴ്"),
    (48, "നാല്പത്തിയെട്ട്"),
    (49, "നാല്പത്തൊമ്പത്"),
    (50, "അന്പത്"),
    (60, "അറുപത്"),
    (70, "എഴുപത്"),
    (80, "എണ്പത്"),
    (90, "തൊണ്ണൂറ്"),
    (100, "ഒരു നൂറ്"),
    (101, "ഒരു നൂറ്റിയൊന്ന്"),
    (110, "ഒരു നൂറ്റിപത്ത്"),
    (111, "ഒരു നൂറ്റിപതിനൊന്ന്"),
    (120, "ഒരു നൂറ്റിഇരുപത്"),
    (150, "ഒരു നൂറ്റിയന്പത്"),
    (200, "ഇരുനൂറ്"),
    (300, "മുന്നൂറ്"),
    (400, "നാന്നൂറ്"),
    (500, "അഞ്ഞൂറ്"),
    (600, "ആറുനൂറ്"),
    (700, "ഏഴുനൂറ്"),
    (800, "എട്ടുനൂറ്"),
    (900, "ഒമ്പതുനൂറ്"),
    (999, "ഒമ്പതുനൂറ്റിതൊണ്ണൂറ്റൊമ്പത്"),
    (1000, "ഒരായിരം"),
    (1001, "ഒരായിരത്തിയൊന്ന്"),
    (1100, "ഒരായിരത്തിഒരു നൂറ്"),
    (1500, "ഒരായിരത്തിഅഞ്ഞൂറ്"),
    (2000, "രണ്ടായിരം"),
    (5000, "അഞ്ചായിരം"),
    (10000, "പത്തായിരം"),
    (50000, "അന്പതായിരം"),
    (99999, "തൊണ്ണൂറ്റൊമ്പതായിരത്തിഒമ്പതുനൂറ്റിതൊണ്ണൂറ്റൊമ്പത്"),
    (100000, "ഒരുലക്ഷം"),
    (200000, "രണ്ടുലക്ഷം"),
    (500000, "അഞ്ചുലക്ഷം"),
    (1000000, "പത്തുലക്ഷം"),
    (5000000, "അന്പതുലക്ഷം"),
    (10000000, "ഒരുകോടി"),
    (50000000, "അഞ്ചുകോടി"),
    (100000000, "പത്തുകോടി"),
    (1234, "ഒരായിരത്തിഇരുനൂറ്റിമുപ്പത്തിനാല്"),
    (12345, "പന്ത്രണ്ടായിരത്തിമുന്നൂറ്റിനാല്പത്തിയഞ്ച്"),
    (123456, "ഒരുലക്ഷത്തിഇരുപത്തിയമൂന്നായിരത്തിനാന്നൂറ്റിയന്പത്തിയാറ്"),
)

# Test cases for Malayalam ordinal numbers
TEST_CASES_ORDINAL = (
    (1, "ഒന്നാം"),
    (2, "രണ്ടാം"),
    (3, "മൂന്നാം"),
    (4, "നാലാം"),
    (5, "അഞ്ചാം"),
    (6, "ആറാം"),
    (7, "ഏഴാം"),
    (8, "എട്ടാം"),
    (9, "ഒമ്പതാം"),
    (10, "പത്താം"),
    (11, "പതിനൊന്നാം"),
    (12, "പന്ത്രണ്ടാം"),
    (20, "ഇരുപതാം"),
    (21, "ഇരുപത്തിയൊന്നാം"),
    (100, "ഒരു നൂറാം"),
    (1000, "ഒരായിരാം"),
    (100000, "ഒരുലക്ഷാം"),
    (10000000, "ഒരുകോടിയാം"),
)


class Num2WordsMLTest(TestCase):
    def test_cardinal(self):
        for number, words in TEST_CASES_CARDINAL:
            with self.subTest(number=number):
                self.assertEqual(
                    num2words(number, lang="ml"),
                    words,
                    msg="failing number %s" % number,
                )

    def test_ordinal(self):
        for number, words in TEST_CASES_ORDINAL:
            with self.subTest(number=number):
                self.assertEqual(
                    num2words(number, lang="ml", ordinal=True),
                    words,
                    msg="failing ordinal number %s" % number,
                )

    def test_negative_cardinal(self):
        self.assertEqual(num2words(-5, lang="ml"), "മൈനസ് അഞ്ച്")
        self.assertEqual(num2words(-42, lang="ml"), "മൈനസ് നാല്പത്തിരണ്ട്")
        self.assertEqual(num2words(-100, lang="ml"), "മൈനസ് ഒരു നൂറ്")

    def test_float_cardinal(self):
        self.assertEqual(num2words(12.5, lang="ml"), "പന്ത്രണ്ട് പോയിന്റ് അഞ്ച്")
        self.assertEqual(num2words(12.51, lang="ml"), "പന്ത്രണ്ട് പോയിന്റ് അഞ്ച് ഒന്ന്")
        self.assertEqual(num2words(0.5, lang="ml"), "പൂജ്യം പോയിന്റ് അഞ്ച്")
        self.assertEqual(num2words(0.05, lang="ml"), "പൂജ്യം പോയിന്റ് പൂജ്യം അഞ്ച്")

    def test_negative_decimals(self):
        # Test negative decimals including -0.4
        self.assertEqual(num2words(-0.4, lang="ml"), "മൈനസ് പൂജ്യം പോയിന്റ് നാല്")
        self.assertEqual(num2words(-0.5, lang="ml"), "മൈനസ് പൂജ്യം പോയിന്റ് അഞ്ച്")
        self.assertEqual(num2words(-1.4, lang="ml"), "മൈനസ് ഒന്ന് പോയിന്റ് നാല്")
        self.assertEqual(num2words(-12.34, lang="ml"), "മൈനസ് പന്ത്രണ്ട് പോയിന്റ് മൂന്ന് നാല്")

    def test_zero_variants(self):
        self.assertEqual(num2words(0, lang="ml"), "പൂജ്യം")

    def test_large_numbers(self):
        # Test large numbers with crores and lakhs
        self.assertEqual(num2words(12345678, lang="ml"), "ഒരുകോടിയിരുപത്തിയമൂന്നുലക്ഷത്തിനാല്പത്തിയഞ്ചായിരത്തിആറുനൂറ്റിഎഴുപത്തിയെട്ട്")
        self.assertEqual(num2words(987654321, lang="ml"), "തൊണ്ണൂറ്റിഎട്ടുകോടിഎഴുപത്തിയാറുലക്ഷത്തിഅന്പത്തിനാലായിരത്തിമുന്നൂറ്റിഇരുപത്തിയൊന്ന്")

    def test_edge_cases(self):
        # Test specific numbers that might have edge cases
        self.assertEqual(num2words(11, lang="ml"), "പതിനൊന്ന്")
        self.assertEqual(num2words(111, lang="ml"), "ഒരു നൂറ്റിപതിനൊന്ന്")
        self.assertEqual(num2words(1111, lang="ml"), "ഒരായിരത്തിഒരു നൂറ്റിപതിനൊന്ന്")

    def test_hundreds_combinations(self):
        # Test different hundreds combinations
        for i in range(2, 10):
            hundreds = i * 100
            with self.subTest(hundreds=hundreds):
                result = num2words(hundreds, lang="ml")
                self.assertIsNotNone(result)
                self.assertNotEqual(result, "")

    def test_thousands_combinations(self):
        # Test different thousands combinations  
        for i in range(2, 100):
            thousands = i * 1000
            with self.subTest(thousands=thousands):
                result = num2words(thousands, lang="ml")
                self.assertIsNotNone(result)
                self.assertNotEqual(result, "")

    def test_ordinal_edge_cases(self):
        # Test ordinal edge cases
        self.assertEqual(num2words(1, lang="ml", ordinal=True), "ഒന്നാം")
        self.assertEqual(num2words(11, lang="ml", ordinal=True), "പതിനൊന്നാം")
        self.assertEqual(num2words(101, lang="ml", ordinal=True), "ഒരു നൂറ്റിയൊന്നാം")