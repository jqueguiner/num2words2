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

from num2words import num2words


class Num2WordsTLTest(TestCase):
    """Test suite for Tagalog number to words converter."""

    def test_zero(self):
        """Test zero conversion."""
        self.assertEqual(num2words(0, lang="tl"), "wala")

    def test_basic_digits_1_to_9(self):
        """Test basic digit conversion 1-9."""
        self.assertEqual(num2words(1, lang="tl"), "isa")
        self.assertEqual(num2words(2, lang="tl"), "dalawa")
        self.assertEqual(num2words(3, lang="tl"), "tatlo")
        self.assertEqual(num2words(4, lang="tl"), "apat")
        self.assertEqual(num2words(5, lang="tl"), "lima")
        self.assertEqual(num2words(6, lang="tl"), "anim")
        self.assertEqual(num2words(7, lang="tl"), "pito")
        self.assertEqual(num2words(8, lang="tl"), "walo")
        self.assertEqual(num2words(9, lang="tl"), "siyam")

    def test_ten(self):
        """Test ten conversion."""
        self.assertEqual(num2words(10, lang="tl"), "sampu")

    def test_teens_11_to_19(self):
        """Test teens conversion 11-19."""
        self.assertEqual(num2words(11, lang="tl"), "labing-isa")
        self.assertEqual(num2words(12, lang="tl"), "labindalawa")
        self.assertEqual(num2words(13, lang="tl"), "labintatlo")
        self.assertEqual(num2words(14, lang="tl"), "labing-apat")
        self.assertEqual(num2words(15, lang="tl"), "labinlima")
        self.assertEqual(num2words(16, lang="tl"), "labing-anim")
        self.assertEqual(num2words(17, lang="tl"), "labimpito")
        self.assertEqual(num2words(18, lang="tl"), "labinwalo")
        self.assertEqual(num2words(19, lang="tl"), "labinsiyam")

    def test_tens_20_to_90(self):
        """Test tens conversion 20-90."""
        self.assertEqual(num2words(20, lang="tl"), "dalawampu")
        self.assertEqual(num2words(30, lang="tl"), "tatlumpu")
        self.assertEqual(num2words(40, lang="tl"), "apatnapu")
        self.assertEqual(num2words(50, lang="tl"), "limampu")
        self.assertEqual(num2words(60, lang="tl"), "animnapu")
        self.assertEqual(num2words(70, lang="tl"), "pitumpu")
        self.assertEqual(num2words(80, lang="tl"), "walumpu")
        self.assertEqual(num2words(90, lang="tl"), "siyamnapu")

    def test_compound_numbers_21_to_99(self):
        """Test compound numbers 21-99."""
        self.assertEqual(num2words(21, lang="tl"), "dalawampu't isa")
        self.assertEqual(num2words(22, lang="tl"), "dalawampu't dalawa")
        self.assertEqual(num2words(25, lang="tl"), "dalawampu't lima")
        self.assertEqual(num2words(33, lang="tl"), "tatlumpu't tatlo")
        self.assertEqual(num2words(44, lang="tl"), "apatnapu't apat")
        self.assertEqual(num2words(55, lang="tl"), "limampu't lima")
        self.assertEqual(num2words(66, lang="tl"), "animnapu't anim")
        self.assertEqual(num2words(77, lang="tl"), "pitumpu't pito")
        self.assertEqual(num2words(88, lang="tl"), "walumpu't walo")
        self.assertEqual(num2words(99, lang="tl"), "siyamnapu't siyam")

    def test_hundreds_100_to_900(self):
        """Test hundreds conversion 100-900."""
        self.assertEqual(num2words(100, lang="tl"), "isandaan")
        self.assertEqual(num2words(200, lang="tl"), "dalawandaan")
        self.assertEqual(num2words(300, lang="tl"), "tatlondaan")
        self.assertEqual(num2words(400, lang="tl"), "apat na daan")
        self.assertEqual(num2words(500, lang="tl"), "lima na daan")
        self.assertEqual(num2words(600, lang="tl"), "anim na daan")
        self.assertEqual(num2words(700, lang="tl"), "pito na daan")
        self.assertEqual(num2words(800, lang="tl"), "walo na daan")
        self.assertEqual(num2words(900, lang="tl"), "siyam na daan")

    def test_hundreds_with_tens_and_units(self):
        """Test hundreds combined with tens and units."""
        self.assertEqual(num2words(101, lang="tl"), "isandaan at isa")
        self.assertEqual(num2words(110, lang="tl"), "isandaan at sampu")
        self.assertEqual(num2words(111, lang="tl"), "isandaan at labing-isa")
        self.assertEqual(num2words(121, lang="tl"), "isandaan at dalawampu't isa")
        self.assertEqual(num2words(150, lang="tl"), "isandaan at limampu")
        self.assertEqual(num2words(199, lang="tl"), "isandaan at siyamnapu't siyam")
        self.assertEqual(num2words(250, lang="tl"), "dalawandaan at limampu")
        self.assertEqual(num2words(321, lang="tl"), "tatlondaan at dalawampu't isa")
        self.assertEqual(num2words(456, lang="tl"), "apat na daan at limampu't anim")
        self.assertEqual(num2words(789, lang="tl"), "pito na daan at walumpu't siyam")
        self.assertEqual(num2words(999, lang="tl"), "siyam na daan at siyamnapu't siyam")

    def test_thousands_1000_to_9000(self):
        """Test thousands conversion 1000-9000."""
        self.assertEqual(num2words(1000, lang="tl"), "isanlibo")
        self.assertEqual(num2words(2000, lang="tl"), "dalawanlibo")
        self.assertEqual(num2words(3000, lang="tl"), "tatlonlibo")
        self.assertEqual(num2words(4000, lang="tl"), "apat na libo")
        self.assertEqual(num2words(5000, lang="tl"), "lima na libo")
        self.assertEqual(num2words(6000, lang="tl"), "anim na libo")
        self.assertEqual(num2words(7000, lang="tl"), "pito na libo")
        self.assertEqual(num2words(8000, lang="tl"), "walo na libo")
        self.assertEqual(num2words(9000, lang="tl"), "siyam na libo")

    def test_thousands_with_hundreds_tens_units(self):
        """Test thousands combined with hundreds, tens, and units."""
        self.assertEqual(num2words(1001, lang="tl"), "isanlibo at isa")
        self.assertEqual(num2words(1010, lang="tl"), "isanlibo at sampu")
        self.assertEqual(num2words(1100, lang="tl"), "isanlibo at isandaan")
        self.assertEqual(num2words(1111, lang="tl"), "isanlibo at isandaan at labing-isa")
        self.assertEqual(num2words(1234, lang="tl"), "isanlibo at dalawandaan at tatlumpu't apat")
        self.assertEqual(num2words(2500, lang="tl"), "dalawanlibo at lima na daan")
        self.assertEqual(num2words(3456, lang="tl"), "tatlonlibo at apat na daan at limampu't anim")
        self.assertEqual(num2words(9999, lang="tl"), "siyam na libo at siyam na daan at siyamnapu't siyam")

    def test_ten_thousands_to_hundred_thousands(self):
        """Test ten thousands to hundred thousands."""
        self.assertEqual(num2words(10000, lang="tl"), "sampung libo")
        self.assertEqual(num2words(11000, lang="tl"), "labing-isang libo")
        self.assertEqual(num2words(20000, lang="tl"), "dalawampung libo")
        self.assertEqual(num2words(25000, lang="tl"), "dalawampu't limang libo")
        self.assertEqual(num2words(50000, lang="tl"), "limampung libo")
        self.assertEqual(num2words(100000, lang="tl"), "isandaang libo")
        self.assertEqual(num2words(123456, lang="tl"), "isandaan at dalawampu't tatlong libo at apat na daan at limampu't anim")
        self.assertEqual(num2words(999999, lang="tl"), "siyam na daan at siyamnapu't siyam na libo at siyam na daan at siyamnapu't siyam")

    def test_millions(self):
        """Test millions conversion."""
        self.assertEqual(num2words(1000000, lang="tl"), "isang milyon")
        self.assertEqual(num2words(2000000, lang="tl"), "dalawang milyon")
        self.assertEqual(num2words(3000000, lang="tl"), "tatlong milyon")
        self.assertEqual(num2words(10000000, lang="tl"), "sampung milyon")
        self.assertEqual(num2words(100000000, lang="tl"), "isandaang milyon")

    def test_millions_with_smaller_units(self):
        """Test millions combined with smaller units."""
        self.assertEqual(num2words(1000001, lang="tl"), "isang milyon at isa")
        self.assertEqual(num2words(1001000, lang="tl"), "isang milyon at isanlibo")
        self.assertEqual(num2words(1001001, lang="tl"), "isang milyon at isanlibo at isa")
        self.assertEqual(num2words(1234567, lang="tl"), "isang milyon at dalawandaan at tatlumpu't apat na libo at lima na daan at animnapu't pito")
        self.assertEqual(num2words(12345678, lang="tl"), "labindalawang milyon at tatlondaan at apatnapu't lima na libo at anim na daan at pitumpu't walo")

    def test_billions(self):
        """Test billions conversion."""
        self.assertEqual(num2words(1000000000, lang="tl"), "isang bilyon")
        self.assertEqual(num2words(2000000000, lang="tl"), "dalawang bilyon")
        self.assertEqual(num2words(1000000001, lang="tl"), "isang bilyon at isa")
        self.assertEqual(num2words(1000001000, lang="tl"), "isang bilyon at isanlibo")
        self.assertEqual(num2words(1001000000, lang="tl"), "isang bilyon at isang milyon")

    def test_negative_numbers(self):
        """Test negative numbers conversion."""
        self.assertEqual(num2words(-1, lang="tl"), "negatibong isa")
        self.assertEqual(num2words(-10, lang="tl"), "negatibong sampu")
        self.assertEqual(num2words(-100, lang="tl"), "negatibong isandaan")
        self.assertEqual(num2words(-1000, lang="tl"), "negatibong isanlibo")
        self.assertEqual(num2words(-1000000, lang="tl"), "negatibong isang milyon")

    def test_decimal_numbers(self):
        """Test decimal numbers conversion."""
        self.assertEqual(num2words(1.5, lang="tl"), "isa punto lima")
        self.assertEqual(num2words(10.25, lang="tl"), "sampu punto dalawampu't lima")
        self.assertEqual(num2words(123.45, lang="tl"), "isandaan at dalawampu't tatlo punto apatnapu't lima")
        self.assertEqual(num2words(0.5, lang="tl"), "wala punto lima")
        self.assertEqual(num2words(0.01, lang="tl"), "wala punto isa")
        self.assertEqual(num2words(0.99, lang="tl"), "wala punto siyamnapu't siyam")

    def test_negative_decimals(self):
        """Test negative decimal numbers conversion."""
        self.assertEqual(num2words(-0.4, lang="tl"), "negatibong wala punto apat")
        self.assertEqual(num2words(-0.5, lang="tl"), "negatibong wala punto lima")
        self.assertEqual(num2words(-1.4, lang="tl"), "negatibong isa punto apat")
        self.assertEqual(num2words(-10.25, lang="tl"), "negatibong sampu punto dalawampu't lima")

    def test_ordinal_numbers(self):
        """Test ordinal numbers conversion."""
        self.assertEqual(num2words(1, lang="tl", to="ordinal"), "una")
        self.assertEqual(num2words(2, lang="tl", to="ordinal"), "pangalawa")
        self.assertEqual(num2words(3, lang="tl", to="ordinal"), "pangatlo")
        self.assertEqual(num2words(4, lang="tl", to="ordinal"), "pang-apat")
        self.assertEqual(num2words(5, lang="tl", to="ordinal"), "panlima")
        self.assertEqual(num2words(6, lang="tl", to="ordinal"), "pang-anim")
        self.assertEqual(num2words(7, lang="tl", to="ordinal"), "pampito")
        self.assertEqual(num2words(8, lang="tl", to="ordinal"), "panwalo")
        self.assertEqual(num2words(9, lang="tl", to="ordinal"), "pansiyam")
        self.assertEqual(num2words(10, lang="tl", to="ordinal"), "pansampu")

    def test_ordinal_larger_numbers(self):
        """Test ordinal numbers for larger values."""
        self.assertEqual(num2words(11, lang="tl", to="ordinal"), "pang-labing-isa")
        self.assertEqual(num2words(20, lang="tl", to="ordinal"), "pandalawampu")
        self.assertEqual(num2words(21, lang="tl", to="ordinal"), "pang-dalawampu't isa")
        self.assertEqual(num2words(100, lang="tl", to="ordinal"), "pang-isandaan")
        self.assertEqual(num2words(1000, lang="tl", to="ordinal"), "pang-isanlibo")
        self.assertEqual(num2words(1000000, lang="tl", to="ordinal"), "pang-isang milyon")

    def test_ordinal_num(self):
        """Test ordinal number with suffix."""
        self.assertEqual(num2words(1, lang="tl", to="ordinal_num"), "1st")
        self.assertEqual(num2words(2, lang="tl", to="ordinal_num"), "2nd")
        self.assertEqual(num2words(3, lang="tl", to="ordinal_num"), "3rd")
        self.assertEqual(num2words(4, lang="tl", to="ordinal_num"), "4th")
        self.assertEqual(num2words(21, lang="tl", to="ordinal_num"), "21st")
        self.assertEqual(num2words(22, lang="tl", to="ordinal_num"), "22nd")
        self.assertEqual(num2words(23, lang="tl", to="ordinal_num"), "23rd")
        self.assertEqual(num2words(100, lang="tl", to="ordinal_num"), "100th")

    def test_currency_pesos(self):
        """Test Philippine Peso currency conversion."""
        # Test whole pesos
        self.assertEqual(num2words(1, lang="tl", to="currency", currency="PHP"), "isang piso")
        self.assertEqual(num2words(2, lang="tl", to="currency", currency="PHP"), "dalawang piso")
        self.assertEqual(num2words(10, lang="tl", to="currency", currency="PHP"), "sampung piso")
        self.assertEqual(num2words(100, lang="tl", to="currency", currency="PHP"), "isandaang piso")

        # Test pesos with centavos
        self.assertEqual(num2words(1.50, lang="tl", to="currency", currency="PHP"), "isang piso at limampung sentimo")
        self.assertEqual(num2words(10.25, lang="tl", to="currency", currency="PHP"), "sampung piso at dalawampu't limang sentimo")
        self.assertEqual(num2words(0.50, lang="tl", to="currency", currency="PHP"), "limampung sentimo")
        self.assertEqual(num2words(0.01, lang="tl", to="currency", currency="PHP"), "isang sentimo")

    def test_currency_dollars(self):
        """Test US Dollar currency conversion."""
        self.assertEqual(num2words(1, lang="tl", to="currency", currency="USD"), "isang dolyar")
        self.assertEqual(num2words(5, lang="tl", to="currency", currency="USD"), "limang dolyar")
        self.assertEqual(num2words(1.50, lang="tl", to="currency", currency="USD"), "isang dolyar at limampung sentimo")
        self.assertEqual(num2words(0.25, lang="tl", to="currency", currency="USD"), "dalawampu't limang sentimo")

    def test_year_conversion(self):
        """Test year conversion."""
        self.assertEqual(num2words(1990, lang="tl", to="year"), "isanlibo at siyam na daan at siyamnapu")
        self.assertEqual(num2words(2000, lang="tl", to="year"), "dalawanlibo")
        self.assertEqual(num2words(2020, lang="tl", to="year"), "dalawanlibo at dalawampu")
        self.assertEqual(num2words(2024, lang="tl", to="year"), "dalawanlibo at dalawampu't apat")

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Large numbers
        self.assertEqual(num2words(999999999, lang="tl"), "siyam na daan at siyamnapu't siyam na milyon at siyam na daan at siyamnapu't siyam na libo at siyam na daan at siyamnapu't siyam")
        
        # Very small decimals
        self.assertEqual(num2words(0.001, lang="tl"), "wala punto isa")
        
        # Negative large numbers
        self.assertEqual(num2words(-1000000, lang="tl"), "negatibong isang milyon")

    def test_special_tagalog_number_patterns(self):
        """Test special Tagalog number patterns and contractions."""
        # Test specific Tagalog contractions and special cases
        self.assertEqual(num2words(11, lang="tl"), "labing-isa")  # labing + isa with hyphen
        self.assertEqual(num2words(12, lang="tl"), "labindalawa")  # labin + dalawa without hyphen
        self.assertEqual(num2words(14, lang="tl"), "labing-apat")  # labing + apat with hyphen
        self.assertEqual(num2words(16, lang="tl"), "labing-anim")  # labing + anim with hyphen
        self.assertEqual(num2words(17, lang="tl"), "labimpito")   # labin + pito contraction
        self.assertEqual(num2words(18, lang="tl"), "labinwalo")   # labin + walo contraction
        
        # Test compound numbers with "at" connector
        self.assertEqual(num2words(101, lang="tl"), "isandaan at isa")
        self.assertEqual(num2words(1001, lang="tl"), "isanlibo at isa")
        
        # Test "na" spacing in hundreds and thousands
        self.assertEqual(num2words(400, lang="tl"), "apat na daan")
        self.assertEqual(num2words(4000, lang="tl"), "apat na libo")