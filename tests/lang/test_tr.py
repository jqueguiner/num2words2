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


class Num2WordsTRTest(TestCase):
    """Comprehensive test cases for Turkish language."""

    def test_cardinal_basic(self):
        """Test cardinal numbers from 0 to 100."""
        self.assertEqual(num2words(0, lang="tr"), "sıfır")
        self.assertEqual(num2words(1, lang="tr"), "bir")
        self.assertEqual(num2words(2, lang="tr"), "iki")
        self.assertEqual(num2words(3, lang="tr"), "üç")
        self.assertEqual(num2words(4, lang="tr"), "dört")
        self.assertEqual(num2words(5, lang="tr"), "beş")
        self.assertEqual(num2words(6, lang="tr"), "altı")
        self.assertEqual(num2words(7, lang="tr"), "yedi")
        self.assertEqual(num2words(8, lang="tr"), "sekiz")
        self.assertEqual(num2words(9, lang="tr"), "dokuz")
        self.assertEqual(num2words(10, lang="tr"), "on")
        self.assertEqual(num2words(11, lang="tr"), "onbir")
        self.assertEqual(num2words(12, lang="tr"), "oniki")
        self.assertEqual(num2words(13, lang="tr"), "onüç")
        self.assertEqual(num2words(14, lang="tr"), "ondört")
        self.assertEqual(num2words(15, lang="tr"), "onbeş")
        self.assertEqual(num2words(16, lang="tr"), "onaltı")
        self.assertEqual(num2words(17, lang="tr"), "onyedi")
        self.assertEqual(num2words(18, lang="tr"), "onsekiz")
        self.assertEqual(num2words(19, lang="tr"), "ondokuz")
        self.assertEqual(num2words(20, lang="tr"), "yirmi")
        self.assertEqual(num2words(21, lang="tr"), "yirmibir")
        self.assertEqual(num2words(22, lang="tr"), "yirmiiki")
        self.assertEqual(num2words(23, lang="tr"), "yirmiüç")
        self.assertEqual(num2words(24, lang="tr"), "yirmidört")
        self.assertEqual(num2words(25, lang="tr"), "yirmibeş")
        self.assertEqual(num2words(26, lang="tr"), "yirmialtı")
        self.assertEqual(num2words(27, lang="tr"), "yirmiyedi")
        self.assertEqual(num2words(28, lang="tr"), "yirmisekiz")
        self.assertEqual(num2words(29, lang="tr"), "yirmidokuz")
        self.assertEqual(num2words(30, lang="tr"), "otuz")
        self.assertEqual(num2words(31, lang="tr"), "otuzbir")
        self.assertEqual(num2words(35, lang="tr"), "otuzbeş")
        self.assertEqual(num2words(40, lang="tr"), "kırk")
        self.assertEqual(num2words(45, lang="tr"), "kırkbeş")
        self.assertEqual(num2words(50, lang="tr"), "elli")
        self.assertEqual(num2words(55, lang="tr"), "ellibeş")
        self.assertEqual(num2words(60, lang="tr"), "altmış")
        self.assertEqual(num2words(65, lang="tr"), "altmışbeş")
        self.assertEqual(num2words(70, lang="tr"), "yetmiş")
        self.assertEqual(num2words(75, lang="tr"), "yetmişbeş")
        self.assertEqual(num2words(80, lang="tr"), "seksen")
        self.assertEqual(num2words(85, lang="tr"), "seksenbeş")
        self.assertEqual(num2words(90, lang="tr"), "doksan")
        self.assertEqual(num2words(95, lang="tr"), "doksanbeş")
        self.assertEqual(num2words(99, lang="tr"), "doksandokuz")
        self.assertEqual(num2words(100, lang="tr"), "yüz")

    def test_cardinal_hundreds(self):
        """Test cardinal numbers from 100 to 999."""
        self.assertEqual(num2words(101, lang="tr"), "yüzbir")
        self.assertEqual(num2words(110, lang="tr"), "yüzon")
        self.assertEqual(num2words(111, lang="tr"), "yüzonbir")
        self.assertEqual(num2words(120, lang="tr"), "yüzyirmi")
        self.assertEqual(num2words(125, lang="tr"), "yüzyirmibeş")
        self.assertEqual(num2words(150, lang="tr"), "yüzelli")
        self.assertEqual(num2words(175, lang="tr"), "yüzyetmişbeş")
        self.assertEqual(num2words(199, lang="tr"), "yüzdoksandokuz")
        self.assertEqual(num2words(200, lang="tr"), "ikiyüz")
        self.assertEqual(num2words(201, lang="tr"), "ikiyüzbir")
        self.assertEqual(num2words(210, lang="tr"), "ikiyüzon")
        self.assertEqual(num2words(220, lang="tr"), "ikiyüzyirmi")
        self.assertEqual(num2words(250, lang="tr"), "ikiyüzelli")
        self.assertEqual(num2words(299, lang="tr"), "ikiyüzdoksandokuz")
        self.assertEqual(num2words(300, lang="tr"), "üçyüz")
        self.assertEqual(num2words(333, lang="tr"), "üçyüzotuzüç")
        self.assertEqual(num2words(400, lang="tr"), "dörtyüz")
        self.assertEqual(num2words(444, lang="tr"), "dörtyüzkırkdört")
        self.assertEqual(num2words(500, lang="tr"), "beşyüz")
        self.assertEqual(num2words(555, lang="tr"), "beşyüzellibeş")
        self.assertEqual(num2words(600, lang="tr"), "altıyüz")
        self.assertEqual(num2words(666, lang="tr"), "altıyüzaltmışaltı")
        self.assertEqual(num2words(700, lang="tr"), "yediyüz")
        self.assertEqual(num2words(777, lang="tr"), "yediyüzyetmişyedi")
        self.assertEqual(num2words(800, lang="tr"), "sekizyüz")
        self.assertEqual(num2words(888, lang="tr"), "sekizyüzseksensekiz")
        self.assertEqual(num2words(900, lang="tr"), "dokuzyüz")
        self.assertEqual(num2words(999, lang="tr"), "dokuzyüzdoksandokuz")

    def test_cardinal_thousands(self):
        """Test cardinal numbers from 1000 to 999999."""
        self.assertEqual(num2words(1000, lang="tr"), "bin")
        self.assertEqual(num2words(1001, lang="tr"), "binbir")
        self.assertEqual(num2words(1010, lang="tr"), "binon")
        self.assertEqual(num2words(1100, lang="tr"), "binyüz")
        self.assertEqual(num2words(1111, lang="tr"), "binyüzonbir")
        self.assertEqual(num2words(1234, lang="tr"), "binikiyüzotuzdört")
        self.assertEqual(num2words(1500, lang="tr"), "binbeşyüz")
        self.assertEqual(num2words(1999, lang="tr"), "bindokuzyüzdoksandokuz")
        self.assertEqual(num2words(2000, lang="tr"), "ikibin")
        self.assertEqual(num2words(2001, lang="tr"), "ikibinbir")
        self.assertEqual(num2words(2020, lang="tr"), "ikibinyirmi")
        self.assertEqual(num2words(2222, lang="tr"), "ikibinikiyüzyirmiiki")
        self.assertEqual(num2words(3000, lang="tr"), "üçbin")
        self.assertEqual(num2words(3333, lang="tr"), "üçbinüçyüzotuzüç")
        self.assertEqual(num2words(4000, lang="tr"), "dörtbin")
        self.assertEqual(num2words(4444, lang="tr"), "dörtbindörtyüzkırkdört")
        self.assertEqual(num2words(5000, lang="tr"), "beşbin")
        self.assertEqual(num2words(5555, lang="tr"), "beşbinbeşyüzellibeş")
        self.assertEqual(num2words(6000, lang="tr"), "altıbin")
        self.assertEqual(num2words(6666, lang="tr"), "altıbinaltıyüzaltmışaltı")
        self.assertEqual(num2words(7000, lang="tr"), "yedibin")
        self.assertEqual(num2words(7777, lang="tr"), "yedibinyediyüzyetmişyedi")
        self.assertEqual(num2words(8000, lang="tr"), "sekizbin")
        self.assertEqual(num2words(8888, lang="tr"), "sekizbinsekizyüzseksensekiz")
        self.assertEqual(num2words(9000, lang="tr"), "dokuzbin")
        self.assertEqual(num2words(9999, lang="tr"), "dokuzbindokuzyüzdoksandokuz")
        self.assertEqual(num2words(10000, lang="tr"), "onbin")
        self.assertEqual(num2words(10001, lang="tr"), "onbinbir")
        self.assertEqual(num2words(11111, lang="tr"), "onbirbinyüzonbir")
        self.assertEqual(num2words(12345, lang="tr"), "onikibinüçyüzkırkbeş")
        self.assertEqual(num2words(20000, lang="tr"), "yirmibin")
        self.assertEqual(num2words(50000, lang="tr"), "ellibin")
        self.assertEqual(
            num2words(99999, lang="tr"), "doksandokuzbindokuzyüzdoksandokuz"
        )
        self.assertEqual(num2words(100000, lang="tr"), "yüzbin")
        self.assertEqual(num2words(123456, lang="tr"), "yüzyirmiüçbindörtyüzellialtı")
        self.assertEqual(num2words(200000, lang="tr"), "ikiyüzbin")
        self.assertEqual(num2words(500000, lang="tr"), "beşyüzbin")
        self.assertEqual(
            num2words(654321, lang="tr"), "altıyüzellidörtbinüçyüzyirmibir"
        )
        self.assertEqual(
            num2words(999999, lang="tr"), "dokuzyüzdoksandokuzbindokuzyüzdoksandokuz"
        )

    def test_cardinal_large(self):
        """Test large cardinal numbers (millions and billions)."""
        self.assertEqual(num2words(1000000, lang="tr"), "birmilyon")
        self.assertEqual(num2words(1000001, lang="tr"), "birmilyonbir")
        self.assertEqual(num2words(1111111, lang="tr"), "birmilyonyüzonbirbinyüzonbir")
        self.assertEqual(
            num2words(1234567, lang="tr"), "birmilyonikiyüzotuzdörtbinbeşyüzaltmışyedi"
        )
        self.assertEqual(num2words(2000000, lang="tr"), "ikimilyon")
        self.assertEqual(num2words(5000000, lang="tr"), "beşmilyon")
        self.assertEqual(
            num2words(9999999, lang="tr"),
            "dokuzmilyondokuzyüzdoksandokuzbindokuzyüzdoksandokuz",
        )
        self.assertEqual(num2words(10000000, lang="tr"), "onmilyon")
        self.assertEqual(
            num2words(12345678, lang="tr"),
            "onikimilyonüçyüzkırkbeşbinaltıyüzyetmişsekiz",
        )
        self.assertEqual(
            num2words(99999999, lang="tr"),
            "doksandokuzmilyondokuzyüzdoksandokuzbindokuzyüzdoksandokuz",
        )
        self.assertEqual(num2words(100000000, lang="tr"), "yüzmilyon")
        self.assertEqual(
            num2words(123456789, lang="tr"),
            "yüzyirmiüçmilyondörtyüzellialtıbinyediyüzseksendokuz",
        )
        self.assertEqual(
            num2words(999999999, lang="tr"),
            "dokuzyüzdoksandokuzmilyondokuzyüzdoksandokuzbindokuzyüzdoksandokuz",
        )
        self.assertEqual(num2words(1000000000, lang="tr"), "birmilyar")
        self.assertEqual(
            num2words(1234567890, lang="tr"),
            "birmilyarikiyüzotuzdörtmilyonbeşyüzaltmışyedibinsekizyüzdoksan",
        )
        self.assertEqual(
            num2words(9999999999, lang="tr"),
            "dokuzmilyardokuzyüzdoksandokuzmilyondokuzyüzdoksandokuzbindokuzyüzdoksandokuz",
        )
        self.assertEqual(num2words(10000000000, lang="tr"), "onmilyar")
        self.assertEqual(
            num2words(99999999999, lang="tr"),
            "doksandokuzmilyardokuzyüzdoksandokuzmilyondokuzyüzdoksandokuzbindokuzyüzdoksandokuz",
        )

    def test_negative_numbers(self):
        """Test negative numbers."""
        self.assertEqual(num2words(-1, lang="tr"), "eksibir")
        self.assertEqual(num2words(-2, lang="tr"), "eksiiki")
        self.assertEqual(num2words(-5, lang="tr"), "eksibeş")
        self.assertEqual(num2words(-10, lang="tr"), "eksion")
        self.assertEqual(num2words(-11, lang="tr"), "eksionbir")
        self.assertEqual(num2words(-20, lang="tr"), "eksiyirmi")
        self.assertEqual(num2words(-50, lang="tr"), "eksielli")
        self.assertEqual(num2words(-99, lang="tr"), "eksidoksandokuz")
        self.assertEqual(num2words(-100, lang="tr"), "eksiyüz")
        self.assertEqual(num2words(-101, lang="tr"), "eksiyüzbir")
        self.assertEqual(num2words(-200, lang="tr"), "eksiikiyüz")
        self.assertEqual(num2words(-999, lang="tr"), "eksidokuzyüzdoksandokuz")
        self.assertEqual(num2words(-1000, lang="tr"), "eksibin")
        self.assertEqual(num2words(-1001, lang="tr"), "eksibinbir")
        self.assertEqual(num2words(-10000, lang="tr"), "eksionbin")
        self.assertEqual(num2words(-100000, lang="tr"), "eksiyüzbin")
        self.assertEqual(num2words(-1000000, lang="tr"), "eksibirmilyon")

    def test_decimal_numbers(self):
        """Test decimal numbers."""
        self.assertEqual(num2words(0.1, lang="tr"), "sıfırvirgülon")
        self.assertEqual(num2words(0.5, lang="tr"), "sıfırvirgülelli")
        self.assertEqual(num2words(0.9, lang="tr"), "sıfırvirgüldoksan")
        self.assertEqual(num2words(1.1, lang="tr"), "birvirgülon")
        self.assertEqual(num2words(1.5, lang="tr"), "birvirgülelli")
        self.assertEqual(num2words(2.5, lang="tr"), "ikivirgülelli")
        self.assertEqual(num2words(3.14, lang="tr"), "üçvirgülondört")
        self.assertEqual(num2words(10.5, lang="tr"), "onvirgülelli")
        self.assertEqual(num2words(11.11, lang="tr"), "onbirvirgülonbir")
        self.assertEqual(num2words(20.2, lang="tr"), "yirmivirgülyirmi")
        self.assertEqual(num2words(99.99, lang="tr"), "doksandokuzvirgüldoksandokuz")
        self.assertEqual(num2words(100.01, lang="tr"), "yüzvirgülsıfırbir")
        # Regression for savoirfairelinux/num2words#487 (leading zero in fractional).
        self.assertEqual(num2words(0.03, lang="tr"), "sıfırvirgülsıfırüç")
        self.assertEqual(num2words(0.05, lang="tr"), "sıfırvirgülsıfırbeş")
        self.assertEqual(num2words(100.5, lang="tr"), "yüzvirgülelli")
        self.assertEqual(num2words(123.45, lang="tr"), "yüzyirmiüçvirgülkırkbeş")
        self.assertEqual(num2words(1000.5, lang="tr"), "binvirgülelli")
        self.assertEqual(
            num2words(1234.56, lang="tr"), "binikiyüzotuzdörtvirgülellialtı"
        )
        self.assertEqual(num2words(10000.01, lang="tr"), "onbinvirgülsıfırbir")
        self.assertEqual(num2words(-0.5, lang="tr"), "eksi sıfırvirgülelli")
        self.assertEqual(num2words(-1.5, lang="tr"), "eksi birvirgülelli")
        self.assertEqual(num2words(-10.5, lang="tr"), "eksi onvirgülelli")

    def test_ordinal(self):
        """Test ordinal numbers."""
        self.assertEqual(num2words(1, lang="tr", ordinal=True), "birinci")
        self.assertEqual(num2words(2, lang="tr", ordinal=True), "ikinci")
        self.assertEqual(num2words(3, lang="tr", ordinal=True), "üçüncü")
        self.assertEqual(num2words(4, lang="tr", ordinal=True), "dördüncü")
        self.assertEqual(num2words(5, lang="tr", ordinal=True), "beşinci")
        self.assertEqual(num2words(6, lang="tr", ordinal=True), "altıncı")
        self.assertEqual(num2words(7, lang="tr", ordinal=True), "yedinci")
        self.assertEqual(num2words(8, lang="tr", ordinal=True), "sekizinci")
        self.assertEqual(num2words(9, lang="tr", ordinal=True), "dokuzuncu")
        self.assertEqual(num2words(10, lang="tr", ordinal=True), "onuncu")
        self.assertEqual(num2words(11, lang="tr", ordinal=True), "onbirinci")
        self.assertEqual(num2words(12, lang="tr", ordinal=True), "onikinci")
        self.assertEqual(num2words(13, lang="tr", ordinal=True), "onüçüncü")
        self.assertEqual(num2words(14, lang="tr", ordinal=True), "ondördüncü")
        self.assertEqual(num2words(15, lang="tr", ordinal=True), "onbeşinci")
        self.assertEqual(num2words(16, lang="tr", ordinal=True), "onaltıncı")
        self.assertEqual(num2words(17, lang="tr", ordinal=True), "onyedinci")
        self.assertEqual(num2words(18, lang="tr", ordinal=True), "onsekizinci")
        self.assertEqual(num2words(19, lang="tr", ordinal=True), "ondokuzuncu")
        self.assertEqual(num2words(20, lang="tr", ordinal=True), "yirminci")
        self.assertEqual(num2words(21, lang="tr", ordinal=True), "yirmibirinci")
        self.assertEqual(num2words(22, lang="tr", ordinal=True), "yirmiikinci")
        self.assertEqual(num2words(25, lang="tr", ordinal=True), "yirmibeşinci")
        self.assertEqual(num2words(30, lang="tr", ordinal=True), "otuzuncu")
        self.assertEqual(num2words(40, lang="tr", ordinal=True), "kırkıncı")
        self.assertEqual(num2words(50, lang="tr", ordinal=True), "ellinci")
        self.assertEqual(num2words(60, lang="tr", ordinal=True), "altmışıncı")
        self.assertEqual(num2words(70, lang="tr", ordinal=True), "yetmişinci")
        self.assertEqual(num2words(80, lang="tr", ordinal=True), "sekseninci")
        self.assertEqual(num2words(90, lang="tr", ordinal=True), "doksanıncı")
        self.assertEqual(num2words(100, lang="tr", ordinal=True), "yüzüncü")
        self.assertEqual(num2words(101, lang="tr", ordinal=True), "yüzbirinci")
        self.assertEqual(num2words(200, lang="tr", ordinal=True), "ikiyüzüncü")
        self.assertEqual(num2words(500, lang="tr", ordinal=True), "beşyüzüncü")
        self.assertEqual(num2words(1000, lang="tr", ordinal=True), "bininci")
        self.assertEqual(num2words(1001, lang="tr", ordinal=True), "binbirinci")
        self.assertEqual(num2words(10000, lang="tr", ordinal=True), "onbininci")

    def test_currency(self):
        """Test currency conversion."""
        self.assertEqual(
            num2words(0, lang="tr", to="currency", currency="TRY"), "sıfırlira"
        )
        self.assertEqual(
            num2words(0.01, lang="tr", to="currency", currency="TRY"),
            "sıfır lira, bir kuruş",
        )
        self.assertEqual(
            num2words(0.5, lang="tr", to="currency", currency="TRY"),
            "sıfır lira, elli kuruş",
        )
        self.assertEqual(
            num2words(1, lang="tr", to="currency", currency="TRY"), "birlira"
        )
        self.assertEqual(
            num2words(1.5, lang="tr", to="currency", currency="TRY"),
            "bir lira, elli kuruş",
        )
        self.assertEqual(
            num2words(0, lang="tr", to="currency", currency="EUR"), "sıfırlira"
        )
        self.assertEqual(
            num2words(0.01, lang="tr", to="currency", currency="EUR"),
            "sıfır avro, bir sent",
        )
        self.assertEqual(
            num2words(0.5, lang="tr", to="currency", currency="EUR"),
            "sıfır avro, elli sent",
        )
        self.assertEqual(
            num2words(1, lang="tr", to="currency", currency="EUR"), "birlira"
        )
        self.assertEqual(
            num2words(1.5, lang="tr", to="currency", currency="EUR"),
            "bir avro, elli sent",
        )
        self.assertEqual(
            num2words(0, lang="tr", to="currency", currency="USD"), "sıfırlira"
        )
        self.assertEqual(
            num2words(0.01, lang="tr", to="currency", currency="USD"),
            "sıfır dolar, bir sent",
        )
        self.assertEqual(
            num2words(0.5, lang="tr", to="currency", currency="USD"),
            "sıfır dolar, elli sent",
        )
        self.assertEqual(
            num2words(1, lang="tr", to="currency", currency="USD"), "birlira"
        )
        self.assertEqual(
            num2words(1.5, lang="tr", to="currency", currency="USD"),
            "bir dolar, elli sent",
        )

    def test_year(self):
        """Test year conversion."""
        self.assertEqual(num2words(1000, lang="tr", to="year"), "bin")
        self.assertEqual(num2words(1066, lang="tr", to="year"), "binaltmışaltı")
        self.assertEqual(num2words(1492, lang="tr", to="year"), "bindörtyüzdoksaniki")
        self.assertEqual(num2words(1776, lang="tr", to="year"), "binyediyüzyetmişaltı")
        self.assertEqual(num2words(1800, lang="tr", to="year"), "binsekizyüz")
        self.assertEqual(num2words(1900, lang="tr", to="year"), "bindokuzyüz")
        self.assertEqual(num2words(1984, lang="tr", to="year"), "bindokuzyüzseksendört")
        self.assertEqual(
            num2words(1999, lang="tr", to="year"), "bindokuzyüzdoksandokuz"
        )
        self.assertEqual(num2words(2000, lang="tr", to="year"), "ikibin")
        self.assertEqual(num2words(2001, lang="tr", to="year"), "ikibinbir")
        self.assertEqual(num2words(2010, lang="tr", to="year"), "ikibinon")
        self.assertEqual(num2words(2020, lang="tr", to="year"), "ikibinyirmi")
        self.assertEqual(num2words(2024, lang="tr", to="year"), "ikibinyirmidört")
        self.assertEqual(num2words(2100, lang="tr", to="year"), "ikibinyüz")

    def test_string_input(self):
        """Test string input conversion."""
        self.assertEqual(num2words("0", lang="tr"), "sıfır")
        self.assertEqual(num2words("1", lang="tr"), "bir")
        self.assertEqual(num2words("10", lang="tr"), "on")
        self.assertEqual(num2words("100", lang="tr"), "yüz")
        self.assertEqual(num2words("1000", lang="tr"), "bin")
        self.assertEqual(num2words("10000", lang="tr"), "onbin")
        self.assertEqual(num2words("100000", lang="tr"), "yüzbin")
        self.assertEqual(num2words("1000000", lang="tr"), "birmilyon")

    def test_edge_cases(self):
        """Test edge cases and special conditions."""
        # Test zero
        self.assertEqual(num2words(0, lang="tr"), "sıfır")

        # Test that the converter handles various input types
        self.assertEqual(num2words(100, lang="tr"), num2words("100", lang="tr"))
        self.assertEqual(num2words(1000, lang="tr"), num2words("1000", lang="tr"))

    def test_converter_methods(self):
        """Test direct converter methods for better coverage."""
        from num2words2.lang_TR import Num2Word_TR

        converter = Num2Word_TR()

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
