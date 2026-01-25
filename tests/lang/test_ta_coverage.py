# -*- coding: utf-8 -*-
# Additional coverage tests for Tamil language

from unittest import TestCase

from num2words2 import num2words
from num2words2.lang_TA import Num2Word_TA


class Num2WordsTACoverageTest(TestCase):
    """Additional tests to achieve 100% coverage for Tamil."""

    def test_setup_method(self):
        """Test the _setup method is called."""
        converter = Num2Word_TA()
        # This implicitly tests _setup through __init__
        self.assertIsNotNone(converter.negword)

    def test_direct_int_to_word_zero(self):
        """Test _int_to_word directly with zero."""
        converter = Num2Word_TA()
        result = converter._int_to_word(0)
        self.assertEqual(result, "பூஜ்ஜியம்")

    def test_to_cardinal_string_input(self):
        """Test to_cardinal with string input."""
        self.assertEqual(num2words("42", lang="ta"), "நாற்பது இரண்டு")
        self.assertEqual(num2words("0", lang="ta"), "பூஜ்ஜியம்")

    def test_to_cardinal_exception_handling(self):
        """Test to_cardinal exception handling."""
        converter = Num2Word_TA()
        # Test with float that triggers exception path
        result = converter.to_cardinal(3.14)
        self.assertEqual(result, "மூன்று")

    def test_to_ordinal_string_input(self):
        """Test to_ordinal with string input."""
        self.assertEqual(num2words("5", lang="ta", to="ordinal"), "ஐந்தாம்")

    def test_to_ordinal_exception_handling(self):
        """Test to_ordinal exception handling."""
        converter = Num2Word_TA()
        result = converter.to_ordinal(3.14)
        self.assertEqual(result, "மூன்றாம்")

    def test_to_ordinal_num_string_input(self):
        """Test to_ordinal_num with string input."""
        self.assertEqual(num2words("15", lang="ta", to="ordinal_num"), "15-வது")

    def test_to_ordinal_num_exception_handling(self):
        """Test to_ordinal_num exception handling."""
        converter = Num2Word_TA()
        result = converter.to_ordinal_num(3.14)
        self.assertEqual(result, "3.14-வது")

    def test_to_currency_not_implemented(self):
        """Test currency with unsupported currency code."""
        # This should raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            num2words(100, lang="ta", to="currency", currency="XXX")

    def test_to_currency_negative(self):
        """Test negative currency amounts."""
        self.assertEqual(
            num2words(-50.50, lang="ta", to="currency", currency="INR"),
            "கழித்தல் ஐம்பது ரூபாய் ஐம்பது பைசா",
        )

    def test_to_currency_exception_handling(self):
        """Test to_currency exception handling."""
        converter = Num2Word_TA()
        # Test with invalid input that triggers exception
        result = converter.to_currency("invalid", "INR")
        self.assertEqual(result, "invalid INR")

    def test_to_year_small_numbers(self):
        """Test year conversion for numbers less than 1000."""
        self.assertEqual(
            num2words(999, lang="ta", to="year"), "தொள்ளாயிரம் தொண்ணூறு ஒன்பது"
        )
        self.assertEqual(num2words(500, lang="ta", to="year"), "ஐநூறு")

    def test_to_year_special_cases(self):
        """Test year conversion special cases."""
        # Test year 1000 exactly
        self.assertEqual(num2words(1000, lang="ta", to="year"), "ஆயிரத்து")
        # Test year 2000 exactly
        self.assertEqual(num2words(2000, lang="ta", to="year"), "இரண்டு ஆயிரத்து")
