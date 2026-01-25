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


class Num2WordsLATest(TestCase):
    """Comprehensive test cases for Latin language."""

    def test_cardinal_basic(self):
        """Test cardinal numbers from 0 to 100."""
        self.assertEqual(num2words(0, lang="la"), "zero")
        self.assertEqual(num2words(1, lang="la"), "unus")
        self.assertEqual(num2words(2, lang="la"), "duo")
        self.assertEqual(num2words(3, lang="la"), "tres")
        self.assertEqual(num2words(4, lang="la"), "quattuor")
        self.assertEqual(num2words(5, lang="la"), "quinque")
        self.assertEqual(num2words(6, lang="la"), "sex")
        self.assertEqual(num2words(7, lang="la"), "septem")
        self.assertEqual(num2words(8, lang="la"), "octo")
        self.assertEqual(num2words(9, lang="la"), "novem")
        self.assertEqual(num2words(10, lang="la"), "decem")
        self.assertEqual(num2words(11, lang="la"), "decem unus")
        self.assertEqual(num2words(12, lang="la"), "decem duo")
        self.assertEqual(num2words(13, lang="la"), "decem tres")
        self.assertEqual(num2words(14, lang="la"), "decem quattuor")
        self.assertEqual(num2words(15, lang="la"), "decem quinque")
        self.assertEqual(num2words(16, lang="la"), "decem sex")
        self.assertEqual(num2words(17, lang="la"), "decem septem")
        self.assertEqual(num2words(18, lang="la"), "decem octo")
        self.assertEqual(num2words(19, lang="la"), "decem novem")
        self.assertEqual(num2words(20, lang="la"), "viginti")
        self.assertEqual(num2words(21, lang="la"), "viginti unus")
        self.assertEqual(num2words(22, lang="la"), "viginti duo")
        self.assertEqual(num2words(23, lang="la"), "viginti tres")
        self.assertEqual(num2words(24, lang="la"), "viginti quattuor")
        self.assertEqual(num2words(25, lang="la"), "viginti quinque")
        self.assertEqual(num2words(26, lang="la"), "viginti sex")
        self.assertEqual(num2words(27, lang="la"), "viginti septem")
        self.assertEqual(num2words(28, lang="la"), "viginti octo")
        self.assertEqual(num2words(29, lang="la"), "viginti novem")
        self.assertEqual(num2words(30, lang="la"), "triginta")
        self.assertEqual(num2words(31, lang="la"), "triginta unus")
        self.assertEqual(num2words(35, lang="la"), "triginta quinque")
        self.assertEqual(num2words(40, lang="la"), "quadraginta")
        self.assertEqual(num2words(45, lang="la"), "quadraginta quinque")
        self.assertEqual(num2words(50, lang="la"), "quinquaginta")
        self.assertEqual(num2words(55, lang="la"), "quinquaginta quinque")
        self.assertEqual(num2words(60, lang="la"), "sexaginta")
        self.assertEqual(num2words(65, lang="la"), "sexaginta quinque")
        self.assertEqual(num2words(70, lang="la"), "septuaginta")
        self.assertEqual(num2words(75, lang="la"), "septuaginta quinque")
        self.assertEqual(num2words(80, lang="la"), "octoginta")
        self.assertEqual(num2words(85, lang="la"), "octoginta quinque")
        self.assertEqual(num2words(90, lang="la"), "nonaginta")
        self.assertEqual(num2words(95, lang="la"), "nonaginta quinque")
        self.assertEqual(num2words(99, lang="la"), "nonaginta novem")
        self.assertEqual(num2words(100, lang="la"), "unus centum")

    def test_cardinal_hundreds(self):
        """Test cardinal numbers from 100 to 999."""
        self.assertEqual(num2words(101, lang="la"), "unus centum unus")
        self.assertEqual(num2words(110, lang="la"), "unus centum decem")
        self.assertEqual(num2words(111, lang="la"), "unus centum decem unus")
        self.assertEqual(num2words(120, lang="la"), "unus centum viginti")
        self.assertEqual(num2words(125, lang="la"), "unus centum viginti quinque")
        self.assertEqual(num2words(150, lang="la"), "unus centum quinquaginta")
        self.assertEqual(num2words(175, lang="la"), "unus centum septuaginta quinque")
        self.assertEqual(num2words(199, lang="la"), "unus centum nonaginta novem")
        self.assertEqual(num2words(200, lang="la"), "duo centum")
        self.assertEqual(num2words(201, lang="la"), "duo centum unus")
        self.assertEqual(num2words(210, lang="la"), "duo centum decem")
        self.assertEqual(num2words(220, lang="la"), "duo centum viginti")
        self.assertEqual(num2words(250, lang="la"), "duo centum quinquaginta")
        self.assertEqual(num2words(299, lang="la"), "duo centum nonaginta novem")
        self.assertEqual(num2words(300, lang="la"), "tres centum")
        self.assertEqual(num2words(333, lang="la"), "tres centum triginta tres")
        self.assertEqual(num2words(400, lang="la"), "quattuor centum")
        self.assertEqual(
            num2words(444, lang="la"), "quattuor centum quadraginta quattuor"
        )
        self.assertEqual(num2words(500, lang="la"), "quinque centum")
        self.assertEqual(
            num2words(555, lang="la"), "quinque centum quinquaginta quinque"
        )
        self.assertEqual(num2words(600, lang="la"), "sex centum")
        self.assertEqual(num2words(666, lang="la"), "sex centum sexaginta sex")
        self.assertEqual(num2words(700, lang="la"), "septem centum")
        self.assertEqual(num2words(777, lang="la"), "septem centum septuaginta septem")
        self.assertEqual(num2words(800, lang="la"), "octo centum")
        self.assertEqual(num2words(888, lang="la"), "octo centum octoginta octo")
        self.assertEqual(num2words(900, lang="la"), "novem centum")
        self.assertEqual(num2words(999, lang="la"), "novem centum nonaginta novem")

    def test_cardinal_thousands(self):
        """Test cardinal numbers from 1000 to 999999."""
        self.assertEqual(num2words(1000, lang="la"), "unus mille")
        self.assertEqual(num2words(1001, lang="la"), "unus mille unus")
        self.assertEqual(num2words(1010, lang="la"), "unus mille decem")
        self.assertEqual(num2words(1100, lang="la"), "unus mille unus centum")
        self.assertEqual(
            num2words(1111, lang="la"), "unus mille unus centum decem unus"
        )
        self.assertEqual(
            num2words(1234, lang="la"), "unus mille duo centum triginta quattuor"
        )
        self.assertEqual(num2words(1500, lang="la"), "unus mille quinque centum")
        self.assertEqual(
            num2words(1999, lang="la"), "unus mille novem centum nonaginta novem"
        )
        self.assertEqual(num2words(2000, lang="la"), "duo mille")
        self.assertEqual(num2words(2001, lang="la"), "duo mille unus")
        self.assertEqual(num2words(2020, lang="la"), "duo mille viginti")
        self.assertEqual(num2words(2222, lang="la"), "duo mille duo centum viginti duo")
        self.assertEqual(num2words(3000, lang="la"), "tres mille")
        self.assertEqual(
            num2words(3333, lang="la"), "tres mille tres centum triginta tres"
        )
        self.assertEqual(num2words(4000, lang="la"), "quattuor mille")
        self.assertEqual(
            num2words(4444, lang="la"),
            "quattuor mille quattuor centum quadraginta quattuor",
        )
        self.assertEqual(num2words(5000, lang="la"), "quinque mille")
        self.assertEqual(
            num2words(5555, lang="la"),
            "quinque mille quinque centum quinquaginta quinque",
        )
        self.assertEqual(num2words(6000, lang="la"), "sex mille")
        self.assertEqual(
            num2words(6666, lang="la"), "sex mille sex centum sexaginta sex"
        )
        self.assertEqual(num2words(7000, lang="la"), "septem mille")
        self.assertEqual(
            num2words(7777, lang="la"), "septem mille septem centum septuaginta septem"
        )
        self.assertEqual(num2words(8000, lang="la"), "octo mille")
        self.assertEqual(
            num2words(8888, lang="la"), "octo mille octo centum octoginta octo"
        )
        self.assertEqual(num2words(9000, lang="la"), "novem mille")
        self.assertEqual(
            num2words(9999, lang="la"), "novem mille novem centum nonaginta novem"
        )
        self.assertEqual(num2words(10000, lang="la"), "decem mille")
        self.assertEqual(num2words(10001, lang="la"), "decem mille unus")
        self.assertEqual(
            num2words(11111, lang="la"), "decem unus mille unus centum decem unus"
        )
        self.assertEqual(
            num2words(12345, lang="la"),
            "decem duo mille tres centum quadraginta quinque",
        )
        self.assertEqual(num2words(20000, lang="la"), "viginti mille")
        self.assertEqual(num2words(50000, lang="la"), "quinquaginta mille")
        self.assertEqual(
            num2words(99999, lang="la"),
            "nonaginta novem mille novem centum nonaginta novem",
        )
        self.assertEqual(num2words(100000, lang="la"), "unus centum mille")
        self.assertEqual(
            num2words(123456, lang="la"),
            "unus centum viginti tres mille quattuor centum quinquaginta sex",
        )
        self.assertEqual(num2words(200000, lang="la"), "duo centum mille")
        self.assertEqual(num2words(500000, lang="la"), "quinque centum mille")
        self.assertEqual(
            num2words(654321, lang="la"),
            "sex centum quinquaginta quattuor mille tres centum viginti unus",
        )
        self.assertEqual(
            num2words(999999, lang="la"),
            "novem centum nonaginta novem mille novem centum nonaginta novem",
        )

    def test_cardinal_large(self):
        """Test large cardinal numbers (millions and billions)."""
        self.assertEqual(num2words(1000000, lang="la"), "unus decies centena milia")
        self.assertEqual(
            num2words(1000001, lang="la"), "unus decies centena milia unus"
        )
        self.assertEqual(
            num2words(1111111, lang="la"),
            "unus decies centena milia unus centum decem unus mille unus centum decem unus",
        )
        self.assertEqual(
            num2words(1234567, lang="la"),
            "unus decies centena milia duo centum triginta quattuor mille quinque centum sexaginta septem",
        )
        self.assertEqual(num2words(2000000, lang="la"), "duo decies centena milia")
        self.assertEqual(num2words(5000000, lang="la"), "quinque decies centena milia")
        self.assertEqual(
            num2words(9999999, lang="la"),
            "novem decies centena milia novem centum nonaginta novem mille novem centum nonaginta novem",
        )
        self.assertEqual(num2words(10000000, lang="la"), "decem decies centena milia")
        self.assertEqual(
            num2words(12345678, lang="la"),
            "decem duo decies centena milia tres centum quadraginta quinque mille sex centum septuaginta octo",
        )
        self.assertEqual(
            num2words(99999999, lang="la"),
            "nonaginta novem decies centena milia novem centum nonaginta novem mille novem centum nonaginta novem",
        )
        self.assertEqual(
            num2words(100000000, lang="la"), "unus centum decies centena milia"
        )
        self.assertEqual(
            num2words(123456789, lang="la"),
            "unus centum viginti tres decies centena milia quattuor centum quinquaginta sex mille septem centum octoginta novem",
        )
        self.assertEqual(
            num2words(999999999, lang="la"),
            "novem centum nonaginta novem decies centena milia novem centum nonaginta novem mille novem centum nonaginta novem",
        )
        self.assertEqual(num2words(1000000000, lang="la"), "1000000000")
        self.assertEqual(num2words(1234567890, lang="la"), "1234567890")
        self.assertEqual(num2words(9999999999, lang="la"), "9999999999")
        self.assertEqual(num2words(10000000000, lang="la"), "10000000000")
        self.assertEqual(num2words(99999999999, lang="la"), "99999999999")

    def test_negative_numbers(self):
        """Test negative numbers."""
        self.assertEqual(num2words(-1, lang="la"), "minus unus")
        self.assertEqual(num2words(-2, lang="la"), "minus duo")
        self.assertEqual(num2words(-5, lang="la"), "minus quinque")
        self.assertEqual(num2words(-10, lang="la"), "minus decem")
        self.assertEqual(num2words(-11, lang="la"), "minus decem unus")
        self.assertEqual(num2words(-20, lang="la"), "minus viginti")
        self.assertEqual(num2words(-50, lang="la"), "minus quinquaginta")
        self.assertEqual(num2words(-99, lang="la"), "minus nonaginta novem")
        self.assertEqual(num2words(-100, lang="la"), "minus unus centum")
        self.assertEqual(num2words(-101, lang="la"), "minus unus centum unus")
        self.assertEqual(num2words(-200, lang="la"), "minus duo centum")
        self.assertEqual(
            num2words(-999, lang="la"), "minus novem centum nonaginta novem"
        )
        self.assertEqual(num2words(-1000, lang="la"), "minus unus mille")
        self.assertEqual(num2words(-1001, lang="la"), "minus unus mille unus")
        self.assertEqual(num2words(-10000, lang="la"), "minus decem mille")
        self.assertEqual(num2words(-100000, lang="la"), "minus unus centum mille")
        self.assertEqual(
            num2words(-1000000, lang="la"), "minus unus decies centena milia"
        )

    def test_decimal_numbers(self):
        """Test decimal numbers."""
        self.assertEqual(num2words(0.1, lang="la"), "zero point unus")
        self.assertEqual(num2words(0.5, lang="la"), "zero point quinque")
        self.assertEqual(num2words(0.9, lang="la"), "zero point novem")
        self.assertEqual(num2words(1.1, lang="la"), "unus point unus")
        self.assertEqual(num2words(1.5, lang="la"), "unus point quinque")
        self.assertEqual(num2words(2.5, lang="la"), "duo point quinque")
        self.assertEqual(num2words(3.14, lang="la"), "tres point unus quattuor")
        self.assertEqual(num2words(10.5, lang="la"), "decem point quinque")
        self.assertEqual(num2words(11.11, lang="la"), "decem unus point unus unus")
        self.assertEqual(num2words(20.2, lang="la"), "viginti point duo")
        self.assertEqual(
            num2words(99.99, lang="la"), "nonaginta novem point novem novem"
        )
        self.assertEqual(num2words(100.01, lang="la"), "unus centum point zero unus")
        self.assertEqual(num2words(100.5, lang="la"), "unus centum point quinque")
        self.assertEqual(
            num2words(123.45, lang="la"),
            "unus centum viginti tres point quattuor quinque",
        )
        self.assertEqual(num2words(1000.5, lang="la"), "unus mille point quinque")
        self.assertEqual(
            num2words(1234.56, lang="la"),
            "unus mille duo centum triginta quattuor point quinque sex",
        )
        self.assertEqual(num2words(10000.01, lang="la"), "decem mille point zero unus")
        self.assertEqual(num2words(-0.5, lang="la"), "minus zero point quinque")
        self.assertEqual(num2words(-1.5, lang="la"), "minus unus point quinque")
        self.assertEqual(num2words(-10.5, lang="la"), "minus decem point quinque")

    def test_ordinal(self):
        """Test ordinal numbers."""
        self.assertEqual(num2words(1, lang="la", ordinal=True), "unus-us")
        self.assertEqual(num2words(2, lang="la", ordinal=True), "duo-us")
        self.assertEqual(num2words(3, lang="la", ordinal=True), "tres-us")
        self.assertEqual(num2words(4, lang="la", ordinal=True), "quattuor-us")
        self.assertEqual(num2words(5, lang="la", ordinal=True), "quinque-us")
        self.assertEqual(num2words(6, lang="la", ordinal=True), "sex-us")
        self.assertEqual(num2words(7, lang="la", ordinal=True), "septem-us")
        self.assertEqual(num2words(8, lang="la", ordinal=True), "octo-us")
        self.assertEqual(num2words(9, lang="la", ordinal=True), "novem-us")
        self.assertEqual(num2words(10, lang="la", ordinal=True), "decem-us")
        self.assertEqual(num2words(11, lang="la", ordinal=True), "decem unus-us")
        self.assertEqual(num2words(12, lang="la", ordinal=True), "decem duo-us")
        self.assertEqual(num2words(13, lang="la", ordinal=True), "decem tres-us")
        self.assertEqual(num2words(14, lang="la", ordinal=True), "decem quattuor-us")
        self.assertEqual(num2words(15, lang="la", ordinal=True), "decem quinque-us")
        self.assertEqual(num2words(16, lang="la", ordinal=True), "decem sex-us")
        self.assertEqual(num2words(17, lang="la", ordinal=True), "decem septem-us")
        self.assertEqual(num2words(18, lang="la", ordinal=True), "decem octo-us")
        self.assertEqual(num2words(19, lang="la", ordinal=True), "decem novem-us")
        self.assertEqual(num2words(20, lang="la", ordinal=True), "viginti-us")
        self.assertEqual(num2words(21, lang="la", ordinal=True), "viginti unus-us")
        self.assertEqual(num2words(22, lang="la", ordinal=True), "viginti duo-us")
        self.assertEqual(num2words(25, lang="la", ordinal=True), "viginti quinque-us")
        self.assertEqual(num2words(30, lang="la", ordinal=True), "triginta-us")
        self.assertEqual(num2words(40, lang="la", ordinal=True), "quadraginta-us")
        self.assertEqual(num2words(50, lang="la", ordinal=True), "quinquaginta-us")
        self.assertEqual(num2words(60, lang="la", ordinal=True), "sexaginta-us")
        self.assertEqual(num2words(70, lang="la", ordinal=True), "septuaginta-us")
        self.assertEqual(num2words(80, lang="la", ordinal=True), "octoginta-us")
        self.assertEqual(num2words(90, lang="la", ordinal=True), "nonaginta-us")
        self.assertEqual(num2words(100, lang="la", ordinal=True), "unus centum-us")
        self.assertEqual(num2words(101, lang="la", ordinal=True), "unus centum unus-us")
        self.assertEqual(num2words(200, lang="la", ordinal=True), "duo centum-us")
        self.assertEqual(num2words(500, lang="la", ordinal=True), "quinque centum-us")
        self.assertEqual(num2words(1000, lang="la", ordinal=True), "unus mille-us")
        self.assertEqual(num2words(1001, lang="la", ordinal=True), "unus mille unus-us")
        self.assertEqual(num2words(10000, lang="la", ordinal=True), "decem mille-us")

    def test_currency(self):
        """Test currency conversion."""
        self.assertEqual(
            num2words(0, lang="la", to="currency", currency="EUR"), "zero euros"
        )
        self.assertEqual(
            num2words(0.01, lang="la", to="currency", currency="EUR"),
            "zero euros unus centesima",
        )
        self.assertEqual(
            num2words(0.5, lang="la", to="currency", currency="EUR"),
            "zero euros quinquaginta centesimae",
        )
        self.assertEqual(
            num2words(1, lang="la", to="currency", currency="EUR"), "unus euro"
        )
        self.assertEqual(
            num2words(1.5, lang="la", to="currency", currency="EUR"),
            "unus euro quinquaginta centesimae",
        )
        self.assertEqual(
            num2words(0, lang="la", to="currency", currency="USD"), "zero dollars"
        )
        self.assertEqual(
            num2words(0.01, lang="la", to="currency", currency="USD"),
            "zero dollars unus cent",
        )
        self.assertEqual(
            num2words(0.5, lang="la", to="currency", currency="USD"),
            "zero dollars quinquaginta cents",
        )
        self.assertEqual(
            num2words(1, lang="la", to="currency", currency="USD"), "unus dollar"
        )
        self.assertEqual(
            num2words(1.5, lang="la", to="currency", currency="USD"),
            "unus dollar quinquaginta cents",
        )

    def test_year(self):
        """Test year conversion."""
        self.assertEqual(num2words(1000, lang="la", to="year"), "unus mille")
        self.assertEqual(
            num2words(1066, lang="la", to="year"), "unus mille sexaginta sex"
        )
        self.assertEqual(
            num2words(1492, lang="la", to="year"),
            "unus mille quattuor centum nonaginta duo",
        )
        self.assertEqual(
            num2words(1776, lang="la", to="year"),
            "unus mille septem centum septuaginta sex",
        )
        self.assertEqual(
            num2words(1800, lang="la", to="year"), "unus mille octo centum"
        )
        self.assertEqual(
            num2words(1900, lang="la", to="year"), "unus mille novem centum"
        )
        self.assertEqual(
            num2words(1984, lang="la", to="year"),
            "unus mille novem centum octoginta quattuor",
        )
        self.assertEqual(
            num2words(1999, lang="la", to="year"),
            "unus mille novem centum nonaginta novem",
        )
        self.assertEqual(num2words(2000, lang="la", to="year"), "duo mille")
        self.assertEqual(num2words(2001, lang="la", to="year"), "duo mille unus")
        self.assertEqual(num2words(2010, lang="la", to="year"), "duo mille decem")
        self.assertEqual(num2words(2020, lang="la", to="year"), "duo mille viginti")
        self.assertEqual(
            num2words(2024, lang="la", to="year"), "duo mille viginti quattuor"
        )
        self.assertEqual(num2words(2100, lang="la", to="year"), "duo mille unus centum")

    def test_string_input(self):
        """Test string input conversion."""
        self.assertEqual(num2words("0", lang="la"), "zero")
        self.assertEqual(num2words("1", lang="la"), "unus")
        self.assertEqual(num2words("10", lang="la"), "decem")
        self.assertEqual(num2words("100", lang="la"), "unus centum")
        self.assertEqual(num2words("1000", lang="la"), "unus mille")
        self.assertEqual(num2words("10000", lang="la"), "decem mille")
        self.assertEqual(num2words("100000", lang="la"), "unus centum mille")
        self.assertEqual(num2words("1000000", lang="la"), "unus decies centena milia")

    def test_edge_cases(self):
        """Test edge cases and special conditions."""
        # Test zero
        self.assertEqual(num2words(0, lang="la"), "zero")

        # Test that the converter handles various input types
        self.assertEqual(num2words(100, lang="la"), num2words("100", lang="la"))
        self.assertEqual(num2words(1000, lang="la"), num2words("1000", lang="la"))

    def test_converter_methods(self):
        """Test direct converter methods for better coverage."""
        from num2words2.lang_LA import Num2Word_LA

        converter = Num2Word_LA()

        # Test direct cardinal conversion
        self.assertIsNotNone(converter.to_cardinal(42))
        self.assertIsNotNone(converter.to_cardinal(1337))

        # Test setup method
        converter.setup()

        # Test negative word if exists
        if hasattr(converter, "negword"):
            self.assertIsNotNone(converter.negword)

        # Test point word if exists
        if hasattr(converter, "pointword"):
            self.assertIsNotNone(converter.pointword)
