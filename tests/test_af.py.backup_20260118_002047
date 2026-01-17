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

from unittest import TestCase

from num2words2 import num2words
from num2words2.lang_AF import Num2Word_AF

# Test cases for currency conversion to ZAR (South African Rand)
TEST_CASES_TO_CURRENCY_ZAR = (
    (1.00, 'een rand en nul sent'),
    (2.01, 'twee rand en een sent'),
    (8.10, 'agt rand en tien sent'),
    (12.26, 'twaalf rand en ses-en-twintig sent'),
    (21.29, 'een-en-twintig rand en nege-en-twintig sent'),
    (81.25, 'een-en-tagtig rand en vyf-en-twintig sent'),
    (100.00, 'een honderd rand en nul sent'),
)

# Test cases for currency conversion to EUR
TEST_CASES_TO_CURRENCY_EUR = (
    (1.00, 'een euro en nul sent'),
    (2.01, 'twee euro en een sent'),
    (8.10, 'agt euro en tien sent'),
    (12.26, 'twaalf euro en ses-en-twintig sent'),
    (21.29, 'een-en-twintig euro en nege-en-twintig sent'),
    (81.25, 'een-en-tagtig euro en vyf-en-twintig sent'),
    (100.00, 'een honderd euro en nul sent'),
)

# Test cases for currency conversion to USD
TEST_CASES_TO_CURRENCY_USD = (
    (1.00, 'een dollar en nul sent'),
    (2.01, 'twee dollar en een sent'),
    (8.10, 'agt dollar en tien sent'),
    (12.26, 'twaalf dollar en ses-en-twintig sent'),
    (21.29, 'een-en-twintig dollar en nege-en-twintig sent'),
    (81.25, 'een-en-tagtig dollar en vyf-en-twintig sent'),
    (100.00, 'een honderd dollar en nul sent'),
)


