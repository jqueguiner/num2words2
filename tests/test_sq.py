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
from num2words.lang_SQ import Num2Word_SQ


class Num2WordsSQTest(TestCase):
    """Test suite for Albanian number to words converter."""

    def test_basic_cardinal_numbers(self):
        """Test basic cardinal number conversion."""
        # Single digits
        self.assertEqual(num2words(0, lang="sq"), "zero")
        self.assertEqual(num2words(1, lang="sq"), "një")
        self.assertEqual(num2words(2, lang="sq"), "dy")
        self.assertEqual(num2words(3, lang="sq"), "tre")
        self.assertEqual(num2words(4, lang="sq"), "katër")
        self.assertEqual(num2words(5, lang="sq"), "pesë")
        self.assertEqual(num2words(6, lang="sq"), "gjashtë")
        self.assertEqual(num2words(7, lang="sq"), "shtatë")
        self.assertEqual(num2words(8, lang="sq"), "tetë")
        self.assertEqual(num2words(9, lang="sq"), "nëntë")

        # Ten and teens
        self.assertEqual(num2words(10, lang="sq"), "dhjetë")
        self.assertEqual(num2words(11, lang="sq"), "njëmbëdhjetë")
        self.assertEqual(num2words(12, lang="sq"), "dymbëdhjetë")
        self.assertEqual(num2words(13, lang="sq"), "trembëdhjetë")
        self.assertEqual(num2words(14, lang="sq"), "katërmbëdhjetë")
        self.assertEqual(num2words(15, lang="sq"), "pesëmbëdhjetë")
        self.assertEqual(num2words(16, lang="sq"), "gjashtëmbëdhjetë")
        self.assertEqual(num2words(17, lang="sq"), "shtatëmbëdhjetë")
        self.assertEqual(num2words(18, lang="sq"), "tetëmbëdhjetë")
        self.assertEqual(num2words(19, lang="sq"), "nëntëmbëdhjetë")

        # Tens
        self.assertEqual(num2words(20, lang="sq"), "njëzet")
        self.assertEqual(num2words(21, lang="sq"), "njëzet e një")
        self.assertEqual(num2words(30, lang="sq"), "tridhjetë")
        self.assertEqual(num2words(35, lang="sq"), "tridhjetë e pesë")
        self.assertEqual(num2words(40, lang="sq"), "dyzet")
        self.assertEqual(num2words(50, lang="sq"), "pesëdhjetë")
        self.assertEqual(num2words(60, lang="sq"), "gjashtëdhjetë")
        self.assertEqual(num2words(70, lang="sq"), "shtatëdhjetë")
        self.assertEqual(num2words(80, lang="sq"), "tetëdhjetë")
        self.assertEqual(num2words(90, lang="sq"), "nëntëdhjetë")
        self.assertEqual(num2words(99, lang="sq"), "nëntëdhjetë e nëntë")

        # Hundreds
        self.assertEqual(num2words(100, lang="sq"), "një qind")
        self.assertEqual(num2words(101, lang="sq"), "një qind e një")
        self.assertEqual(num2words(110, lang="sq"), "një qind e dhjetë")
        self.assertEqual(num2words(111, lang="sq"), "një qind e njëmbëdhjetë")
        self.assertEqual(num2words(125, lang="sq"), "një qind e njëzet e pesë")
        self.assertEqual(num2words(200, lang="sq"), "dy qind")
        self.assertEqual(num2words(300, lang="sq"), "tre qind")
        self.assertEqual(num2words(999, lang="sq"), "nëntë qind e nëntëdhjetë e nëntë")

    def test_large_cardinal_numbers(self):
        """Test large cardinal number conversion."""
        # Thousands
        self.assertEqual(num2words(1000, lang="sq"), "një mijë")
        self.assertEqual(num2words(1001, lang="sq"), "një mijë e një")
        self.assertEqual(num2words(1111, lang="sq"), "një mijë e një qind e njëmbëdhjetë")
        self.assertEqual(num2words(2000, lang="sq"), "dy mijë")
        self.assertEqual(num2words(10000, lang="sq"), "dhjetë mijë")
        self.assertEqual(num2words(100000, lang="sq"), "një qind mijë")
        self.assertEqual(num2words(999999, lang="sq"), "nëntë qind e nëntëdhjetë e nëntë mijë e nëntë qind e nëntëdhjetë e nëntë")

        # Millions
        self.assertEqual(num2words(1000000, lang="sq"), "një milion")
        self.assertEqual(num2words(2000000, lang="sq"), "dy milion")
        self.assertEqual(num2words(1000001, lang="sq"), "një milion e një")
        self.assertEqual(num2words(1234567, lang="sq"), "një milion e dy qind e tridhjetë e katër mijë e pesë qind e gjashtëdhjetë e shtatë")

        # Billions
        self.assertEqual(num2words(1000000000, lang="sq"), "një miliard")
        self.assertEqual(num2words(2000000000, lang="sq"), "dy miliard")
        self.assertEqual(num2words(1000000001, lang="sq"), "një miliard e një")

    def test_ordinal_numbers(self):
        """Test ordinal number conversion."""
        # Basic ordinals
        self.assertEqual(num2words(1, lang="sq", to="ordinal"), "i pari")
        self.assertEqual(num2words(2, lang="sq", to="ordinal"), "i dyti")
        self.assertEqual(num2words(3, lang="sq", to="ordinal"), "i treti")
        self.assertEqual(num2words(4, lang="sq", to="ordinal"), "i katërti")
        self.assertEqual(num2words(5, lang="sq", to="ordinal"), "i pesti")
        self.assertEqual(num2words(6, lang="sq", to="ordinal"), "i gjashti")
        self.assertEqual(num2words(7, lang="sq", to="ordinal"), "i shtati")
        self.assertEqual(num2words(8, lang="sq", to="ordinal"), "i teti")
        self.assertEqual(num2words(9, lang="sq", to="ordinal"), "i nënti")
        self.assertEqual(num2words(10, lang="sq", to="ordinal"), "i dhjeti")

        # Larger ordinals
        self.assertEqual(num2words(11, lang="sq", to="ordinal"), "i njëmbëdhjetë")
        self.assertEqual(num2words(20, lang="sq", to="ordinal"), "i njezeti")
        self.assertEqual(num2words(21, lang="sq", to="ordinal"), "i njëzet e një")
        self.assertEqual(num2words(100, lang="sq", to="ordinal"), "i një qindi")
        self.assertEqual(num2words(101, lang="sq", to="ordinal"), "i një qind e një")
        self.assertEqual(num2words(1000, lang="sq", to="ordinal"), "i një mijti")

    def test_ordinal_num_format(self):
        """Test ordinal number with suffix format."""
        self.assertEqual(num2words(1, lang="sq", to="ordinal_num"), "1-shi")
        self.assertEqual(num2words(2, lang="sq", to="ordinal_num"), "2-ri")
        self.assertEqual(num2words(3, lang="sq", to="ordinal_num"), "3-ti")
        self.assertEqual(num2words(10, lang="sq", to="ordinal_num"), "10-ti")
        self.assertEqual(num2words(21, lang="sq", to="ordinal_num"), "21-shi")
        self.assertEqual(num2words(100, lang="sq", to="ordinal_num"), "100-ti")

    def test_currency_basic(self):
        """Test basic currency conversion."""
        # Albanian Lek
        self.assertEqual(num2words(1, lang="sq", to="currency", currency="ALL"), "një lek")
        self.assertEqual(num2words(2, lang="sq", to="currency", currency="ALL"), "dy lekë")
        self.assertEqual(num2words(100, lang="sq", to="currency", currency="ALL"), "një qind lekë")

        # Euro
        self.assertEqual(num2words(1, lang="sq", to="currency", currency="EUR"), "një euro")
        self.assertEqual(num2words(2, lang="sq", to="currency", currency="EUR"), "dy euro")
        self.assertEqual(num2words(100, lang="sq", to="currency", currency="EUR"), "një qind euro")

        # US Dollar
        self.assertEqual(num2words(1, lang="sq", to="currency", currency="USD"), "një dollar")
        self.assertEqual(num2words(2, lang="sq", to="currency", currency="USD"), "dy dollarë")
        self.assertEqual(num2words(100, lang="sq", to="currency", currency="USD"), "një qind dollarë")

    def test_currency_with_cents(self):
        """Test currency conversion with fractional values."""
        # Basic fractional currency
        self.assertEqual(
            num2words(1.50, lang="sq", to="currency", currency="ALL"),
            "një lek, pesëdhjetë qindarkë"
        )
        self.assertEqual(
            num2words(2.25, lang="sq", to="currency", currency="EUR"),
            "dy euro, njëzet e pesë centë"
        )
        self.assertEqual(
            num2words(100.99, lang="sq", to="currency", currency="USD"),
            "një qind dollarë, nëntëdhjetë e nëntë centë"
        )

        # Only fractional part
        self.assertEqual(
            num2words(0.50, lang="sq", to="currency", currency="ALL"),
            "pesëdhjetë qindarkë"
        )
        self.assertEqual(
            num2words(0.75, lang="sq", to="currency", currency="EUR"),
            "shtatëdhjetë e pesë centë"
        )

    def test_currency_no_cents(self):
        """Test currency without cents."""
        self.assertEqual(
            num2words(100, lang="sq", to="currency", currency="ALL", cents=False),
            "një qind lekë"
        )
        self.assertEqual(
            num2words(50.75, lang="sq", to="currency", currency="EUR", cents=False),
            "pesëdhjetë euro"
        )

    def test_negative_numbers(self):
        """Test negative number conversion."""
        self.assertEqual(num2words(-1, lang="sq"), "minus një")
        self.assertEqual(num2words(-10, lang="sq"), "minus dhjetë")
        self.assertEqual(num2words(-100, lang="sq"), "minus një qind")
        self.assertEqual(num2words(-1000, lang="sq"), "minus një mijë")

    def test_decimal_numbers(self):
        """Test decimal number conversion."""
        self.assertEqual(num2words(1.5, lang="sq"), "një presje pesë")
        self.assertEqual(num2words(10.25, lang="sq"), "dhjetë presje dy pesë")
        self.assertEqual(num2words(0.5, lang="sq"), "zero presje pesë")
        self.assertEqual(num2words(-1.5, lang="sq"), "minus një presje pesë")

    def test_year_conversion(self):
        """Test year conversion."""
        self.assertEqual(num2words(2000, lang="sq", to="year"), "dy mijë")
        self.assertEqual(num2words(2023, lang="sq", to="year"), "dy mijë e njëzet e tre")
        self.assertEqual(num2words(1999, lang="sq", to="year"), "një mijë e nëntë qind e nëntëdhjetë e nëntë")

    def test_edge_cases(self):
        """Test edge cases."""
        # Zero
        self.assertEqual(num2words(0, lang="sq"), "zero")
        self.assertEqual(num2words(0, lang="sq", to="ordinal"), "i zeroi")

        # Large numbers edge cases
        converter = Num2Word_SQ()
        
        # Test very large numbers (within MAXVAL limits)
        result = converter.to_cardinal(10**14)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(len(result) > 0)

        # Test string to number conversion
        self.assertEqual(converter.str_to_number("123"), 123)

    def test_pluralization_rules(self):
        """Test Albanian pluralization rules."""
        converter = Num2Word_SQ()

        # Test currency pluralization
        self.assertEqual(converter.pluralize(1, ("lek", "lekë")), "lek")
        self.assertEqual(converter.pluralize(2, ("lek", "lekë")), "lekë")
        self.assertEqual(converter.pluralize(5, ("lek", "lekë")), "lekë")
        self.assertEqual(converter.pluralize(100, ("lek", "lekë")), "lekë")

        # Test with single form
        self.assertEqual(converter.pluralize(1, ("euro",)), "euro")
        self.assertEqual(converter.pluralize(5, ("euro",)), "euro")

        # Test empty forms
        self.assertEqual(converter.pluralize(5, []), "")

    def test_merge_functionality(self):
        """Test the merge method functionality."""
        converter = Num2Word_SQ()

        # Test basic merging
        result = converter.merge(("një qind", 100), ("një", 1))
        self.assertEqual(result[0], "një qind e një")
        self.assertEqual(result[1], 101)

        result = converter.merge(("dy mijë", 2000), ("tre qind", 300))
        self.assertEqual(result[0], "dy mijë e tre qind")
        self.assertEqual(result[1], 2300)

    def test_special_currency_forms(self):
        """Test special currency forms and edge cases."""
        # Test negative currency
        self.assertEqual(
            num2words(-1.50, lang="sq", to="currency", currency="ALL"),
            "minus një lek, pesëdhjetë qindarkë"
        )

        # Test unknown currency fallback
        converter = Num2Word_SQ()
        result = converter.to_currency(100, "XXX")
        self.assertTrue(isinstance(result, str))

    def test_compound_numbers_grammar(self):
        """Test proper Albanian grammar in compound numbers."""
        # Test that compound numbers use proper connectors
        self.assertEqual(num2words(21, lang="sq"), "njëzet e një")
        self.assertEqual(num2words(101, lang="sq"), "një qind e një")
        self.assertEqual(num2words(1001, lang="sq"), "një mijë e një")
        
        # Test without connectors where appropriate
        self.assertEqual(num2words(20, lang="sq"), "njëzet")
        self.assertEqual(num2words(100, lang="sq"), "një qind")
        self.assertEqual(num2words(1000, lang="sq"), "një mijë")

    def test_specific_albanian_numbers(self):
        """Test specific Albanian number patterns."""
        # Numbers that might have special forms in Albanian
        self.assertEqual(num2words(22, lang="sq"), "njëzet e dy")
        self.assertEqual(num2words(33, lang="sq"), "tridhjetë e tre")
        self.assertEqual(num2words(44, lang="sq"), "dyzet e katër")
        self.assertEqual(num2words(77, lang="sq"), "shtatëdhjetë e shtatë")
        
        # Complex numbers
        self.assertEqual(num2words(1234, lang="sq"), "një mijë e dy qind e tridhjetë e katër")
        self.assertEqual(num2words(5678, lang="sq"), "pesë mijë e gjashtë qind e shtatëdhjetë e tetë")