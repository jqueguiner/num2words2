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


class Num2WordsSNTest(TestCase):

    def test_cardinal_numbers(self):
        """Test cardinal numbers 0-20 in Shona"""
        self.assertEqual(num2words(0, lang='sn'), 'zero')
        self.assertEqual(num2words(1, lang='sn'), 'motsi')
        self.assertEqual(num2words(2, lang='sn'), 'piri')
        self.assertEqual(num2words(3, lang='sn'), 'tatu')
        self.assertEqual(num2words(4, lang='sn'), 'china')
        self.assertEqual(num2words(5, lang='sn'), 'shanu')
        self.assertEqual(num2words(6, lang='sn'), 'tanhatu')
        self.assertEqual(num2words(7, lang='sn'), 'nomwe')
        self.assertEqual(num2words(8, lang='sn'), 'sere')
        self.assertEqual(num2words(9, lang='sn'), 'pfumbamwe')
        self.assertEqual(num2words(10, lang='sn'), 'gumi')
        self.assertEqual(num2words(11, lang='sn'), 'gumi nemotsi')
        self.assertEqual(num2words(12, lang='sn'), 'gumi nepiri')
        self.assertEqual(num2words(13, lang='sn'), 'gumi netatu')
        self.assertEqual(num2words(14, lang='sn'), 'gumi nechina')
        self.assertEqual(num2words(15, lang='sn'), 'gumi neshanu')
        self.assertEqual(num2words(16, lang='sn'), 'gumi netanhatu')
        self.assertEqual(num2words(17, lang='sn'), 'gumi nenomwe')
        self.assertEqual(num2words(18, lang='sn'), 'gumi nesere')
        self.assertEqual(num2words(19, lang='sn'), 'gumi nepfumbamwe')
        self.assertEqual(num2words(20, lang='sn'), 'makumi maviri')

    def test_tens(self):
        """Test tens (20, 30, 40, etc.) in Shona"""
        self.assertEqual(num2words(20, lang='sn'), 'makumi maviri')
        self.assertEqual(num2words(30, lang='sn'), 'makumi matatu')
        self.assertEqual(num2words(40, lang='sn'), 'makumi mana')
        self.assertEqual(num2words(50, lang='sn'), 'makumi mashanu')
        self.assertEqual(num2words(60, lang='sn'), 'makumi matanhatu')
        self.assertEqual(num2words(70, lang='sn'), 'makumi manomwe')
        self.assertEqual(num2words(80, lang='sn'), 'makumi masere')
        self.assertEqual(num2words(90, lang='sn'), 'makumi mapfumbamwe')

    def test_compound_numbers(self):
        """Test compound numbers (21-99) in Shona"""
        self.assertEqual(num2words(21, lang='sn'), 'makumi maviri nemotsi')
        self.assertEqual(num2words(25, lang='sn'), 'makumi maviri neshanu')
        self.assertEqual(num2words(35, lang='sn'), 'makumi matatu neshanu')
        self.assertEqual(num2words(47, lang='sn'), 'makumi mana nenomwe')
        self.assertEqual(num2words(59, lang='sn'), 'makumi mashanu nepfumbamwe')
        self.assertEqual(num2words(64, lang='sn'), 'makumi matanhatu nechina')
        self.assertEqual(num2words(78, lang='sn'), 'makumi manomwe nesere')
        self.assertEqual(num2words(82, lang='sn'), 'makumi masere nepiri')
        self.assertEqual(num2words(99, lang='sn'), 'makumi mapfumbamwe nepfumbamwe')

    def test_hundreds(self):
        """Test hundreds in Shona"""
        self.assertEqual(num2words(100, lang='sn'), 'zana')
        self.assertEqual(num2words(200, lang='sn'), 'mazana maviri')
        self.assertEqual(num2words(300, lang='sn'), 'mazana matatu')
        self.assertEqual(num2words(400, lang='sn'), 'mazana mana')
        self.assertEqual(num2words(500, lang='sn'), 'mazana mashanu')
        self.assertEqual(num2words(600, lang='sn'), 'mazana matanhatu')
        self.assertEqual(num2words(700, lang='sn'), 'mazana manomwe')
        self.assertEqual(num2words(800, lang='sn'), 'mazana masere')
        self.assertEqual(num2words(900, lang='sn'), 'mazana mapfumbamwe')

    def test_hundreds_with_tens_and_units(self):
        """Test hundreds with tens and units in Shona"""
        self.assertEqual(num2words(101, lang='sn'), 'zana nemotsi')
        self.assertEqual(num2words(111, lang='sn'), 'zana negumi nemotsi')
        self.assertEqual(num2words(125, lang='sn'), 'zana nemakumi maviri neshanu')
        self.assertEqual(num2words(235, lang='sn'), 'mazana maviri nemakumi matatu neshanu')
        self.assertEqual(num2words(345, lang='sn'), 'mazana matatu nemakumi mana neshanu')
        self.assertEqual(num2words(456, lang='sn'), 'mazana mana nemakumi mashanu netanhatu')
        self.assertEqual(num2words(567, lang='sn'), 'mazana mashanu nemakumi matanhatu nenomwe')
        self.assertEqual(num2words(678, lang='sn'), 'mazana matanhatu nemakumi manomwe nesere')
        self.assertEqual(num2words(789, lang='sn'), 'mazana manomwe nemakumi masere nepfumbamwe')
        self.assertEqual(num2words(999, lang='sn'), 'mazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe')

    def test_thousands(self):
        """Test thousands in Shona"""
        self.assertEqual(num2words(1000, lang='sn'), 'churu')
        self.assertEqual(num2words(2000, lang='sn'), 'zvuru zviviri')
        self.assertEqual(num2words(3000, lang='sn'), 'zvuru zvitatu')
        self.assertEqual(num2words(4000, lang='sn'), 'zvuru zvina')
        self.assertEqual(num2words(5000, lang='sn'), 'zvuru zvishanu')
        self.assertEqual(num2words(6000, lang='sn'), 'zvuru zvitanhatu')
        self.assertEqual(num2words(7000, lang='sn'), 'zvuru zvinomwe')
        self.assertEqual(num2words(8000, lang='sn'), 'zvuru zvisere')
        self.assertEqual(num2words(9000, lang='sn'), 'zvuru zvipfumbamwe')
        self.assertEqual(num2words(10000, lang='sn'), 'zvuru gumi')

    def test_thousands_complex(self):
        """Test complex thousand numbers in Shona"""
        self.assertEqual(num2words(1001, lang='sn'), 'churu nemotsi')
        self.assertEqual(num2words(1010, lang='sn'), 'churu negumi')
        self.assertEqual(num2words(1100, lang='sn'), 'churu nezana')
        self.assertEqual(num2words(1234, lang='sn'), 'churu nemazana maviri nemakumi matatu nechina')
        self.assertEqual(num2words(2345, lang='sn'), 'zvuru zviviri nemazana matatu nemakumi mana neshanu')
        self.assertEqual(num2words(5678, lang='sn'), 'zvuru zvishanu nemazana matanhatu nemakumi manomwe nesere')
        self.assertEqual(num2words(9999, lang='sn'), 'zvuru zvipfumbamwe nemazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe')
        self.assertEqual(num2words(10001, lang='sn'), 'zvuru gumi nemotsi')
        self.assertEqual(num2words(15000, lang='sn'), 'zvuru gumi neshanu')
        self.assertEqual(num2words(20000, lang='sn'), 'zvuru makumi maviri')
        self.assertEqual(num2words(25000, lang='sn'), 'zvuru makumi maviri neshanu')
        self.assertEqual(num2words(99999, lang='sn'), 'zvuru makumi mapfumbamwe nepfumbamwe nemazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe')

    def test_hundred_thousands(self):
        """Test hundred thousands in Shona"""
        self.assertEqual(num2words(100000, lang='sn'), 'zvuru zana')
        self.assertEqual(num2words(200000, lang='sn'), 'zvuru mazana maviri')
        self.assertEqual(num2words(500000, lang='sn'), 'zvuru mazana mashanu')
        self.assertEqual(num2words(999999, lang='sn'), 'zvuru mazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe nemazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe')

    def test_millions(self):
        """Test millions in Shona"""
        self.assertEqual(num2words(1000000, lang='sn'), 'miriyoni')
        self.assertEqual(num2words(2000000, lang='sn'), 'miriyoni mbiri')
        self.assertEqual(num2words(5000000, lang='sn'), 'miriyoni shanu')
        self.assertEqual(num2words(1000001, lang='sn'), 'miriyoni nemotsi')
        self.assertEqual(num2words(1234567, lang='sn'), 'miriyoni nezvuru mazana maviri nemakumi matatu nechina nemazana mashanu nemakumi matanhatu nenomwe')
        self.assertEqual(num2words(9999999, lang='sn'), 'miriyoni pfumbamwe nezvuru mazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe nemazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe')

    def test_negative_numbers(self):
        """Test negative numbers in Shona"""
        self.assertEqual(num2words(-1, lang='sn'), 'minus motsi')
        self.assertEqual(num2words(-5, lang='sn'), 'minus shanu')
        self.assertEqual(num2words(-10, lang='sn'), 'minus gumi')
        self.assertEqual(num2words(-15, lang='sn'), 'minus gumi neshanu')
        self.assertEqual(num2words(-20, lang='sn'), 'minus makumi maviri')
        self.assertEqual(num2words(-100, lang='sn'), 'minus zana')
        self.assertEqual(num2words(-234, lang='sn'), 'minus mazana maviri nemakumi matatu nechina')
        self.assertEqual(num2words(-1000, lang='sn'), 'minus churu')
        self.assertEqual(num2words(-999999, lang='sn'), 'minus zvuru mazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe nemazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe')

    def test_decimal_numbers(self):
        """Test decimal numbers in Shona"""
        self.assertEqual(num2words(0.5, lang='sn'), 'zero poindi shanu')
        self.assertEqual(num2words(0.7, lang='sn'), 'zero poindi nomwe')
        self.assertEqual(num2words(1.5, lang='sn'), 'motsi poindi shanu')
        self.assertEqual(num2words(2.3, lang='sn'), 'piri poindi tatu')
        self.assertEqual(num2words(5.75, lang='sn'), 'shanu poindi nomwe shanu')
        self.assertEqual(num2words(10.5, lang='sn'), 'gumi poindi shanu')
        self.assertEqual(num2words(15.25, lang='sn'), 'gumi neshanu poindi piri shanu')
        self.assertEqual(num2words(100.01, lang='sn'), 'zana poindi zero motsi')
        self.assertEqual(num2words(999.99, lang='sn'), 'mazana mapfumbamwe nemakumi mapfumbamwe nepfumbamwe poindi pfumbamwe pfumbamwe')

    def test_negative_decimals(self):
        """Test negative decimal numbers in Shona"""
        self.assertEqual(num2words(-0.4, lang='sn'), 'minus zero poindi china')
        self.assertEqual(num2words(-0.5, lang='sn'), 'minus zero poindi shanu')
        self.assertEqual(num2words(-1.4, lang='sn'), 'minus motsi poindi china')
        self.assertEqual(num2words(-10.25, lang='sn'), 'minus gumi poindi piri shanu')
        self.assertEqual(num2words(-100.5, lang='sn'), 'minus zana poindi shanu')

    def test_ordinal_numbers(self):
        """Test ordinal numbers in Shona"""
        self.assertEqual(num2words(1, lang='sn', to='ordinal'), 'wekutanga')
        self.assertEqual(num2words(2, lang='sn', to='ordinal'), 'wechipiri')
        self.assertEqual(num2words(3, lang='sn', to='ordinal'), 'wechitatu')
        self.assertEqual(num2words(4, lang='sn', to='ordinal'), 'wechina')
        self.assertEqual(num2words(5, lang='sn', to='ordinal'), 'wechishanu')
        self.assertEqual(num2words(6, lang='sn', to='ordinal'), 'wechitanhatu')
        self.assertEqual(num2words(7, lang='sn', to='ordinal'), 'wechinomwe')
        self.assertEqual(num2words(8, lang='sn', to='ordinal'), 'wechisere')
        self.assertEqual(num2words(9, lang='sn', to='ordinal'), 'wechipfumbamwe')
        self.assertEqual(num2words(10, lang='sn', to='ordinal'), 'wegumi')
        self.assertEqual(num2words(11, lang='sn', to='ordinal'), 'wegumi nemotsi')
        self.assertEqual(num2words(20, lang='sn', to='ordinal'), 'wemakumi maviri')
        self.assertEqual(num2words(21, lang='sn', to='ordinal'), 'wemakumi maviri nemotsi')
        self.assertEqual(num2words(100, lang='sn', to='ordinal'), 'wezana')
        self.assertEqual(num2words(1000, lang='sn', to='ordinal'), 'wechuru')

    def test_currency(self):
        """Test currency conversion in Shona"""
        self.assertEqual(
            num2words(1, lang='sn', to='currency', currency='USD'),
            'dhora rimwe'
        )
        self.assertEqual(
            num2words(2, lang='sn', to='currency', currency='USD'),
            'madhora maviri'
        )
        self.assertEqual(
            num2words(5.50, lang='sn', to='currency', currency='USD'),
            'madhora mashanu nesendi makumi mashanu'
        )
        self.assertEqual(
            num2words(100, lang='sn', to='currency', currency='USD'),
            'madhora zana'
        )
        self.assertEqual(
            num2words(1234.56, lang='sn', to='currency', currency='USD'),
            'madhora churu nemazana maviri nemakumi matatu nechina nesendi makumi mashanu netanhatu'
        )

    def test_year(self):
        """Test year conversion in Shona"""
        self.assertEqual(num2words(1990, lang='sn', to='year'), 'churu nemazana mapfumbamwe nemakumi mapfumbamwe')
        self.assertEqual(num2words(2000, lang='sn', to='year'), 'zvuru zviviri')
        self.assertEqual(num2words(2024, lang='sn', to='year'), 'zvuru zviviri nemakumi maviri nechina')
        self.assertEqual(num2words(1066, lang='sn', to='year'), 'churu nemakumi matanhatu netanhatu')
        self.assertEqual(num2words(1865, lang='sn', to='year'), 'churu nemazana masere nemakumi matanhatu neshanu')

    def test_large_numbers(self):
        """Test large numbers beyond millions in Shona"""
        self.assertEqual(num2words(1000000000, lang='sn'), 'bhiriyoni')
        self.assertEqual(num2words(2000000000, lang='sn'), 'bhiriyoni mbiri')
        self.assertEqual(num2words(1000000000000, lang='sn'), 'tiriyoni')
        self.assertEqual(num2words(2000000000000, lang='sn'), 'tiriyoni mbiri')
