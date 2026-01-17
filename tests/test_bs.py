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


class Num2WordsBSTest(TestCase):

    def test_basic_numbers(self):
        # Test 0-9
        self.assertEqual("nula", num2words(0, lang='bs'))
        self.assertEqual("jedan", num2words(1, lang='bs'))
        self.assertEqual("dva", num2words(2, lang='bs'))
        self.assertEqual("tri", num2words(3, lang='bs'))
        self.assertEqual("četiri", num2words(4, lang='bs'))
        self.assertEqual("pet", num2words(5, lang='bs'))
        self.assertEqual("šest", num2words(6, lang='bs'))
        self.assertEqual("sedam", num2words(7, lang='bs'))
        self.assertEqual("osam", num2words(8, lang='bs'))
        self.assertEqual("devet", num2words(9, lang='bs'))

    def test_ten_and_teens(self):
        # Test 10-19
        self.assertEqual("deset", num2words(10, lang='bs'))
        self.assertEqual("jedanaest", num2words(11, lang='bs'))
        self.assertEqual("dvanaest", num2words(12, lang='bs'))
        self.assertEqual("trinaest", num2words(13, lang='bs'))
        self.assertEqual("četrnaest", num2words(14, lang='bs'))
        self.assertEqual("petnaest", num2words(15, lang='bs'))
        self.assertEqual("šesnaest", num2words(16, lang='bs'))
        self.assertEqual("sedamnaest", num2words(17, lang='bs'))
        self.assertEqual("osamnaest", num2words(18, lang='bs'))
        self.assertEqual("devetnaest", num2words(19, lang='bs'))

    def test_tens(self):
        # Test 20, 30, 40, etc.
        self.assertEqual("dvadeset", num2words(20, lang='bs'))
        self.assertEqual("trideset", num2words(30, lang='bs'))
        self.assertEqual("četrdeset", num2words(40, lang='bs'))
        self.assertEqual("pedeset", num2words(50, lang='bs'))
        self.assertEqual("šezdeset", num2words(60, lang='bs'))
        self.assertEqual("sedamdeset", num2words(70, lang='bs'))
        self.assertEqual("osamdeset", num2words(80, lang='bs'))
        self.assertEqual("devedeset", num2words(90, lang='bs'))

    def test_compound_numbers(self):
        # Test compound numbers like 21, 35, 47, etc.
        self.assertEqual("dvadeset jedan", num2words(21, lang='bs'))
        self.assertEqual("trideset pet", num2words(35, lang='bs'))
        self.assertEqual("četrdeset sedam", num2words(47, lang='bs'))
        self.assertEqual("pedeset devet", num2words(59, lang='bs'))
        self.assertEqual("šezdeset tri", num2words(63, lang='bs'))
        self.assertEqual("sedamdeset osam", num2words(78, lang='bs'))
        self.assertEqual("osamdeset četiri", num2words(84, lang='bs'))
        self.assertEqual("devedeset šest", num2words(96, lang='bs'))

    def test_hundreds(self):
        # Test hundreds
        self.assertEqual("sto", num2words(100, lang='bs'))
        self.assertEqual("dvjesta", num2words(200, lang='bs'))
        self.assertEqual("trista", num2words(300, lang='bs'))
        self.assertEqual("četiristo", num2words(400, lang='bs'))
        self.assertEqual("petsto", num2words(500, lang='bs'))
        self.assertEqual("šesto", num2words(600, lang='bs'))
        self.assertEqual("sedamsto", num2words(700, lang='bs'))
        self.assertEqual("osamsto", num2words(800, lang='bs'))
        self.assertEqual("devetsto", num2words(900, lang='bs'))

    def test_hundreds_with_units(self):
        # Test hundreds with additional units
        self.assertEqual("sto jedan", num2words(101, lang='bs'))
        self.assertEqual("sto deset", num2words(110, lang='bs'))
        self.assertEqual("sto petnaest", num2words(115, lang='bs'))
        self.assertEqual("sto dvadeset tri", num2words(123, lang='bs'))
        self.assertEqual("sto pedeset četiri", num2words(154, lang='bs'))
        self.assertEqual("dvjesta petnaest", num2words(215, lang='bs'))
        self.assertEqual("trista četrdeset šest", num2words(346, lang='bs'))

    def test_thousands(self):
        # Test thousands
        self.assertEqual("jedna hiljada", num2words(1000, lang='bs'))
        self.assertEqual("dvije hiljade", num2words(2000, lang='bs'))
        self.assertEqual("tri hiljade", num2words(3000, lang='bs'))
        self.assertEqual("četiri hiljade", num2words(4000, lang='bs'))
        self.assertEqual("pet hiljada", num2words(5000, lang='bs'))

    def test_thousands_with_units(self):
        # Test thousands with additional units
        self.assertEqual("jedna hiljada jedan", num2words(1001, lang='bs'))
        self.assertEqual("jedna hiljada sto trideset pet", num2words(1135, lang='bs'))
        self.assertEqual("dvije hiljade dvanaest", num2words(2012, lang='bs'))
        self.assertEqual(
            "četiristo osamnaest hiljada petsto trideset jedan",
            num2words(418531, lang='bs')
        )

    def test_millions(self):
        # Test millions
        self.assertEqual("jedan milion", num2words(1000000, lang='bs'))
        self.assertEqual("dva miliona", num2words(2000000, lang='bs'))
        self.assertEqual("pet miliona", num2words(5000000, lang='bs'))
        self.assertEqual(
            "jedan milion sto trideset devet",
            num2words(1000139, lang='bs')
        )

    def test_large_numbers(self):
        # Test very large numbers
        self.assertEqual(
            "jedan bilion dvjesta trideset četiri miliona petsto "
            "šezdeset sedam hiljada osamsto devedeset",
            num2words(1234567890, lang='bs')
        )
        
        self.assertEqual(
            "dvanaest hiljada petsto devetnaest",
            num2words(12519, lang='bs')
        )

    def test_floating_point(self):
        # Test decimal numbers
        self.assertEqual("pet zapeta dva", num2words(5.2, lang='bs'))
        self.assertEqual(
            "deset zapeta nula dva",
            num2words(10.02, lang='bs')
        )
        self.assertEqual(
            "petnaest zapeta nula nula sedam",
            num2words(15.007, lang='bs')
        )
        self.assertEqual(
            "petsto šezdeset jedan zapeta četrdeset dva",
            num2words(561.42, lang='bs')
        )
        self.assertEqual(
            "dvanaest hiljada petsto devetnaest zapeta osamdeset pet",
            num2words(12519.85, lang='bs')
        )

    def test_negative_numbers(self):
        # Test negative numbers
        self.assertEqual("minus jedan", num2words(-1, lang='bs'))
        self.assertEqual("minus pet", num2words(-5, lang='bs'))
        self.assertEqual("minus dvadeset tri", num2words(-23, lang='bs'))
        self.assertEqual("minus sto", num2words(-100, lang='bs'))
        self.assertEqual("minus jedna hiljada", num2words(-1000, lang='bs'))

    def test_negative_decimals(self):
        # Test negative decimal numbers
        self.assertEqual("minus nula zapeta četiri", num2words(-0.4, lang='bs'))
        self.assertEqual("minus nula zapeta pet", num2words(-0.5, lang='bs'))
        self.assertEqual("minus jedan zapeta četiri", num2words(-1.4, lang='bs'))
        self.assertEqual("minus deset zapeta pet", num2words(-10.5, lang='bs'))

    def test_zero_variations(self):
        # Test zero in different contexts
        self.assertEqual("nula", num2words(0, lang='bs'))
        self.assertEqual("nula zapeta nula nula", num2words(0.0, lang='bs'))

    def test_to_ordinal(self):
        # Test that ordinals are not implemented yet
        with self.assertRaises(NotImplementedError):
            num2words(1, lang='bs', to='ordinal')

    def test_to_currency(self):
        # Test currency conversion for EUR
        self.assertEqual(
            'jedan euro, nula centi',
            num2words(1.0, lang='bs', to='currency', currency='EUR')
        )
        self.assertEqual(
            'dva eura, nula centi',
            num2words(2.0, lang='bs', to='currency', currency='EUR')
        )
        self.assertEqual(
            'pet eura, nula centi',
            num2words(5.0, lang='bs', to='currency', currency='EUR')
        )
        self.assertEqual(
            'dva eura, jedan cent',
            num2words(2.01, lang='bs', to='currency', currency='EUR')
        )
        self.assertEqual(
            'dva eura, dva centa',
            num2words(2.02, lang='bs', to='currency', currency='EUR')
        )
        self.assertEqual(
            'dva eura, pet centi',
            num2words(2.05, lang='bs', to='currency', currency='EUR')
        )

        # Test currency conversion for BAM (Bosnian Mark)
        self.assertEqual(
            'jedna marka, nula feninga',
            num2words(1.0, lang='bs', to='currency', currency='BAM')
        )
        self.assertEqual(
            'dvije marke, nula feninga',
            num2words(2.0, lang='bs', to='currency', currency='BAM')
        )
        self.assertEqual(
            'pet maraka, nula feninga',
            num2words(5.0, lang='bs', to='currency', currency='BAM')
        )
        self.assertEqual(
            'dvije marke, jedan fening',
            num2words(2.01, lang='bs', to='currency', currency='BAM')
        )
        self.assertEqual(
            'dvije marke, dva feninga',
            num2words(2.02, lang='bs', to='currency', currency='BAM')
        )
        self.assertEqual(
            'dvije marke, pet feninga',
            num2words(2.05, lang='bs', to='currency', currency='BAM')
        )
        
        # Test larger amounts
        self.assertEqual(
            'jedna hiljada dvjesta trideset četiri eura, '
            'pedeset šest centi',
            num2words(
                1234.56, lang='bs', to='currency', currency='EUR'
            )
        )
        
        # Test with separator
        self.assertEqual(
            'sto jedan euro i jedanaest centi',
            num2words(
                10111,
                lang='bs',
                to='currency',
                currency='EUR',
                separator=' i'
            )
        )
        
        # Test negative currency
        self.assertEqual(
            'minus dvanaest hiljada petsto devetnaest eura, 85 centi',
            num2words(
                -1251985,
                lang='bs',
                to='currency',
                currency='EUR',
                cents=False
            )
        )

    def test_edge_cases(self):
        # Test edge cases and specific number combinations
        self.assertEqual("jedanaest", num2words(11, lang='bs'))
        self.assertEqual("dvanaest", num2words(12, lang='bs'))
        self.assertEqual("dvadeset", num2words(20, lang='bs'))
        self.assertEqual("dvadeset jedan", num2words(21, lang='bs'))
        self.assertEqual("sto", num2words(100, lang='bs'))
        self.assertEqual("sto jedan", num2words(101, lang='bs'))
        self.assertEqual("jedna hiljada", num2words(1000, lang='bs'))
        self.assertEqual("deset hiljada", num2words(10000, lang='bs'))
        self.assertEqual("sto hiljada", num2words(100000, lang='bs'))
        self.assertEqual("jedan milion", num2words(1000000, lang='bs'))

    def test_gender_agreement(self):
        # Test feminine forms where applicable
        # For thousands (hiljada is feminine)
        self.assertEqual("jedna hiljada", num2words(1000, lang='bs'))
        self.assertEqual("dvije hiljade", num2words(2000, lang='bs'))
        self.assertEqual("tri hiljade", num2words(3000, lang='bs'))
        self.assertEqual("četiri hiljade", num2words(4000, lang='bs'))