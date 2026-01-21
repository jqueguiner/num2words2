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


class Num2WordsBGTest(TestCase):
    def test_cardinal_basics(self):
        """Test basic cardinal numbers in Bulgarian."""
        self.assertEqual(num2words(0, lang='bg'), 'нула')
        self.assertEqual(num2words(1, lang='bg'), 'един')
        self.assertEqual(num2words(2, lang='bg'), 'два')
        self.assertEqual(num2words(3, lang='bg'), 'три')
        self.assertEqual(num2words(4, lang='bg'), 'четири')
        self.assertEqual(num2words(5, lang='bg'), 'пет')
        self.assertEqual(num2words(6, lang='bg'), 'шест')
        self.assertEqual(num2words(7, lang='bg'), 'седем')
        self.assertEqual(num2words(8, lang='bg'), 'осем')
        self.assertEqual(num2words(9, lang='bg'), 'девет')

    def test_cardinal_tens(self):
        """Test tens in Bulgarian."""
        self.assertEqual(num2words(10, lang='bg'), 'десет')
        self.assertEqual(num2words(11, lang='bg'), 'единадесет')
        self.assertEqual(num2words(12, lang='bg'), 'дванадесет')
        self.assertEqual(num2words(13, lang='bg'), 'тринадесет')
        self.assertEqual(num2words(14, lang='bg'), 'четиринадесет')
        self.assertEqual(num2words(15, lang='bg'), 'петнадесет')
        self.assertEqual(num2words(16, lang='bg'), 'шестнадесет')
        self.assertEqual(num2words(17, lang='bg'), 'седемнадесет')
        self.assertEqual(num2words(18, lang='bg'), 'осемнадесет')
        self.assertEqual(num2words(19, lang='bg'), 'деветнадесет')
        self.assertEqual(num2words(20, lang='bg'), 'двадесет')
        self.assertEqual(num2words(30, lang='bg'), 'тридесет')
        self.assertEqual(num2words(40, lang='bg'), 'четиридесет')
        self.assertEqual(num2words(50, lang='bg'), 'петдесет')
        self.assertEqual(num2words(60, lang='bg'), 'шестдесет')
        self.assertEqual(num2words(70, lang='bg'), 'седемдесет')
        self.assertEqual(num2words(80, lang='bg'), 'осемдесет')
        self.assertEqual(num2words(90, lang='bg'), 'деветдесет')

    def test_cardinal_compound_tens(self):
        """Test compound numbers with tens."""
        self.assertEqual(num2words(21, lang='bg'), 'двадесет и един')
        self.assertEqual(num2words(32, lang='bg'), 'тридесет и два')
        self.assertEqual(num2words(45, lang='bg'), 'четиридесет и пет')
        self.assertEqual(num2words(67, lang='bg'), 'шестдесет и седем')
        self.assertEqual(num2words(89, lang='bg'), 'осемдесет и девет')
        self.assertEqual(num2words(99, lang='bg'), 'деветдесет и девет')

    def test_cardinal_hundreds(self):
        """Test hundreds in Bulgarian."""
        self.assertEqual(num2words(100, lang='bg'), 'сто')
        self.assertEqual(num2words(200, lang='bg'), 'двеста')
        self.assertEqual(num2words(300, lang='bg'), 'триста')
        self.assertEqual(num2words(400, lang='bg'), 'четиристотин')
        self.assertEqual(num2words(500, lang='bg'), 'петстотин')
        self.assertEqual(num2words(600, lang='bg'), 'шестстотин')
        self.assertEqual(num2words(700, lang='bg'), 'седемстотин')
        self.assertEqual(num2words(800, lang='bg'), 'осемстотин')
        self.assertEqual(num2words(900, lang='bg'), 'деветстотин')

    def test_cardinal_complex_hundreds(self):
        """Test complex numbers with hundreds."""
        self.assertEqual(num2words(101, lang='bg'), 'сто един')
        self.assertEqual(num2words(111, lang='bg'), 'сто единадесет')
        self.assertEqual(num2words(212, lang='bg'), 'двеста дванадесет')
        self.assertEqual(num2words(345, lang='bg'), 'триста четиридесет и пет')
        self.assertEqual(num2words(567,
                         lang='bg'), 'петстотин шестдесет и седем')
        self.assertEqual(num2words(891,
                         lang='bg'), 'осемстотин деветдесет и един')
        self.assertEqual(
            num2words(999, lang='bg'), 'деветстотин деветдесет и девет')

    def test_cardinal_thousands(self):
        """Test thousands in Bulgarian."""
        self.assertEqual(num2words(1000, lang='bg'), 'хиляда')
        self.assertEqual(num2words(2000, lang='bg'), 'две хиляди')
        self.assertEqual(num2words(3000, lang='bg'), 'три хиляди')
        self.assertEqual(num2words(5000, lang='bg'), 'пет хиляди')
        self.assertEqual(num2words(10000, lang='bg'), 'десет хиляди')
        self.assertEqual(num2words(15000, lang='bg'), 'петнадесет хиляди')
        self.assertEqual(num2words(25000, lang='bg'), 'двадесет и пет хиляди')
        self.assertEqual(num2words(100000, lang='bg'), 'сто хиляди')
        self.assertEqual(
            num2words(999999, lang='bg'),
            'деветстотин деветдесет и девет хиляди '
            'деветстотин деветдесет и девет')

    def test_cardinal_millions(self):
        """Test millions in Bulgarian."""
        self.assertEqual(num2words(1000000, lang='bg'), 'един милион')
        self.assertEqual(num2words(2000000, lang='bg'), 'два милиона')
        self.assertEqual(num2words(5000000, lang='bg'), 'пет милиона')
        self.assertEqual(num2words(15000000, lang='bg'), 'петнадесет милиона')
        self.assertEqual(
            num2words(123456789, lang='bg'),
            'сто двадесет и три милиона '
            'четиристотин петдесет и шест хиляди '
            'седемстотин осемдесет и девет')

    def test_cardinal_billions(self):
        """Test billions in Bulgarian."""
        self.assertEqual(num2words(1000000000, lang='bg'), 'един милиард')
        self.assertEqual(num2words(2000000000, lang='bg'), 'два милиарда')
        self.assertEqual(num2words(5000000000, lang='bg'), 'пет милиарда')

    def test_negative_numbers(self):
        """Test negative numbers in Bulgarian."""
        self.assertEqual(num2words(-1, lang='bg'), 'минус един')
        self.assertEqual(num2words(-10, lang='bg'), 'минус десет')
        self.assertEqual(num2words(-25, lang='bg'), 'минус двадесет и пет')
        self.assertEqual(num2words(-100, lang='bg'), 'минус сто')
        self.assertEqual(num2words(-1000, lang='bg'), 'минус хиляда')

    def test_ordinal_basics(self):
        """Test basic ordinal numbers in Bulgarian."""
        self.assertEqual(num2words(1, lang='bg', to='ordinal'), 'първи')
        self.assertEqual(num2words(2, lang='bg', to='ordinal'), 'втори')
        self.assertEqual(num2words(3, lang='bg', to='ordinal'), 'трети')
        self.assertEqual(num2words(4, lang='bg', to='ordinal'), 'четвърти')
        self.assertEqual(num2words(5, lang='bg', to='ordinal'), 'пети')
        self.assertEqual(num2words(6, lang='bg', to='ordinal'), 'шести')
        self.assertEqual(num2words(7, lang='bg', to='ordinal'), 'седми')
        self.assertEqual(num2words(8, lang='bg', to='ordinal'), 'осми')
        self.assertEqual(num2words(9, lang='bg', to='ordinal'), 'девети')
        self.assertEqual(num2words(10, lang='bg', to='ordinal'), 'десети')

    def test_ordinal_tens(self):
        """Test ordinal tens in Bulgarian."""
        self.assertEqual(num2words(11, lang='bg', to='ordinal'), 'единадесети')
        self.assertEqual(num2words(12, lang='bg', to='ordinal'), 'дванадесети')
        self.assertEqual(num2words(20, lang='bg', to='ordinal'), 'двадесети')
        self.assertEqual(num2words(30, lang='bg', to='ordinal'), 'тридесети')
        self.assertEqual(num2words(50, lang='bg', to='ordinal'), 'петдесети')
        self.assertEqual(num2words(100, lang='bg', to='ordinal'), 'стотен')
        self.assertEqual(num2words(1000, lang='bg', to='ordinal'), 'хиляден')

    def test_ordinal_num(self):
        """Test ordinal number formatting in Bulgarian."""
        self.assertEqual(num2words(1, lang='bg', to='ordinal_num'), '1-ви')
        self.assertEqual(num2words(2, lang='bg', to='ordinal_num'), '2-ри')
        self.assertEqual(num2words(3, lang='bg', to='ordinal_num'), '3-ти')
        self.assertEqual(num2words(4, lang='bg', to='ordinal_num'), '4-ти')
        self.assertEqual(num2words(5, lang='bg', to='ordinal_num'), '5-ти')
        self.assertEqual(num2words(7, lang='bg', to='ordinal_num'), '7-ми')
        self.assertEqual(num2words(8, lang='bg', to='ordinal_num'), '8-ми')
        self.assertEqual(num2words(10, lang='bg', to='ordinal_num'), '10-ти')
        self.assertEqual(num2words(11, lang='bg', to='ordinal_num'), '11-ти')
        self.assertEqual(num2words(21, lang='bg', to='ordinal_num'), '21-ви')
        self.assertEqual(num2words(22, lang='bg', to='ordinal_num'), '22-ри')
        self.assertEqual(num2words(100, lang='bg', to='ordinal_num'), '100-ти')

    def test_currency(self):
        """Test currency in Bulgarian."""
        self.assertEqual(
            num2words(1, lang='bg', to='currency', currency='BGN'),
            'един лев'
        )
        self.assertEqual(
            num2words(2, lang='bg', to='currency', currency='BGN'),
            'два лева'
        )
        self.assertEqual(
            num2words(5.50, lang='bg', to='currency', currency='BGN'),
            'пет лева и петдесет стотинки'
        )
        self.assertEqual(
            num2words(10.01, lang='bg', to='currency', currency='BGN'),
            'десет лева и един стотинка'
        )
        self.assertEqual(
            num2words(100.25, lang='bg', to='currency', currency='BGN'),
            'сто лева и двадесет и пет стотинки'
        )
        self.assertEqual(
            num2words(1, lang='bg', to='currency', currency='EUR'),
            'един евро'
        )
        self.assertEqual(
            num2words(2.50, lang='bg', to='currency', currency='EUR'),
            'два евро и петдесет цента'
        )
        self.assertEqual(
            num2words(1, lang='bg', to='currency', currency='USD'),
            'един долар'
        )
        self.assertEqual(
            num2words(5.25, lang='bg', to='currency', currency='USD'),
            'пет долара и двадесет и пет цента'
        )

    def test_year(self):
        """Test year conversion in Bulgarian."""
        self.assertEqual(num2words(1900, lang='bg', to='year'),
                         'хиляда деветстотин')
        self.assertEqual(num2words(1999, lang='bg', to='year'),
                         'хиляда деветстотин деветдесет и девет')
        self.assertEqual(num2words(2000, lang='bg', to='year'),
                         'две хиляди')
        self.assertEqual(num2words(2001, lang='bg', to='year'),
                         'две хиляди един')
        self.assertEqual(num2words(2020, lang='bg', to='year'),
                         'две хиляди двадесет')
        self.assertEqual(num2words(2023, lang='bg', to='year'),
                         'две хиляди двадесет и три')
        self.assertEqual(num2words(2100, lang='bg', to='year'),
                         'две хиляди сто')
