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

from num2words2 import num2words_sentence


class Num2WordsSentenceTest(TestCase):
    """Test cases for the num2words_sentence function."""

    def test_basic_sentence(self):
        """Test basic sentence with single number."""
        sentence = "I just bought 6 apples"
        expected = "I just bought six apples"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_multiple_numbers(self):
        """Test sentence with multiple numbers."""
        sentence = "I have 3 cats, 2 dogs, and 5 fish"
        expected = "I have three cats, two dogs, and five fish"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_decimal_numbers(self):
        """Test sentence with decimal numbers."""
        sentence = "The price is 19.99 dollars"
        expected = "The price is nineteen point nine nine dollars"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_large_numbers(self):
        """Test sentence with large numbers."""
        sentence = "The population is 1000000 people"
        expected = "The population is one million people"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_negative_numbers(self):
        """Test sentence with negative numbers."""
        sentence = "The temperature is -5 degrees"
        expected = "The temperature is minus five degrees"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_number_at_start(self):
        """Test sentence starting with a number."""
        sentence = "100 years ago, things were different"
        expected = "One hundred years ago, things were different"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_number_after_period(self):
        """Test number after period gets capitalized."""
        sentence = "First item done. 50 items remain"
        expected = "First item done. Fifty items remain"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_spanish_language(self):
        """Test conversion with Spanish language."""
        sentence = "Tengo 10 manzanas"
        expected = "Tengo diez manzanas"
        self.assertEqual(num2words_sentence(sentence, lang="es"), expected)

    def test_french_language(self):
        """Test conversion with French language."""
        sentence = "J'ai 20 euros"
        expected = "J'ai vingt euros"
        self.assertEqual(num2words_sentence(sentence, lang="fr"), expected)

    def test_zero(self):
        """Test conversion of zero."""
        sentence = "There are 0 errors"
        expected = "There are zero errors"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_mixed_formats(self):
        """Test sentence with various number formats."""
        sentence = "We have 1000 users, -3.14 balance, and 42 tickets"
        expected = "We have one thousand users, minus three point one four balance, and forty-two tickets"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_no_numbers(self):
        """Test sentence without any numbers."""
        sentence = "This is a sentence without numbers"
        expected = "This is a sentence without numbers"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_ordinal_conversion(self):
        """Test ordinal conversion parameter."""
        sentence = "He finished in 1 place"
        expected = "He finished in first place"
        self.assertEqual(num2words_sentence(sentence, to="ordinal"), expected)

    def test_year_format(self):
        """Test year format with multiple numbers."""
        sentence = "The year 2024 marks 50 years since 1974"
        expected = "The year two thousand and twenty-four marks fifty years since one thousand, nine hundred and seventy-four"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_preserve_non_numeric_text(self):
        """Test that non-numeric text is preserved exactly."""
        sentence = "Test123word contains 456 numbers"
        # Note: This should only convert standalone numbers, not those within words
        expected = "Test123word contains four hundred and fifty-six numbers"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_multiple_decimal_places(self):
        """Test numbers with multiple decimal places."""
        sentence = "Pi is approximately 3.14159"
        expected = "Pi is approximately three point one four one five nine"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_capitalization_after_exclamation(self):
        """Test capitalization after exclamation mark."""
        sentence = "Amazing! 10 people came"
        expected = "Amazing! Ten people came"
        self.assertEqual(num2words_sentence(sentence), expected)

    def test_capitalization_after_question(self):
        """Test capitalization after question mark."""
        sentence = "How many? 25 exactly"
        expected = "How many? Twenty-five exactly"
        self.assertEqual(num2words_sentence(sentence), expected)
