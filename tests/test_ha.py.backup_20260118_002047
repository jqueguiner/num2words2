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
from num2words2.lang_HA import Num2Word_HA


class Num2WordsHATest(TestCase):
    """Test suite for Hausa number to words converter."""

    def test_basic_cardinal_numbers(self):
        """Test basic cardinal number conversion."""
        # Single digits
        self.assertEqual(num2words(0, lang="ha"), "sifiri")
        self.assertEqual(num2words(1, lang="ha"), "ɗaya")
        self.assertEqual(num2words(2, lang="ha"), "biyu")
        self.assertEqual(num2words(3, lang="ha"), "uku")
        self.assertEqual(num2words(4, lang="ha"), "huɗu")
        self.assertEqual(num2words(5, lang="ha"), "biyar")
        self.assertEqual(num2words(6, lang="ha"), "shida")
        self.assertEqual(num2words(7, lang="ha"), "bakwai")
        self.assertEqual(num2words(8, lang="ha"), "takwas")
        self.assertEqual(num2words(9, lang="ha"), "tara")

        # Ten and teens
        self.assertEqual(num2words(10, lang="ha"), "goma")
        self.assertEqual(num2words(11, lang="ha"), "sha ɗaya")
        self.assertEqual(num2words(12, lang="ha"), "sha biyu")
        self.assertEqual(num2words(13, lang="ha"), "sha uku")
        self.assertEqual(num2words(14, lang="ha"), "sha huɗu")
        self.assertEqual(num2words(15, lang="ha"), "sha biyar")
        self.assertEqual(num2words(16, lang="ha"), "sha shida")
        self.assertEqual(num2words(17, lang="ha"), "sha bakwai")
        self.assertEqual(num2words(18, lang="ha"), "sha takwas")
        self.assertEqual(num2words(19, lang="ha"), "sha tara")

        # Tens
        self.assertEqual(num2words(20, lang="ha"), "ashirin")
        self.assertEqual(num2words(21, lang="ha"), "ashirin da ɗaya")
        self.assertEqual(num2words(30, lang="ha"), "talatin")
        self.assertEqual(num2words(35, lang="ha"), "talatin da biyar")
        self.assertEqual(num2words(40, lang="ha"), "arba'in")
        self.assertEqual(num2words(50, lang="ha"), "hamsin")
        self.assertEqual(num2words(60, lang="ha"), "sittin")
        self.assertEqual(num2words(70, lang="ha"), "saba'in")
        self.assertEqual(num2words(80, lang="ha"), "tamanin")
        self.assertEqual(num2words(90, lang="ha"), "casa'in")
        self.assertEqual(num2words(99, lang="ha"), "casa'in da tara")

        # Hundreds
        self.assertEqual(num2words(100, lang="ha"), "ɗari")
        self.assertEqual(num2words(101, lang="ha"), "ɗari da ɗaya")
        self.assertEqual(num2words(111, lang="ha"), "ɗari sha ɗaya")
        self.assertEqual(num2words(120, lang="ha"), "ɗari ashirin")
        self.assertEqual(num2words(200, lang="ha"), "ɗari biyu")
        self.assertEqual(num2words(300, lang="ha"), "ɗari uku")
        self.assertEqual(num2words(999, lang="ha"), "ɗari tara casa'in da tara")

    def test_large_cardinal_numbers(self):
        """Test large cardinal number conversion."""
        # Thousands
        self.assertEqual(num2words(1000, lang="ha"), "dubu")
        self.assertEqual(num2words(1001, lang="ha"), "dubu da ɗaya")
        self.assertEqual(num2words(1111, lang="ha"), "dubu ɗari sha ɗaya")
        self.assertEqual(num2words(2000, lang="ha"), "dubu biyu")
        self.assertEqual(num2words(10000, lang="ha"), "dubu goma")
        self.assertEqual(num2words(100000, lang="ha"), "dubu ɗari")

        # Millions
        self.assertEqual(num2words(1000000, lang="ha"), "miliyan")
        self.assertEqual(num2words(2000000, lang="ha"), "miliyan biyu")
        self.assertEqual(num2words(1000001, lang="ha"), "miliyan da ɗaya")

    def test_negative_numbers(self):
        """Test negative number conversion."""
        self.assertEqual(num2words(-1, lang="ha"), "ban ɗaya")
        self.assertEqual(num2words(-10, lang="ha"), "ban goma")
        self.assertEqual(num2words(-100, lang="ha"), "ban ɗari")
        self.assertEqual(num2words(-1000, lang="ha"), "ban dubu")

    def test_decimal_numbers(self):
        """Test decimal number conversion."""
        self.assertEqual(num2words(1.5, lang="ha"), "ɗaya wajen biyar")
        self.assertEqual(num2words(10.25, lang="ha"), "goma wajen ashirin da biyar")
        self.assertEqual(num2words(0.1, lang="ha"), "sifiri wajen ɗaya")

    def test_ordinal_numbers(self):
        """Test ordinal number conversion."""
        self.assertEqual(num2words(1, lang="ha", to="ordinal"), "na farko")
        self.assertEqual(num2words(2, lang="ha", to="ordinal"), "na biyu")
        self.assertEqual(num2words(3, lang="ha", to="ordinal"), "na uku")
        self.assertEqual(num2words(10, lang="ha", to="ordinal"), "na goma")
        self.assertEqual(num2words(21, lang="ha", to="ordinal"), "na ashirin da ɗaya")
        self.assertEqual(num2words(100, lang="ha", to="ordinal"), "na ɗari")

    def test_ordinal_num(self):
        """Test ordinal number conversion with numerals."""
        self.assertEqual(num2words(1, lang="ha", to="ordinal_num"), "1st")
        self.assertEqual(num2words(2, lang="ha", to="ordinal_num"), "2nd")

        self.assertEqual(num2words(3, lang="ha", to="ordinal_num"), "3rd")
        self.assertEqual(num2words(4, lang="ha", to="ordinal_num"), "4th")
        self.assertEqual(num2words(21, lang="ha", to="ordinal_num"), "21st")
        self.assertEqual(num2words(22, lang="ha", to="ordinal_num"), "22nd")
        self.assertEqual(num2words(23, lang="ha", to="ordinal_num"), "23rd")
        self.assertEqual(num2words(101, lang="ha", to="ordinal_num"), "101st")

    def test_year_conversion(self):
        """Test year conversion."""
        self.assertEqual(num2words(1990, lang="ha", to="year"), "dubu ɗari tara casa'in")
        self.assertEqual(num2words(2000, lang="ha", to="year"), "dubu biyu")
        self.assertEqual(num2words(2023, lang="ha", to="year"), "dubu biyu ashirin da uku")

    def test_currency_conversion(self):
        """Test currency conversion."""
        # Default Naira currency
        self.assertEqual(num2words(1, lang="ha", to="currency"), "naira ɗaya")
        self.assertEqual(num2words(100, lang="ha", to="currency"), "naira ɗari")
        self.assertEqual(num2words(1.50, lang="ha", to="currency"), "naira ɗaya da kobo hamsin")

        # USD currency
        converter = Num2Word_HA()
        self.assertEqual(converter.to_currency(1, currency='USD'), "dala ɗaya")
        self.assertEqual(converter.to_currency(100, currency='USD'), "dala ɗari")

    def test_edge_cases(self):
        """Test edge cases and special scenarios."""
        # Zero
        self.assertEqual(num2words(0, lang="ha"), "sifiri")

        # Large numbers
        self.assertEqual(num2words(1000000000, lang="ha"), "biliyan")

        # Complex combinations
        self.assertEqual(num2words(1234, lang="ha"), "dubu ɗari biyu talatin da huɗu")
        self.assertEqual(num2words(5678, lang="ha"), "dubu biyar ɗari shida saba'in da takwas")

    def test_class_instance(self):
        """Test direct class instance usage."""
        converter = Num2Word_HA()

        # Basic functionality
        self.assertEqual(converter.to_cardinal(5), "biyar")
        self.assertEqual(converter.to_cardinal(15), "sha biyar")
        self.assertEqual(converter.to_cardinal(50), "hamsin")

        # Ordinal functionality
        self.assertEqual(converter.to_ordinal(1), "na farko")
        self.assertEqual(converter.to_ordinal(5), "na biyar")

        # Currency functionality
        self.assertEqual(converter.to_currency(10), "naira goma")

    def test_complex_numbers(self):
        """Test more complex number combinations."""
        # Complex hundreds
        self.assertEqual(num2words(456, lang="ha"), "ɗari huɗu hamsin da shida")
        self.assertEqual(num2words(789, lang="ha"), "ɗari bakwai tamanin da tara")

        # Complex thousands
        self.assertEqual(num2words(2345, lang="ha"), "dubu biyu ɗari uku arba'in da biyar")
        self.assertEqual(num2words(9876, lang="ha"), "dubu tara ɗari takwas saba'in da shida")

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        converter = Num2Word_HA()

        # Very large numbers should still work or raise appropriate errors
        try:
            result = converter.to_cardinal(10**15)
            self.assertTrue(isinstance(result, str))
        except (ValueError, NotImplementedError):  # pragma: no cover
            # Either is acceptable for very large numbers
            pass
