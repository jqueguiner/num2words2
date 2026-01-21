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


class Num2WordsARTest(TestCase):

    def test_default_currency(self):
        self.assertEqual(num2words(1, to='currency', lang='ar'), 'واحد ريال')
        self.assertEqual(num2words(2, to='currency', lang='ar'),
                         'اثنان ريالان')
        self.assertEqual(num2words(10, to='currency', lang='ar'),
                         'عشرة ريالات')
        self.assertEqual(num2words(100, to='currency', lang='ar'), 'مائة ريال')
        self.assertEqual(num2words(652.12, to='currency', lang='ar'),
                         'ستمائة واثنان وخمسون ريالاً واثنتا عشرة هللة')
        self.assertEqual(num2words(324, to='currency', lang='ar'),
                         'ثلاثمائة وأربعة وعشرون ريالاً')
        self.assertEqual(num2words(2000, to='currency', lang='ar'),
                         'ألفا ريال')
        self.assertEqual(num2words(541, to='currency', lang='ar'),
                         'خمسمائة وواحد وأربعون ريالاً')
        self.assertEqual(num2words(10000, to='currency', lang='ar'),
                         'عشرة آلاف ريال')
        self.assertEqual(num2words(20000.12, to='currency', lang='ar'),
                         'عشرون ألف ريال واثنتا عشرة هللة')
        self.assertEqual(num2words(1000000, to='currency', lang='ar'),
                         'مليون ريال')
        val = 'تسعمائة وثلاثة وعشرون ألفاً وأربعمائة وأحد عشر ريالاً'
        self.assertEqual(num2words(923411, to='currency', lang='ar'), val)
        self.assertEqual(num2words(63411, to='currency', lang='ar'),
                         'ثلاثة وستون ألفاً وأربعمائة وأحد عشر ريالاً')
        self.assertEqual(num2words(1000000.99, to='currency', lang='ar'),
                         'مليون ريال وتسع وتسعون هللة')

    def test_currency_parm(self):
        self.assertEqual(
            num2words(1, to='currency', lang='ar', currency="KWD"),
            'واحد دينار')
        self.assertEqual(
            num2words(10, to='currency', lang='ar', currency="EGP"),
            'عشرة جنيهات')
        self.assertEqual(
            num2words(20000.12, to='currency', lang='ar', currency="EGP"),
            'عشرون ألف جنيه واثنتا عشرة قرش')
        self.assertEqual(
            num2words(923411, to='currency', lang='ar', currency="SR"),
            'تسعمائة وثلاثة وعشرون ألفاً وأربعمائة وأحد عشر ريالاً')
        self.assertEqual(
            num2words(1000000.99, to='currency', lang='ar', currency="KWD"),
            'مليون دينار وتسع وتسعون فلس')
        self.assertEqual(
            num2words(1000.42, to='currency', lang='ar', currency="TND"),
            'ألف دينار وأربعمائة وعشرون مليم')
        self.assertEqual(
            num2words(123.21, to='currency', lang='ar', currency="TND"),
            'مائة وثلاثة وعشرون ديناراً ومئتان وعشر مليمات')

    def test_ordinal(self):

        self.assertEqual(num2words(1, to='ordinal', lang='ar'), 'اول')
        self.assertEqual(num2words(2, to='ordinal', lang='ar'), 'ثاني')
        self.assertEqual(num2words(3, to='ordinal', lang='ar'), 'ثالث')
        self.assertEqual(num2words(4, to='ordinal', lang='ar'), 'رابع')
        self.assertEqual(num2words(5, to='ordinal', lang='ar'), 'خامس')
        self.assertEqual(num2words(6, to='ordinal', lang='ar'), 'سادس')
        self.assertEqual(num2words(9, to='ordinal', lang='ar'), 'تاسع')
        self.assertEqual(num2words(20, to='ordinal', lang='ar'), 'عشرون')
        self.assertEqual(num2words(94, to='ordinal', lang='ar'),
                         'أربع وتسعون')
        self.assertEqual(num2words(102, to='ordinal', lang='ar'),
                         'مائة واثنان')
        self.assertEqual(
            num2words(923411, to='ordinal_num', lang='ar'),
            'تسعمائة وثلاثة وعشرون ألفاً وأربعمائة وأحد عشر')

        # See https://github.com/savoirfairelinux/num2words/issues/403
        self.assertEqual(num2words(23, lang="ar"), 'ثلاثة وعشرون')
        self.assertEqual(num2words(23, to='ordinal',
                         lang="ar"), 'ثلاث وعشرون')
        self.assertEqual(num2words(23, lang="ar"), 'ثلاثة وعشرون')

    def test_cardinal(self):
        self.assertEqual(num2words(0, to='cardinal', lang='ar'), 'صفر')
        self.assertEqual(num2words(12, to='cardinal', lang='ar'), 'اثنا عشر')
        self.assertEqual(num2words(12.3, to='cardinal', lang='ar'),
                         'اثنا عشر  , ثلاثون')
        self.assertEqual(num2words(12.01, to='cardinal', lang='ar'),
                         'اثنا عشر  , إحدى')
        self.assertEqual(num2words(12.02, to='cardinal', lang='ar'),
                         'اثنا عشر  , اثنتان')
        self.assertEqual(num2words(12.03, to='cardinal', lang='ar'),
                         'اثنا عشر  , ثلاث')
        self.assertEqual(num2words(12.34, to='cardinal', lang='ar'),
                         'اثنا عشر  , أربع وثلاثون')
        # Not implemented
        self.assertEqual(num2words(12.345, to='cardinal', lang='ar'),
                         num2words(12.34, to='cardinal', lang='ar'))
        self.assertEqual(num2words(-8324, to='cardinal', lang='ar'),
                         'سالب ثمانية آلاف وثلاثمائة وأربعة وعشرون')

        self.assertEqual(num2words(200, to='cardinal', lang='ar'),
                         'مئتا')
        self.assertEqual(num2words(700, to='cardinal', lang='ar'),
                         'سبعمائة')
        self.assertEqual(num2words(101010, to='cardinal', lang='ar'),
                         'مائة وألف ألف وعشرة')

        self.assertEqual(
            num2words(3431.12, to='cardinal', lang='ar'),
            'ثلاثة آلاف وأربعمائة وواحد وثلاثون  , اثنتا عشرة')
        self.assertEqual(num2words(431, to='cardinal', lang='ar'),
                         'أربعمائة وواحد وثلاثون')
        self.assertEqual(num2words(94231, to='cardinal', lang='ar'),
                         'أربعة وتسعون ألفاً ومئتان وواحد وثلاثون')
        self.assertEqual(num2words(1431, to='cardinal', lang='ar'),
                         'ألف وأربعمائة وواحد وثلاثون')
        self.assertEqual(num2words(740, to='cardinal', lang='ar'),
                         'سبعمائة وأربعون')
        self.assertEqual(num2words(741, to='cardinal', lang='ar'),
                         # 'سبعة مائة وواحد وأربعون'
                         'سبعمائة وواحد وأربعون'
                         )
        self.assertEqual(num2words(262, to='cardinal', lang='ar'),
                         'مئتان واثنان وستون'
                         )
        self.assertEqual(num2words(798, to='cardinal', lang='ar'),
                         'سبعمائة وثمانية وتسعون'
                         )
        self.assertEqual(num2words(710, to='cardinal', lang='ar'),
                         'سبعمائة وعشرة')
        self.assertEqual(num2words(711, to='cardinal', lang='ar'),
                         # 'سبعة مائة وإحدى عشر'
                         'سبعمائة وأحد عشر'
                         )
        self.assertEqual(num2words(700, to='cardinal', lang='ar'),
                         'سبعمائة')
        self.assertEqual(num2words(701, to='cardinal', lang='ar'),
                         'سبعمائة وواحد')

        self.assertEqual(
            num2words(1258888, to='cardinal', lang='ar'),
            'مليون ومئتان وثمانية وخمسون ألفاً وثمانمائة وثمانية وثمانون'
        )

        self.assertEqual(num2words(1100, to='cardinal', lang='ar'),
                         'ألف ومائة')

        self.assertEqual(num2words(1000000521, to='cardinal', lang='ar'),
                         'مليار وخمسمائة وواحد وعشرون')

    def test_prefix_and_suffix(self):
        # Test prefix/suffix - may need implementation
        pass  # Will implement if needed

    def test_year(self):
        self.assertEqual(num2words(2000, to='year', lang='ar'), 'ألفا')

    def test_max_numbers(self):

        for number in 10**51, 10**51 + 2:

            with self.assertRaises(OverflowError) as context:
                num2words(number, lang='ar')

            self.assertTrue('must be less' in str(context.exception))

    def test_big_numbers(self):
        self.assertEqual(
            num2words(1000000045000000000000003000000002000000300,
                      to='cardinal', lang='ar'),
            'تريديسيليون وخمسة وأربعون ديسيليوناً\
 وثلاثة كوينتليونات وملياران وثلاثمائة'
        )
        self.assertEqual(
            num2words(-1000000000000000000000003000000002000000302,
                      to='cardinal', lang='ar'),
            'سالب تريديسيليون وثلاثة كوينتليونات \
وملياران وثلاثمائة واثنان'
        )
        self.assertEqual(
            num2words(9999999999999999999999999999999999999999999999992,
                      to='cardinal', lang='ar'),
            'تسعة كوينتينيليونات وتسعمائة و\
تسعة وتسعون كوادريسيليوناً وتسعمائة وتسعة\
 وتسعون تريديسيليوناً وتسعمائة وتسعة وتسعون دوديسيليوناً وتسعمائة\
 وتسعة وتسعون أندسيليوناً وتسعمائة وتسعة وتسعون ديسيليوناً\
 وتسعمائة وتسعة وتسعون نونيليوناً وتسعمائة وتسعة وتسعون\
 أوكتيليوناً وتسعمائة وتسعة وتسعون سبتيليوناً وتسعمائة وتسعة\
 وتسعون سكستيليوناً وتسعمائة وتسعة وتسعون كوينتليوناً وتسعمائة و\
تسعة وتسعون كوادريليوناً وتسعمائة وتسعة وتسعون تريليوناً\
 وتسعمائة وتسعة وتسعون ملياراً وتسعمائة وتسعة وتسعون مليوناً\
 وتسعمائة وتسعة وتسعون ألفاً وتسعمائة واثنان وتسعون'
        )

    def test_negative_decimals(self):
        # Comprehensive test for negative decimals including -0.4
        self.assertEqual(num2words(-0.4, lang="ar"), "سالب , أربعون")
        self.assertEqual(num2words(-0.5, lang="ar"), "سالب , خمسون")
        self.assertEqual(num2words(-1.4, lang="ar"), "سالب واحد  , أربعون")
