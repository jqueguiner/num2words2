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

from num2words2 import num2words


class Num2WordsSWTest(TestCase):
    def test_basic_numbers(self):
        """Test basic numbers 0-19"""
        self.assertEqual(num2words(0, lang='sw'), "sifuri")
        self.assertEqual(num2words(1, lang='sw'), "moja")
        self.assertEqual(num2words(2, lang='sw'), "mbili")
        self.assertEqual(num2words(3, lang='sw'), "tatu")
        self.assertEqual(num2words(4, lang='sw'), "nne")
        self.assertEqual(num2words(5, lang='sw'), "tano")
        self.assertEqual(num2words(6, lang='sw'), "sita")
        self.assertEqual(num2words(7, lang='sw'), "saba")
        self.assertEqual(num2words(8, lang='sw'), "nane")
        self.assertEqual(num2words(9, lang='sw'), "tisa")
        self.assertEqual(num2words(10, lang='sw'), "kumi")
        self.assertEqual(num2words(11, lang='sw'), "kumi na moja")
        self.assertEqual(num2words(12, lang='sw'), "kumi na mbili")
        self.assertEqual(num2words(13, lang='sw'), "kumi na tatu")
        self.assertEqual(num2words(14, lang='sw'), "kumi na nne")
        self.assertEqual(num2words(15, lang='sw'), "kumi na tano")
        self.assertEqual(num2words(16, lang='sw'), "kumi na sita")
        self.assertEqual(num2words(17, lang='sw'), "kumi na saba")
        self.assertEqual(num2words(18, lang='sw'), "kumi na nane")
        self.assertEqual(num2words(19, lang='sw'), "kumi na tisa")

    def test_tens(self):
        """Test tens 20-90"""
        self.assertEqual(num2words(20, lang='sw'), "ishirini")
        self.assertEqual(num2words(30, lang='sw'), "thelathini")
        self.assertEqual(num2words(40, lang='sw'), "arobaini")
        self.assertEqual(num2words(50, lang='sw'), "hamsini")
        self.assertEqual(num2words(60, lang='sw'), "sitini")
        self.assertEqual(num2words(70, lang='sw'), "sabini")
        self.assertEqual(num2words(80, lang='sw'), "themanini")
        self.assertEqual(num2words(90, lang='sw'), "tisini")

    def test_compound_numbers(self):
        """Test compound numbers with 'na' connector"""
        self.assertEqual(num2words(21, lang='sw'), "ishirini na moja")
        self.assertEqual(num2words(25, lang='sw'), "ishirini na tano")
        self.assertEqual(num2words(33, lang='sw'), "thelathini na tatu")
        self.assertEqual(num2words(47, lang='sw'), "arobaini na saba")
        self.assertEqual(num2words(56, lang='sw'), "hamsini na sita")
        self.assertEqual(num2words(68, lang='sw'), "sitini na nane")
        self.assertEqual(num2words(79, lang='sw'), "sabini na tisa")
        self.assertEqual(num2words(84, lang='sw'), "themanini na nne")
        self.assertEqual(num2words(95, lang='sw'), "tisini na tano")
        self.assertEqual(num2words(99, lang='sw'), "tisini na tisa")

    def test_hundreds(self):
        """Test hundreds"""
        self.assertEqual(num2words(100, lang='sw'), "mia moja")
        self.assertEqual(num2words(200, lang='sw'), "mia mbili")
        self.assertEqual(num2words(300, lang='sw'), "mia tatu")
        self.assertEqual(num2words(400, lang='sw'), "mia nne")
        self.assertEqual(num2words(500, lang='sw'), "mia tano")
        self.assertEqual(num2words(600, lang='sw'), "mia sita")
        self.assertEqual(num2words(700, lang='sw'), "mia saba")
        self.assertEqual(num2words(800, lang='sw'), "mia nane")
        self.assertEqual(num2words(900, lang='sw'), "mia tisa")

    def test_hundreds_compound(self):
        """Test hundreds with additional units"""
        self.assertEqual(num2words(101, lang='sw'), "mia moja na moja")
        self.assertEqual(num2words(105, lang='sw'), "mia moja na tano")
        self.assertEqual(num2words(120, lang='sw'), "mia moja na ishirini")
        self.assertEqual(num2words(123, lang='sw'), "mia moja na ishirini na tatu")
        self.assertEqual(num2words(250, lang='sw'), "mia mbili na hamsini")
        self.assertEqual(num2words(365, lang='sw'), "mia tatu na sitini na tano")
        self.assertEqual(num2words(456, lang='sw'), "mia nne na hamsini na sita")
        self.assertEqual(num2words(789, lang='sw'), "mia saba na themanini na tisa")
        self.assertEqual(num2words(999, lang='sw'), "mia tisa na tisini na tisa")

    def test_thousands(self):
        """Test thousands"""
        self.assertEqual(num2words(1000, lang='sw'), "elfu moja")
        self.assertEqual(num2words(2000, lang='sw'), "elfu mbili")
        self.assertEqual(num2words(3000, lang='sw'), "elfu tatu")
        self.assertEqual(num2words(5000, lang='sw'), "elfu tano")
        self.assertEqual(num2words(10000, lang='sw'), "elfu kumi")
        self.assertEqual(num2words(15000, lang='sw'), "elfu kumi na tano")
        self.assertEqual(num2words(20000, lang='sw'), "elfu ishirini")

    def test_thousands_compound(self):
        """Test thousands with additional units"""
        self.assertEqual(num2words(1001, lang='sw'), "elfu moja na moja")
        self.assertEqual(num2words(1010, lang='sw'), "elfu moja na kumi")
        self.assertEqual(num2words(1100, lang='sw'), "elfu moja na mia moja")
        self.assertEqual(num2words(1234, lang='sw'), "elfu moja na mia mbili na thelathini na nne")
        self.assertEqual(num2words(2500, lang='sw'), "elfu mbili na mia tano")
        self.assertEqual(num2words(5678, lang='sw'), "elfu tano na mia sita na sabini na nane")
        self.assertEqual(num2words(12345, lang='sw'), "elfu kumi na mbili na mia tatu na arobaini na tano")

    def test_large_numbers(self):
        """Test larger numbers"""
        self.assertEqual(num2words(100000, lang='sw'), "laki moja")
        self.assertEqual(num2words(200000, lang='sw'), "laki mbili")
        self.assertEqual(num2words(1000000, lang='sw'), "milioni moja")
        self.assertEqual(num2words(2000000, lang='sw'), "milioni mbili")
        self.assertEqual(num2words(1000000000, lang='sw'), "bilioni moja")

    def test_negative_numbers(self):
        """Test negative numbers"""
        self.assertEqual(num2words(-1, lang='sw'), "hasi moja")
        self.assertEqual(num2words(-10, lang='sw'), "hasi kumi")
        self.assertEqual(num2words(-25, lang='sw'), "hasi ishirini na tano")
        self.assertEqual(num2words(-100, lang='sw'), "hasi mia moja")
        self.assertEqual(num2words(-1000, lang='sw'), "hasi elfu moja")

    def test_ordinal_numbers(self):
        """Test ordinal numbers"""
        self.assertEqual(num2words(1, lang='sw', to='ordinal'), "wa kwanza")
        self.assertEqual(num2words(2, lang='sw', to='ordinal'), "wa pili")
        self.assertEqual(num2words(3, lang='sw', to='ordinal'), "wa tatu")
        self.assertEqual(num2words(4, lang='sw', to='ordinal'), "wa nne")
        self.assertEqual(num2words(5, lang='sw', to='ordinal'), "wa tano")
        self.assertEqual(num2words(10, lang='sw', to='ordinal'), "wa kumi")
        self.assertEqual(num2words(11, lang='sw', to='ordinal'), "wa kumi na moja")
        self.assertEqual(num2words(21, lang='sw', to='ordinal'), "wa ishirini na moja")
        self.assertEqual(num2words(100, lang='sw', to='ordinal'), "wa mia moja")

    def test_ordinal_num(self):
        """Test ordinal numbers with suffix"""
        self.assertEqual(num2words(1, lang='sw', to='ordinal_num'), "1.")
        self.assertEqual(num2words(2, lang='sw', to='ordinal_num'), "2.")
        self.assertEqual(num2words(10, lang='sw', to='ordinal_num'), "10.")
        self.assertEqual(num2words(21, lang='sw', to='ordinal_num'), "21.")
        self.assertEqual(num2words(100, lang='sw', to='ordinal_num'), "100.")

    def test_currency(self):
        """Test currency conversion"""
        # Test with Tanzanian Shilling (TZS)
        self.assertEqual(
            num2words(1, lang='sw', to='currency', currency='TZS'),
            "moja shilingi"
        )
        self.assertEqual(
            num2words(2, lang='sw', to='currency', currency='TZS'),
            "mbili shilingi"
        )
        self.assertEqual(
            num2words(100, lang='sw', to='currency', currency='TZS'),
            "mia moja shilingi"
        )
        
        # Test with decimal amounts
        self.assertEqual(
            num2words(1.50, lang='sw', to='currency', currency='TZS'),
            "moja shilingi na hamsini senti"
        )
        self.assertEqual(
            num2words(10.25, lang='sw', to='currency', currency='TZS'),
            "kumi shilingi na ishirini na tano senti"
        )

        # Test with USD
        self.assertEqual(
            num2words(1, lang='sw', to='currency', currency='USD'),
            "moja dola"
        )
        self.assertEqual(
            num2words(5.75, lang='sw', to='currency', currency='USD'),
            "tano dola na sabini na tano senti"
        )

    def test_year(self):
        """Test year conversion"""
        self.assertEqual(num2words(2000, lang='sw', to='year'), "elfu mbili")
        self.assertEqual(num2words(2023, lang='sw', to='year'), "elfu mbili na ishirini na tatu")
        self.assertEqual(num2words(1995, lang='sw', to='year'), "elfu moja na mia tisa na tisini na tano")

    def test_decimal_numbers(self):
        """Test decimal numbers"""
        self.assertEqual(num2words(1.5, lang='sw'), "moja nukta tano")
        self.assertEqual(num2words(10.25, lang='sw'), "kumi nukta mbili tano")
        self.assertEqual(num2words(0.75, lang='sw'), "sifuri nukta saba tano")
        self.assertEqual(num2words(3.14, lang='sw'), "tatu nukta moja nne")

    def test_negative_decimals(self):
        """Test negative decimal numbers"""
        self.assertEqual(num2words(-1.5, lang='sw'), "hasi moja nukta tano")
        self.assertEqual(num2words(-0.25, lang='sw'), "hasi sifuri nukta mbili tano")
        self.assertEqual(num2words(-10.75, lang='sw'), "hasi kumi nukta saba tano")

    def test_edge_cases(self):
        """Test edge cases and special numbers"""
        # Test zero in different contexts
        self.assertEqual(num2words(0, lang='sw'), "sifuri")
        self.assertEqual(num2words(0.0, lang='sw'), "sifuri")
        
        # Test large round numbers
        self.assertEqual(num2words(1000000, lang='sw'), "milioni moja")
        self.assertEqual(num2words(2000000, lang='sw'), "milioni mbili")
        self.assertEqual(num2words(1000000000, lang='sw'), "bilioni moja")