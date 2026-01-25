# -*- coding: utf-8 -*-
# Additional coverage tests for Malay language

from unittest import TestCase

from num2words2 import num2words
from num2words2.lang_MS import Num2Word_MS


class Num2WordsMSCoverageTest(TestCase):
    """Additional tests to achieve 100% coverage for Malay."""

    def test_setup_method(self):
        """Test the _setup method is called."""
        converter = Num2Word_MS()
        # This implicitly tests _setup through __init__
        self.assertIsNotNone(converter.negword)

    def test_merge_method(self):
        """Test the merge method - not implemented in Malay."""
        converter = Num2Word_MS()
        # Malay doesn't implement merge, it raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            converter.merge("satu", "ratus")

    def test_to_cardinal_string_input(self):
        """Test to_cardinal with string input."""
        self.assertEqual(num2words("42", lang="ms"), "empat puluh dua")
        self.assertEqual(num2words("0", lang="ms"), "kosong")

    def test_to_cardinal_exception_handling(self):
        """Test to_cardinal exception handling."""
        converter = Num2Word_MS()
        # Test with float that triggers exception path
        result = converter.to_cardinal(3.14)
        self.assertEqual(result, "tiga")

    def test_to_ordinal_string_input(self):
        """Test to_ordinal with string input."""
        self.assertEqual(num2words("5", lang="ms", to="ordinal"), "kelima")

    def test_to_ordinal_exception_handling(self):
        """Test to_ordinal exception handling."""
        converter = Num2Word_MS()
        result = converter.to_ordinal(3.14)
        self.assertEqual(result, "ketiga")

    def test_to_ordinal_num_string_input(self):
        """Test to_ordinal_num with string input."""
        self.assertEqual(num2words("15", lang="ms", to="ordinal_num"), "ke-15")

    def test_to_ordinal_num_exception_handling(self):
        """Test to_ordinal_num exception handling."""
        converter = Num2Word_MS()
        result = converter.to_ordinal_num(3.14)
        self.assertEqual(result, "ke-3.14")

    def test_to_currency_not_implemented(self):
        """Test currency with unsupported currency code."""
        # This should raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            num2words(100, lang="ms", to="currency", currency="XXX")

    def test_to_currency_negative(self):
        """Test negative currency amounts."""
        self.assertEqual(
            num2words(-50.50, lang="ms", to="currency", currency="MYR"),
            "negatif lima puluh ringgit lima puluh sen",
        )

    def test_to_currency_exception_handling(self):
        """Test to_currency exception handling."""
        converter = Num2Word_MS()
        # Test with invalid input that triggers exception
        result = converter.to_currency("invalid", "MYR")
        self.assertEqual(result, "invalid MYR")

    def test_to_year_small_numbers(self):
        """Test year conversion for numbers less than 1000."""
        self.assertEqual(
            num2words(999, lang="ms", to="year"),
            "sembilan ratus sembilan puluh sembilan",
        )
        self.assertEqual(num2words(500, lang="ms", to="year"), "lima ratus")