class Num2WordsAFTest(TestCase):

    def test_cardinal_basic_numbers(self):
        """Test basic cardinal numbers from 0 to 20"""
        self.assertEqual(num2words(0, lang='af'), "nul")
        self.assertEqual(num2words(1, lang='af'), "een")
        self.assertEqual(num2words(2, lang='af'), "twee")
        self.assertEqual(num2words(3, lang='af'), "drie")
        self.assertEqual(num2words(4, lang='af'), "vier")
        self.assertEqual(num2words(5, lang='af'), "vyf")
        self.assertEqual(num2words(6, lang='af'), "ses")
        self.assertEqual(num2words(7, lang='af'), "sewe")
        self.assertEqual(num2words(8, lang='af'), "agt")
        self.assertEqual(num2words(9, lang='af'), "nege")
        self.assertEqual(num2words(10, lang='af'), "tien")
        self.assertEqual(num2words(11, lang='af'), "elf")
        self.assertEqual(num2words(12, lang='af'), "twaalf")
        self.assertEqual(num2words(13, lang='af'), "dertien")
        self.assertEqual(num2words(14, lang='af'), "veertien")
        self.assertEqual(num2words(15, lang='af'), "vyftien")
        self.assertEqual(num2words(16, lang='af'), "sestien")
        self.assertEqual(num2words(17, lang='af'), "sewentien")
        self.assertEqual(num2words(18, lang='af'), "agttien")
        self.assertEqual(num2words(19, lang='af'), "negentien")
        self.assertEqual(num2words(20, lang='af'), "twintig")

    def test_cardinal_tens(self):
        """Test tens from 20 to 90"""
        self.assertEqual(num2words(20, lang='af'), "twintig")
        self.assertEqual(num2words(30, lang='af'), "dertig")
        self.assertEqual(num2words(40, lang='af'), "veertig")
        self.assertEqual(num2words(50, lang='af'), "vyftig")
        self.assertEqual(num2words(60, lang='af'), "sestig")
        self.assertEqual(num2words(70, lang='af'), "sewentig")
        self.assertEqual(num2words(80, lang='af'), "tagtig")
        self.assertEqual(num2words(90, lang='af'), "negentig")

    def test_cardinal_compound_numbers(self):
        """Test compound numbers like 21, 34, 87 etc."""
        self.assertEqual(num2words(21, lang='af'), "een-en-twintig")
        self.assertEqual(num2words(34, lang='af'), "vier-en-dertig")
        self.assertEqual(num2words(56, lang='af'), "ses-en-vyftig")
        self.assertEqual(num2words(87, lang='af'), "sewe-en-tagtig")
        self.assertEqual(num2words(99, lang='af'), "nege-en-negentig")

    def test_cardinal_hundreds(self):
        """Test hundreds"""
        self.assertEqual(num2words(100, lang='af'), "een honderd")
        self.assertEqual(num2words(200, lang='af'), "twee honderd")
        self.assertEqual(num2words(300, lang='af'), "drie honderd")
        self.assertEqual(num2words(500, lang='af'), "vyf honderd")
        self.assertEqual(num2words(900, lang='af'), "nege honderd")

    def test_cardinal_hundreds_with_compound(self):
        """Test hundreds with compound numbers"""
        self.assertEqual(num2words(101, lang='af'), "een honderd een")
        self.assertEqual(num2words(125, lang='af'), "een honderd vyf-en-twintig")
        self.assertEqual(num2words(234, lang='af'), "twee honderd vier-en-dertig")
        self.assertEqual(num2words(456, lang='af'), "vier honderd ses-en-vyftig")
        self.assertEqual(num2words(789, lang='af'), "sewe honderd nege-en-tagtig")

    def test_cardinal_thousands(self):
        """Test thousands"""
        self.assertEqual(num2words(1000, lang='af'), "een duisend")
        self.assertEqual(num2words(2000, lang='af'), "twee duisend")
        self.assertEqual(num2words(5000, lang='af'), "vyf duisend")
        self.assertEqual(num2words(10000, lang='af'), "tien duisend")
        self.assertEqual(num2words(11000, lang='af'), "elf duisend")
        self.assertEqual(num2words(100000, lang='af'), "een honderd duisend")

    def test_cardinal_thousands_with_compound(self):
        """Test thousands with compound numbers"""
        self.assertEqual(num2words(1001, lang='af'), "een duisend een")
        self.assertEqual(num2words(1234, lang='af'), "een duisend twee honderd vier-en-dertig")
        self.assertEqual(num2words(12345, lang='af'), "twaalf duisend drie honderd vyf-en-veertig")

    def test_cardinal_millions(self):
        """Test millions"""
        self.assertEqual(num2words(1000000, lang='af'), "een miljoen")
        self.assertEqual(num2words(2000000, lang='af'), "twee miljoen")
        self.assertEqual(num2words(5000000, lang='af'), "vyf miljoen")

    def test_cardinal_large_numbers(self):
        """Test larger numbers"""
        self.assertEqual(num2words(1000000000, lang='af'), "een miljard")
        self.assertEqual(num2words(2000000000, lang='af'), "twee miljard")
        self.assertEqual(num2words(1000000000000, lang='af'), "een biljoen")

    def test_ordinal_basic_numbers(self):
        """Test basic ordinal numbers"""
        self.assertEqual(num2words(1, ordinal=True, lang='af'), "eerste")
        self.assertEqual(num2words(2, ordinal=True, lang='af'), "tweede")
        self.assertEqual(num2words(3, ordinal=True, lang='af'), "derde")
        self.assertEqual(num2words(4, ordinal=True, lang='af'), "vierde")
        self.assertEqual(num2words(5, ordinal=True, lang='af'), "vyfde")
        self.assertEqual(num2words(6, ordinal=True, lang='af'), "sesde")
        self.assertEqual(num2words(7, ordinal=True, lang='af'), "sewende")
        self.assertEqual(num2words(8, ordinal=True, lang='af'), "agste")
        self.assertEqual(num2words(9, ordinal=True, lang='af'), "negende")
        self.assertEqual(num2words(10, ordinal=True, lang='af'), "tiende")

    def test_ordinal_teens(self):
        """Test ordinal teen numbers"""
        self.assertEqual(num2words(11, ordinal=True, lang='af'), "elfde")
        self.assertEqual(num2words(12, ordinal=True, lang='af'), "twaalfde")
        self.assertEqual(num2words(13, ordinal=True, lang='af'), "dertiende")
        self.assertEqual(num2words(14, ordinal=True, lang='af'), "veertiende")
        self.assertEqual(num2words(15, ordinal=True, lang='af'), "vyftiende")
        self.assertEqual(num2words(16, ordinal=True, lang='af'), "sestiende")
        self.assertEqual(num2words(17, ordinal=True, lang='af'), "sewentiende")
        self.assertEqual(num2words(18, ordinal=True, lang='af'), "agttiende")
        self.assertEqual(num2words(19, ordinal=True, lang='af'), "negentiende")
        self.assertEqual(num2words(20, ordinal=True, lang='af'), "twintigste")

    def test_ordinal_tens(self):
        """Test ordinal tens"""
        self.assertEqual(num2words(30, ordinal=True, lang='af'), "dertigste")
        self.assertEqual(num2words(40, ordinal=True, lang='af'), "veertigste")
        self.assertEqual(num2words(50, ordinal=True, lang='af'), "vyftigste")
        self.assertEqual(num2words(60, ordinal=True, lang='af'), "sestigste")
        self.assertEqual(num2words(70, ordinal=True, lang='af'), "sewentigste")
        self.assertEqual(num2words(80, ordinal=True, lang='af'), "tagtigste")
        self.assertEqual(num2words(90, ordinal=True, lang='af'), "negentigste")

    def test_ordinal_hundreds_and_larger(self):
        """Test ordinal hundreds and larger numbers"""
        self.assertEqual(num2words(100, ordinal=True, lang='af'), "een honderdste")
        self.assertEqual(num2words(1000, ordinal=True, lang='af'), "een duisendste")
        self.assertEqual(num2words(1000000, ordinal=True, lang='af'), "een miljoenste")

    def test_ordinal_compound_numbers(self):
        """Test compound ordinal numbers"""
        self.assertEqual(num2words(21, ordinal=True, lang='af'), "een-en-twintigste")
        self.assertEqual(num2words(34, ordinal=True, lang='af'), "vier-en-dertigste")
        self.assertEqual(num2words(101, ordinal=True, lang='af'), "een honderd eerste")

    def test_ordinal_num(self):
        """Test ordinal number format (1st, 2nd, etc.)"""
        self.assertEqual(num2words(1, lang='af', to='ordinal_num'), "1ste")
        self.assertEqual(num2words(2, lang='af', to='ordinal_num'), "2de")
        self.assertEqual(num2words(3, lang='af', to='ordinal_num'), "3de")
        self.assertEqual(num2words(4, lang='af', to='ordinal_num'), "4de")
        self.assertEqual(num2words(21, lang='af', to='ordinal_num'), "21ste")
        self.assertEqual(num2words(22, lang='af', to='ordinal_num'), "22ste")
        self.assertEqual(num2words(23, lang='af', to='ordinal_num'), "23ste")

    def test_decimal_numbers(self):
        """Test decimal numbers"""
        self.assertEqual(num2words(3.14, lang='af'), "drie komma een vier")
        self.assertEqual(num2words(0.5, lang='af'), "nul komma vyf")
        self.assertEqual(num2words(12.34, lang='af'), "twaalf komma drie vier")
        self.assertEqual(num2words(123.456, lang='af'), "een honderd drie-en-twintig komma vier vyf ses")

    def test_negative_numbers(self):
        """Test negative numbers"""
        self.assertEqual(num2words(-1, lang='af'), "minus een")
        self.assertEqual(num2words(-12, lang='af'), "minus twaalf")
        self.assertEqual(num2words(-100, lang='af'), "minus een honderd")
        self.assertEqual(num2words(-1234, lang='af'), "minus een duisend twee honderd vier-en-dertig")

    def test_negative_decimals(self):
        """Test negative decimal numbers including edge cases"""
        self.assertEqual(num2words(-0.4, lang='af'), "minus nul komma vier")
        self.assertEqual(num2words(-0.5, lang='af'), "minus nul komma vyf")
        self.assertEqual(num2words(-0.04, lang='af'), "minus nul komma nul vier")
        self.assertEqual(num2words(-1.4, lang='af'), "minus een komma vier")
        self.assertEqual(num2words(-10.25, lang='af'), "minus tien komma twee vyf")

    def test_ordinal_negative_numbers_raise_error(self):
        """Test that negative numbers raise TypeError for ordinals"""
        self.assertRaises(TypeError, num2words, -1, ordinal=True, lang='af')
        self.assertRaises(TypeError, num2words, -12, ordinal=True, lang='af')

    def test_ordinal_float_numbers_raise_error(self):
        """Test that float numbers raise TypeError for ordinals"""
        self.assertRaises(TypeError, num2words, 3.14, ordinal=True, lang='af')
        self.assertRaises(TypeError, num2words, 0.5, ordinal=True, lang='af')

    def test_currency_zar(self):
        """Test South African Rand currency conversion"""
        for test_input, expected_result in TEST_CASES_TO_CURRENCY_ZAR:
            result = num2words(test_input, lang='af', to='currency', currency='ZAR')
            self.assertEqual(result, expected_result)

    def test_currency_eur(self):
        """Test Euro currency conversion"""
        for test_input, expected_result in TEST_CASES_TO_CURRENCY_EUR:
            result = num2words(test_input, lang='af', to='currency', currency='EUR')
            self.assertEqual(result, expected_result)

    def test_currency_usd(self):
        """Test US Dollar currency conversion"""
        for test_input, expected_result in TEST_CASES_TO_CURRENCY_USD:
            result = num2words(test_input, lang='af', to='currency', currency='USD')
            self.assertEqual(result, expected_result)

    def test_currency_with_no_cents(self):
        """Test currency conversion without cents"""
        # Test with decimal format (will still show cents part)
        result = num2words(100.00, lang='af', to='currency', currency='ZAR', cents=False)
        self.assertEqual(result, "een honderd rand en 00 sent")

        # Test with integer (no cents shown)
        result = num2words(100, lang='af', to='currency', currency='ZAR', cents=False)
        self.assertEqual(result, "een rand")

        result = num2words(50.25, lang='af', to='currency', currency='EUR', cents=False)
        self.assertEqual(result, "vyftig euro en 25 sent")

    def test_currency_with_different_separator(self):
        """Test currency conversion with different separator"""
        result = num2words(15.75, lang='af', to='currency', currency='USD',
                           separator=' plus ')

        self.assertEqual(result, "vyftien dollar plus  vyf-en-sewentig sent")

    def test_pluralize_method(self):
        """Test pluralization method"""
        converter = Num2Word_AF()

        # Test ZAR currency forms
        zar_major, zar_minor = converter.CURRENCY_FORMS['ZAR']
        self.assertEqual(converter.pluralize(1, zar_major), 'rand')
        self.assertEqual(converter.pluralize(2, zar_major), 'rand')  # rand is same for singular/plural
        self.assertEqual(converter.pluralize(1, zar_minor), 'sent')
        self.assertEqual(converter.pluralize(2, zar_minor), 'sent')  # sent is same for singular/plural

    def test_year_conversion(self):
        """Test year conversion"""
        self.assertEqual(num2words(2023, lang='af', to='year'), "twintig drie-en-twintig")
        self.assertEqual(num2words(1999, lang='af', to='year'), "negentien nege-en-negentig")
        self.assertEqual(num2words(2000, lang='af', to='year'), "twee duisend")
        self.assertEqual(num2words(2001, lang='af', to='year'), "twee duisend een")

    def test_edge_cases(self):
        """Test edge cases and special numbers"""
        # Test zero variations
        self.assertEqual(num2words(0, lang='af'), "nul")
        self.assertEqual(num2words(0.0, lang='af'), "nul")

        # Test very large numbers
        self.assertEqual(num2words(999999999, lang='af'),
                         "nege honderd nege-en-negentig miljoen nege honderd nege-en-negentig duisend nege honderd nege-en-negentig")

    def test_special_ordinal_cases(self):
        """Test special cases for ordinals"""
        # Test 0th
        self.assertEqual(num2words(0, ordinal=True, lang='af'), "nullde")

        # Test compound ordinals with specific formatting
        self.assertEqual(num2words(81, ordinal=True, lang='af'), "een-en-tagtigste")
        self.assertEqual(num2words(101, ordinal=True, lang='af'), "een honderd eerste")
