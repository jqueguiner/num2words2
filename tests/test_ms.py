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


class Num2WordsMSTest(TestCase):
    def test_cardinal_basics(self):
        """Test basic cardinal numbers in Malay."""
        self.assertEqual(num2words(0, lang='ms'), 'kosong')
        self.assertEqual(num2words(1, lang='ms'), 'satu')
        self.assertEqual(num2words(2, lang='ms'), 'dua')
        self.assertEqual(num2words(3, lang='ms'), 'tiga')
        self.assertEqual(num2words(4, lang='ms'), 'empat')
        self.assertEqual(num2words(5, lang='ms'), 'lima')
        self.assertEqual(num2words(6, lang='ms'), 'enam')
        self.assertEqual(num2words(7, lang='ms'), 'tujuh')
        self.assertEqual(num2words(8, lang='ms'), 'lapan')
        self.assertEqual(num2words(9, lang='ms'), 'sembilan')

    def test_cardinal_tens(self):
        """Test tens in Malay."""
        self.assertEqual(num2words(10, lang='ms'), 'sepuluh')
        self.assertEqual(num2words(11, lang='ms'), 'sebelas')
        self.assertEqual(num2words(12, lang='ms'), 'dua belas')
        self.assertEqual(num2words(13, lang='ms'), 'tiga belas')
        self.assertEqual(num2words(14, lang='ms'), 'empat belas')
        self.assertEqual(num2words(15, lang='ms'), 'lima belas')
        self.assertEqual(num2words(16, lang='ms'), 'enam belas')
        self.assertEqual(num2words(17, lang='ms'), 'tujuh belas')
        self.assertEqual(num2words(18, lang='ms'), 'lapan belas')
        self.assertEqual(num2words(19, lang='ms'), 'sembilan belas')
        self.assertEqual(num2words(20, lang='ms'), 'dua puluh')
        self.assertEqual(num2words(30, lang='ms'), 'tiga puluh')
        self.assertEqual(num2words(40, lang='ms'), 'empat puluh')
        self.assertEqual(num2words(50, lang='ms'), 'lima puluh')
        self.assertEqual(num2words(60, lang='ms'), 'enam puluh')
        self.assertEqual(num2words(70, lang='ms'), 'tujuh puluh')
        self.assertEqual(num2words(80, lang='ms'), 'lapan puluh')
        self.assertEqual(num2words(90, lang='ms'), 'sembilan puluh')

    def test_cardinal_compound_tens(self):
        """Test compound numbers with tens."""
        self.assertEqual(num2words(21, lang='ms'), 'dua puluh satu')
        self.assertEqual(num2words(32, lang='ms'), 'tiga puluh dua')
        self.assertEqual(num2words(45, lang='ms'), 'empat puluh lima')
        self.assertEqual(num2words(67, lang='ms'), 'enam puluh tujuh')
        self.assertEqual(num2words(89, lang='ms'), 'lapan puluh sembilan')
        self.assertEqual(num2words(99, lang='ms'), 'sembilan puluh sembilan')

    def test_cardinal_hundreds(self):
        """Test hundreds in Malay."""
        self.assertEqual(num2words(100, lang='ms'), 'seratus')
        self.assertEqual(num2words(200, lang='ms'), 'dua ratus')
        self.assertEqual(num2words(300, lang='ms'), 'tiga ratus')
        self.assertEqual(num2words(400, lang='ms'), 'empat ratus')
        self.assertEqual(num2words(500, lang='ms'), 'lima ratus')
        self.assertEqual(num2words(600, lang='ms'), 'enam ratus')
        self.assertEqual(num2words(700, lang='ms'), 'tujuh ratus')
        self.assertEqual(num2words(800, lang='ms'), 'lapan ratus')
        self.assertEqual(num2words(900, lang='ms'), 'sembilan ratus')

    def test_cardinal_complex_hundreds(self):
        """Test complex numbers with hundreds."""
        self.assertEqual(num2words(101, lang='ms'), 'seratus satu')
        self.assertEqual(num2words(111, lang='ms'), 'seratus sebelas')
        self.assertEqual(num2words(212, lang='ms'), 'dua ratus dua belas')
        self.assertEqual(num2words(345,
                         lang='ms'), 'tiga ratus empat puluh lima')
        self.assertEqual(num2words(567,
                         lang='ms'), 'lima ratus enam puluh tujuh')
        self.assertEqual(
            num2words(891, lang='ms'), 'lapan ratus sembilan puluh satu')
        self.assertEqual(
            num2words(999, lang='ms'),
            'sembilan ratus sembilan puluh sembilan')

    def test_cardinal_thousands(self):
        """Test thousands in Malay."""
        self.assertEqual(num2words(1000, lang='ms'), 'seribu')
        self.assertEqual(num2words(2000, lang='ms'), 'dua ribu')
        self.assertEqual(num2words(3000, lang='ms'), 'tiga ribu')
        self.assertEqual(num2words(5000, lang='ms'), 'lima ribu')
        self.assertEqual(num2words(10000, lang='ms'), 'sepuluh ribu')
        self.assertEqual(num2words(15000, lang='ms'), 'lima belas ribu')
        self.assertEqual(num2words(25000, lang='ms'), 'dua puluh lima ribu')
        self.assertEqual(num2words(100000, lang='ms'), 'seratus ribu')
        self.assertEqual(num2words(999999, lang='ms'),
                         'sembilan ratus sembilan puluh sembilan ribu '
                         'sembilan ratus sembilan puluh sembilan')

    def test_cardinal_millions(self):
        """Test millions in Malay."""
        self.assertEqual(num2words(1000000, lang='ms'), 'satu juta')
        self.assertEqual(num2words(2000000, lang='ms'), 'dua juta')
        self.assertEqual(num2words(5000000, lang='ms'), 'lima juta')
        self.assertEqual(num2words(15000000, lang='ms'), 'lima belas juta')
        self.assertEqual(num2words(123456789, lang='ms'),
                         'seratus dua puluh tiga juta '
                         'empat ratus lima puluh enam ribu '
                         'tujuh ratus lapan puluh sembilan')

    def test_cardinal_billions(self):
        """Test billions in Malay."""
        self.assertEqual(num2words(1000000000, lang='ms'), 'satu bilion')
        self.assertEqual(num2words(2000000000, lang='ms'), 'dua bilion')
        self.assertEqual(num2words(5000000000, lang='ms'), 'lima bilion')

    def test_negative_numbers(self):
        """Test negative numbers in Malay."""
        self.assertEqual(num2words(-1, lang='ms'), 'negatif satu')
        self.assertEqual(num2words(-10, lang='ms'), 'negatif sepuluh')
        self.assertEqual(num2words(-25, lang='ms'), 'negatif dua puluh lima')
        self.assertEqual(num2words(-100, lang='ms'), 'negatif seratus')
        self.assertEqual(num2words(-1000, lang='ms'), 'negatif seribu')

    def test_ordinal_basics(self):
        """Test basic ordinal numbers in Malay."""
        self.assertEqual(num2words(1, lang='ms', to='ordinal'), 'pertama')
        self.assertEqual(num2words(2, lang='ms', to='ordinal'), 'kedua')
        self.assertEqual(num2words(3, lang='ms', to='ordinal'), 'ketiga')
        self.assertEqual(num2words(4, lang='ms', to='ordinal'), 'keempat')
        self.assertEqual(num2words(5, lang='ms', to='ordinal'), 'kelima')
        self.assertEqual(num2words(6, lang='ms', to='ordinal'), 'keenam')
        self.assertEqual(num2words(7, lang='ms', to='ordinal'), 'ketujuh')
        self.assertEqual(num2words(8, lang='ms', to='ordinal'), 'kelapan')
        self.assertEqual(num2words(9, lang='ms', to='ordinal'), 'kesembilan')
        self.assertEqual(num2words(10, lang='ms', to='ordinal'), 'kesepuluh')

    def test_ordinal_tens(self):
        """Test ordinal tens in Malay."""
        self.assertEqual(num2words(11, lang='ms', to='ordinal'), 'ke-sebelas')
        self.assertEqual(num2words(12,
                         lang='ms', to='ordinal'), 'ke-dua belas')
        self.assertEqual(num2words(20,
                         lang='ms', to='ordinal'), 'ke-dua puluh')
        self.assertEqual(num2words(30,
                         lang='ms', to='ordinal'), 'ke-tiga puluh')
        self.assertEqual(num2words(50,
                         lang='ms', to='ordinal'), 'ke-lima puluh')
        self.assertEqual(num2words(100, lang='ms', to='ordinal'), 'ke-seratus')
        self.assertEqual(num2words(1000, lang='ms', to='ordinal'), 'ke-seribu')

    def test_ordinal_num(self):
        """Test ordinal number formatting in Malay."""
        self.assertEqual(num2words(1, lang='ms', to='ordinal_num'), 'ke-1')
        self.assertEqual(num2words(2, lang='ms', to='ordinal_num'), 'ke-2')
        self.assertEqual(num2words(3, lang='ms', to='ordinal_num'), 'ke-3')
        self.assertEqual(num2words(10, lang='ms', to='ordinal_num'), 'ke-10')
        self.assertEqual(num2words(21, lang='ms', to='ordinal_num'), 'ke-21')
        self.assertEqual(num2words(100, lang='ms', to='ordinal_num'), 'ke-100')

    def test_currency(self):
        """Test currency in Malay."""
        self.assertEqual(
            num2words(1, lang='ms', to='currency', currency='MYR'),
            'kosong ringgit satu sen'
        )
        self.assertEqual(
            num2words(2, lang='ms', to='currency', currency='MYR'),
            'kosong ringgit dua sen'
        )
        self.assertEqual(
            num2words(5.50, lang='ms', to='currency', currency='MYR'),
            'lima ringgit lima puluh sen'
        )
        self.assertEqual(
            num2words(10.01, lang='ms', to='currency', currency='MYR'),
            'sepuluh ringgit satu sen'
        )
        self.assertEqual(
            num2words(100.25, lang='ms', to='currency', currency='MYR'),
            'seratus ringgit dua puluh lima sen'
        )
        self.assertEqual(
            num2words(1, lang='ms', to='currency', currency='SGD'),
            'kosong dolar satu sen'
        )
        self.assertEqual(
            num2words(5.25, lang='ms', to='currency', currency='SGD'),
            'lima dolar dua puluh lima sen'
        )

    def test_year(self):
        """Test year conversion in Malay."""
        self.assertEqual(num2words(1900, lang='ms', to='year'),
                         'seribu sembilan ratus')
        self.assertEqual(num2words(1999, lang='ms', to='year'),
                         'seribu sembilan ratus sembilan puluh sembilan')
        self.assertEqual(num2words(2000, lang='ms', to='year'),
                         'dua ribu')
        self.assertEqual(num2words(2001, lang='ms', to='year'),
                         'dua ribu satu')
        self.assertEqual(num2words(2020, lang='ms', to='year'),
                         'dua ribu dua puluh')
        self.assertEqual(num2words(2023, lang='ms', to='year'),
                         'dua ribu dua puluh tiga')
