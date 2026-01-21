# coding: utf-8
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


class Num2WordsISTest(TestCase):

    def test_cardinal(self):
        self.assertEqual(num2words(0, to="cardinal", lang="is"),
                         "núll")
        self.assertEqual(num2words(1, to="cardinal", lang="is"),
                         "einn")
        self.assertEqual(num2words(45, to="cardinal", lang="is"),
                         "fjörutíu og fimm")
        self.assertEqual(num2words(145, to="cardinal", lang="is"),
                         "eitt hundrað fjörutíu og fimm")
        self.assertEqual(num2words(-1245, to="cardinal", lang="is"),
                         "mínus eitt þúsund tvö hundruð fjörutíu og fimm")
        self.assertEqual(num2words(2234045, to="cardinal", lang="is"),
                         "tvær milljónir tvö hundruð þrjátíu og fjögur þúsund "
                         "fjörutíu og fimm")
        self.assertEqual(num2words(4002234045, to="cardinal", lang="is"),
                         "fjórir milljarðar tvær milljónir tvö hundruð "
                         "þrjátíu og fjögur þúsund fjörutíu og fimm")

    def test_cardinal_for_float_number(self):
        self.assertEqual(num2words(12.5, to="cardinal", lang="is"),
                         "tólf komma fimm")
        self.assertEqual(num2words(12.51, to="cardinal", lang="is"),
                         "tólf komma fimm einn")
        self.assertEqual(num2words(-12.53, to="cardinal", lang="is"),
                         "mínus tólf komma fimm þrír")
        self.assertEqual(num2words(12.59, to="cardinal", lang="is"),
                         "tólf komma fimm níu")

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            num2words("1000000000000000000000000000000000000000000000000000000"
                      "0000000000000000000000000000000000000000000000000000000"
                      "0000000000000000000000000000000000000000000000000000000"
                      "0000000000000000000000000000000000000000000000000000000"
                      "0000000000000000000000000000000000000000000000000000000"
                      "00000000000000000000000000000000", lang="is")

    def test_ordinal(self):
        # Test ordinal numbers
        self.assertEqual(num2words(1, to="ordinal", lang="is"), "fyrsti")
        self.assertEqual(num2words(2, to="ordinal", lang="is"), "annar")
        self.assertEqual(num2words(3, to="ordinal", lang="is"), "þriðji")
        self.assertEqual(num2words(4, to="ordinal", lang="is"), "fjórði")
        self.assertEqual(num2words(5, to="ordinal", lang="is"), "fimmti")
        self.assertEqual(num2words(10, to="ordinal", lang="is"), "tíundi")
        self.assertEqual(num2words(20, to="ordinal", lang="is"), "tuttugasti")
        self.assertEqual(num2words(100, to="ordinal", lang="is"), "hundraðasti")

    def test_ordinal_num(self):
        # Test ordinal number formatting
        self.assertEqual(num2words(1, to="ordinal_num", lang="is"), "1.")
        self.assertEqual(num2words(10, to="ordinal_num", lang="is"), "10.")
        self.assertEqual(num2words(21, to="ordinal_num", lang="is"), "21.")

    def test_year(self):
        # Test year conversion
        self.assertEqual(
            num2words(2021, to="year", lang="is"),
            "tvö þúsund tuttugu og einn"
        )
        self.assertEqual(
            num2words(1999, to="year", lang="is"),
            "eitt þúsund níu hundruð níutíu og níu"
        )
        self.assertEqual(
            num2words(2000, to="year", lang="is"),
            "tvö þúsund"
        )

    def test_negative_decimals(self):
        # Comprehensive test for negative decimals including -0.4
        self.assertEqual(num2words(-0.4, lang="is"), "mínus núll komma fjórir")
        self.assertEqual(num2words(-0.5, lang="is"), "mínus núll komma fimm")
        self.assertEqual(num2words(-1.4, lang="is"), "mínus einn komma fjórir")
