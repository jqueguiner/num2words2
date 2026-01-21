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


class Num2WordsETTest(TestCase):
    def test_cardinal_basics(self):
        """Test basic cardinal numbers in Estonian."""
        self.assertEqual(num2words(0, lang='et'), 'null')
        self.assertEqual(num2words(1, lang='et'), 'üks')
        self.assertEqual(num2words(2, lang='et'), 'kaks')
        self.assertEqual(num2words(3, lang='et'), 'kolm')
        self.assertEqual(num2words(4, lang='et'), 'neli')
        self.assertEqual(num2words(5, lang='et'), 'viis')
        self.assertEqual(num2words(6, lang='et'), 'kuus')
        self.assertEqual(num2words(7, lang='et'), 'seitse')
        self.assertEqual(num2words(8, lang='et'), 'kaheksa')
        self.assertEqual(num2words(9, lang='et'), 'üheksa')

    def test_cardinal_tens(self):
        """Test tens in Estonian."""
        self.assertEqual(num2words(10, lang='et'), 'kümme')
        self.assertEqual(num2words(11, lang='et'), 'üksteist')
        self.assertEqual(num2words(12, lang='et'), 'kaksteist')
        self.assertEqual(num2words(13, lang='et'), 'kolmteist')
        self.assertEqual(num2words(14, lang='et'), 'neliteist')
        self.assertEqual(num2words(15, lang='et'), 'viisteist')
        self.assertEqual(num2words(16, lang='et'), 'kuusteist')
        self.assertEqual(num2words(17, lang='et'), 'seitseteist')
        self.assertEqual(num2words(18, lang='et'), 'kaheksateist')
        self.assertEqual(num2words(19, lang='et'), 'üheksateist')
        self.assertEqual(num2words(20, lang='et'), 'kakskümmend')
        self.assertEqual(num2words(30, lang='et'), 'kolmkümmend')
        self.assertEqual(num2words(40, lang='et'), 'nelikümmend')
        self.assertEqual(num2words(50, lang='et'), 'viiskümmend')
        self.assertEqual(num2words(60, lang='et'), 'kuuskümmend')
        self.assertEqual(num2words(70, lang='et'), 'seitsekümmend')
        self.assertEqual(num2words(80, lang='et'), 'kaheksakümmend')
        self.assertEqual(num2words(90, lang='et'), 'üheksakümmend')

    def test_cardinal_compound_tens(self):
        """Test compound numbers with tens."""
        self.assertEqual(num2words(21, lang='et'), 'kakskümmend üks')
        self.assertEqual(num2words(32, lang='et'), 'kolmkümmend kaks')
        self.assertEqual(num2words(45, lang='et'), 'nelikümmend viis')
        self.assertEqual(num2words(67, lang='et'), 'kuuskümmend seitse')
        self.assertEqual(num2words(89, lang='et'), 'kaheksakümmend üheksa')
        self.assertEqual(num2words(99, lang='et'), 'üheksakümmend üheksa')

    def test_cardinal_hundreds(self):
        """Test hundreds in Estonian."""
        self.assertEqual(num2words(100, lang='et'), 'ükssada')
        self.assertEqual(num2words(200, lang='et'), 'kakssada')
        self.assertEqual(num2words(300, lang='et'), 'kolmsada')
        self.assertEqual(num2words(400, lang='et'), 'nelisada')
        self.assertEqual(num2words(500, lang='et'), 'viissada')
        self.assertEqual(num2words(600, lang='et'), 'kuussada')
        self.assertEqual(num2words(700, lang='et'), 'seitsesada')
        self.assertEqual(num2words(800, lang='et'), 'kaheksasada')
        self.assertEqual(num2words(900, lang='et'), 'üheksasada')

    def test_cardinal_complex_hundreds(self):
        """Test complex numbers with hundreds."""
        self.assertEqual(num2words(101, lang='et'), 'ükssada üks')
        self.assertEqual(num2words(111, lang='et'), 'ükssada üksteist')
        self.assertEqual(num2words(212, lang='et'), 'kakssada kaksteist')
        self.assertEqual(num2words(345,
                         lang='et'), 'kolmsada nelikümmend viis')
        self.assertEqual(num2words(567,
                         lang='et'), 'viissada kuuskümmend seitse')
        self.assertEqual(num2words(891,
                         lang='et'), 'kaheksasada üheksakümmend üks')
        self.assertEqual(
            num2words(999, lang='et'), 'üheksasada üheksakümmend üheksa')

    def test_cardinal_thousands(self):
        """Test thousands in Estonian."""
        self.assertEqual(num2words(1000, lang='et'), 'tuhat')
        self.assertEqual(num2words(2000, lang='et'), 'kaks tuhat')
        self.assertEqual(num2words(3000, lang='et'), 'kolm tuhat')
        self.assertEqual(num2words(5000, lang='et'), 'viis tuhat')
        self.assertEqual(num2words(10000, lang='et'), 'kümme tuhat')
        self.assertEqual(num2words(15000, lang='et'), 'viisteist tuhat')
        self.assertEqual(num2words(25000, lang='et'), 'kakskümmend viis tuhat')
        self.assertEqual(num2words(100000, lang='et'), 'sada tuhat')
        self.assertEqual(num2words(999999, lang='et'),
                         'üheksasada üheksakümmend üheksa tuhat '
                         'üheksasada üheksakümmend üheksa')

    def test_cardinal_millions(self):
        """Test millions in Estonian."""
        self.assertEqual(num2words(1000000, lang='et'), 'üks miljon')
        self.assertEqual(num2words(2000000, lang='et'), 'kaks miljonit')
        self.assertEqual(num2words(5000000, lang='et'), 'viis miljonit')
        self.assertEqual(num2words(15000000, lang='et'), 'viisteist miljonit')
        self.assertEqual(num2words(123456789, lang='et'),
                         'ükssada kakskümmend kolm miljonit '
                         'nelisada viiskümmend kuus tuhat '
                         'seitsesada kaheksakümmend üheksa')

    def test_cardinal_billions(self):
        """Test billions in Estonian."""
        self.assertEqual(num2words(1000000000, lang='et'), 'üks miljard')
        self.assertEqual(num2words(2000000000, lang='et'), 'kaks miljardit')
        self.assertEqual(num2words(5000000000, lang='et'), 'viis miljardit')

    def test_negative_numbers(self):
        """Test negative numbers in Estonian."""
        self.assertEqual(num2words(-1, lang='et'), 'miinus üks')
        self.assertEqual(num2words(-10, lang='et'), 'miinus kümme')
        self.assertEqual(num2words(-25, lang='et'), 'miinus kakskümmend viis')
        self.assertEqual(num2words(-100, lang='et'), 'miinus ükssada')
        self.assertEqual(num2words(-1000, lang='et'), 'miinus tuhat')

    def test_ordinal_basics(self):
        """Test basic ordinal numbers in Estonian."""
        self.assertEqual(num2words(1, lang='et', to='ordinal'), 'esimene')
        self.assertEqual(num2words(2, lang='et', to='ordinal'), 'teine')
        self.assertEqual(num2words(3, lang='et', to='ordinal'), 'kolmas')
        self.assertEqual(num2words(4, lang='et', to='ordinal'), 'neljas')
        self.assertEqual(num2words(5, lang='et', to='ordinal'), 'viies')
        self.assertEqual(num2words(6, lang='et', to='ordinal'), 'kuues')
        self.assertEqual(num2words(7, lang='et', to='ordinal'), 'seitsmes')
        self.assertEqual(num2words(8, lang='et', to='ordinal'), 'kaheksas')
        self.assertEqual(num2words(9, lang='et', to='ordinal'), 'üheksas')
        self.assertEqual(num2words(10, lang='et', to='ordinal'), 'kümnes')

    def test_ordinal_tens(self):
        """Test ordinal tens in Estonian."""
        self.assertEqual(num2words(11,
                         lang='et', to='ordinal'), 'üheteistkümnes')
        self.assertEqual(num2words(12,
                         lang='et', to='ordinal'), 'kaheteistkümnes')
        self.assertEqual(num2words(20, lang='et', to='ordinal'), 'kahekümnes')
        self.assertEqual(num2words(30, lang='et', to='ordinal'), 'kolmekümnes')
        self.assertEqual(num2words(50, lang='et', to='ordinal'), 'viiekümnes')
        self.assertEqual(num2words(100, lang='et', to='ordinal'), 'sajas')
        self.assertEqual(num2words(1000, lang='et', to='ordinal'), 'tuhandes')

    def test_ordinal_num(self):
        """Test ordinal number formatting in Estonian."""
        self.assertEqual(num2words(1, lang='et', to='ordinal_num'), '1.')
        self.assertEqual(num2words(2, lang='et', to='ordinal_num'), '2.')
        self.assertEqual(num2words(3, lang='et', to='ordinal_num'), '3.')
        self.assertEqual(num2words(10, lang='et', to='ordinal_num'), '10.')
        self.assertEqual(num2words(21, lang='et', to='ordinal_num'), '21.')
        self.assertEqual(num2words(100, lang='et', to='ordinal_num'), '100.')

    def test_currency(self):
        """Test currency in Estonian."""
        self.assertEqual(
            num2words(1, lang='et', to='currency', currency='EUR'),
            'üks euro'
        )
        self.assertEqual(
            num2words(2, lang='et', to='currency', currency='EUR'),
            'kaks eurot'
        )
        self.assertEqual(
            num2words(5.50, lang='et', to='currency', currency='EUR'),
            'viis eurot ja viiskümmend senti'
        )
        self.assertEqual(
            num2words(10.01, lang='et', to='currency', currency='EUR'),
            'kümme eurot ja üks sent'
        )
        self.assertEqual(
            num2words(100.25, lang='et', to='currency', currency='EUR'),
            'ükssada eurot ja kakskümmend viis senti'
        )
        self.assertEqual(
            num2words(1, lang='et', to='currency', currency='USD'),
            'üks dollar'
        )
        self.assertEqual(
            num2words(5.25, lang='et', to='currency', currency='USD'),
            'viis dollarit ja kakskümmend viis senti'
        )

    def test_year(self):
        """Test year conversion in Estonian."""
        self.assertEqual(num2words(1900, lang='et', to='year'),
                         'tuhat üheksasada')
        self.assertEqual(num2words(1999, lang='et', to='year'),
                         'tuhat üheksasada üheksakümmend üheksa')
        self.assertEqual(num2words(2000, lang='et', to='year'),
                         'kaks tuhat')
        self.assertEqual(num2words(2001, lang='et', to='year'),
                         'kaks tuhat üks')
        self.assertEqual(num2words(2020, lang='et', to='year'),
                         'kaks tuhat kakskümmend')
        self.assertEqual(num2words(2023, lang='et', to='year'),
                         'kaks tuhat kakskümmend kolm')
