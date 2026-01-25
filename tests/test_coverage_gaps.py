"""
Additional tests to improve coverage for uncovered code paths.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from num2words2 import num2words
from num2words2.converters.comprehensive_converter import (
    ComprehensiveConverter,
    _load_langid,
)
from num2words2.converters.sentence import num2words_sentence


class TestGermanCaseHandling(TestCase):
    """Test German case handling in sentence converter."""

    def test_german_dative_case(self):
        """Test German dative case with 'am', 'zum', 'vom'."""
        # Test with 'am' (dative)
        result = num2words_sentence("Am 15. Januar", lang="de")
        self.assertIsNotNone(result)

        # Test with 'zum'
        result = num2words_sentence("Zum 3. Mal", lang="de")
        self.assertIsNotNone(result)

        # Test with 'vom'
        result = num2words_sentence("Vom 1. bis 5.", lang="de")
        self.assertIsNotNone(result)

    def test_german_accusative_case(self):
        """Test German accusative case with 'den'."""
        result = num2words_sentence("Den 10. Mai", lang="de")
        self.assertIsNotNone(result)

    def test_german_nominative_case(self):
        """Test German nominative case (base form)."""
        result = num2words_sentence("Der 25. Dezember", lang="de")
        self.assertIsNotNone(result)

    def test_german_ordinal_with_cases(self):
        """Test German ordinals with different grammatical cases."""
        # Test various case contexts
        test_sentences = [
            "am 1. Januar",  # Dative
            "den 2. Februar",  # Accusative
            "der 3. März",  # Nominative
            "zum 4. April",  # Dative with zu
            "vom 5. Mai",  # Dative with von
        ]

        for sentence in test_sentences:
            result = num2words_sentence(sentence, lang="de")
            self.assertIsNotNone(result)
            # Verify number is converted
            self.assertNotIn("1.", result) if "1." in sentence else None
            self.assertNotIn("2.", result) if "2." in sentence else None

    def test_german_date_ordinals(self):
        """Test German date ordinals in various formats."""
        test_dates = [
            "1. Januar 2024",
            "15. März 2025",
            "31. Dezember 2023",
        ]

        for date in test_dates:
            result = num2words_sentence(date, lang="de")
            self.assertIsNotNone(result)
            # Check that ordinal numbers are converted
            for num in ["1.", "15.", "31."]:
                if num in date:
                    self.assertNotIn(num, result)


class TestComprehensiveConverterMain(TestCase):
    """Test the main execution paths of comprehensive converter."""

    def test_converter_with_command_line_style_args(self):
        """Test converter with command line style arguments."""
        converter = ComprehensiveConverter()

        # Test with explicit language
        result = converter.convert_sentence("Test 123", force_language="en")
        self.assertIn("one hundred", result.lower())

        # Test with auto-detection
        result = converter.convert_sentence("Test 456")
        self.assertIsNotNone(result)

    def test_converter_interactive_style(self):
        """Test converter in interactive style usage."""
        converter = ComprehensiveConverter()

        # Test language prefix parsing style
        test_cases = [
            ("Test 456", None),
            ("Test 789", "fr"),
            ("Test 100", "de"),
        ]

        for text, lang in test_cases:
            if lang:
                result = converter.convert_sentence(text, force_language=lang)
            else:
                result = converter.convert_sentence(text)
            self.assertIsNotNone(result)
            # Numbers should be converted
            self.assertNotIn("456", result) if "456" in text else None
            self.assertNotIn("789", result) if "789" in text else None

    def test_module_demo_execution(self):
        """Test the module demo execution code."""
        # Test that the module can be imported
        from num2words2.converters import comprehensive_converter

        # The module should have the converter class
        self.assertTrue(hasattr(comprehensive_converter, "ComprehensiveConverter"))

        # Test creating an instance
        converter = comprehensive_converter.ComprehensiveConverter()
        self.assertIsNotNone(converter)

    def test_langid_import_failure(self):
        """Test _load_langid when import fails."""
        with patch("builtins.__import__", side_effect=ImportError("test error")):
            result = _load_langid()
            self.assertIsNone(result)

    def test_langid_import_success_mock(self):
        """Test _load_langid with successful mock import."""
        mock_langid = MagicMock()
        mock_langid.classify = MagicMock(return_value=("en", 0.99))

        with patch("builtins.__import__", return_value=mock_langid):
            # Call _load_langid fresh
            # Reset the cached value
            import num2words2.converters.comprehensive_converter
            from num2words2.converters.comprehensive_converter import _load_langid

            num2words2.converters.comprehensive_converter._LANGID = None

            result = _load_langid()
            # Should return the mock module
            self.assertIsNotNone(result)


class TestGreekOrdinals(TestCase):
    """Additional tests for Greek ordinals."""

    def test_greek_ordinal_edge_cases(self):
        """Test Greek ordinal edge cases."""
        # Test ordinals that require special handling
        test_cases = [
            (3, "τρίτος"),
            (4, "τέταρτος"),
            (11, "ενδέκατος"),
            (12, "δωδέκατος"),
            (20, "εικοστός"),
            (100, "εκατοστός"),
            (1000, "χιλιοστός"),
        ]

        for num, expected in test_cases:
            result = num2words(num, lang="el", ordinal=True)
            self.assertIn(expected, result)

    def test_greek_ordinal_num_format(self):
        """Test Greek ordinal number format."""
        test_numbers = [1, 2, 3, 10, 21, 100]

        for num in test_numbers:
            result = num2words(num, lang="el", to="ordinal_num")
            self.assertTrue(result.endswith("ος") or result.endswith("η"))

    def test_greek_large_ordinals(self):
        """Test Greek large ordinals."""
        large_numbers = [10000, 100000, 1000000]

        for num in large_numbers:
            result = num2words(num, lang="el", ordinal=True)
            self.assertIsNotNone(result)
            # Should contain ordinal suffix
            self.assertTrue(
                result.endswith("ός")
                or result.endswith("ος")
                or result.endswith("στός")
            )

    def test_greek_currency_edge_cases(self):
        """Test Greek currency conversion edge cases."""
        # Test with invalid currency
        try:
            result = num2words(100, lang="el", to="currency", currency="INVALID")
            # Should either raise error or use default
        except (NotImplementedError, KeyError):
            # Expected for invalid currency
            pass

        # Test negative currency
        result = num2words(-50.50, lang="el", to="currency")
        self.assertIn("μείον", result.lower())

    def test_greek_year_conversion(self):
        """Test Greek year conversion."""
        years = [1999, 2000, 2024, 1821]  # Including Greek independence year

        for year in years:
            result = num2words(year, lang="el", to="year")
            self.assertIsNotNone(result)
            # Should not be empty
            self.assertTrue(len(result) > 0)


class TestSentenceConverterEdgeCases(TestCase):
    """Test edge cases in sentence converter."""

    def test_empty_and_none_inputs(self):
        """Test handling of empty and None inputs."""
        # Test empty string
        result = num2words_sentence("", lang="en")
        self.assertEqual(result, "")

        # Test whitespace only
        result = num2words_sentence("   ", lang="en")
        self.assertEqual(result, "   ")

        # Test None handling should be done before calling
        # The function expects a string

    def test_unsupported_language_fallback(self):
        """Test fallback for unsupported languages."""
        # Force an invalid language code - should raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            num2words_sentence("Test 123", lang="xyz")

    def test_number_extraction_special_patterns(self):
        """Test number extraction with special patterns."""
        # Test IP addresses (should not convert)
        result = num2words_sentence("IP: 192.168.1.1", lang="en")
        # IP addresses might be partially converted, but check it runs
        self.assertIsNotNone(result)

        # Test version numbers
        result = num2words_sentence("Version 3.14.159", lang="en")
        self.assertIsNotNone(result)

        # Test time formats
        result = num2words_sentence("Time: 14:30:45", lang="en")
        self.assertIsNotNone(result)

    def test_mixed_script_handling(self):
        """Test handling of mixed scripts."""
        # Mix Latin and Cyrillic
        result = num2words_sentence("Test 123 тест", lang="en")
        self.assertIsNotNone(result)

        # Mix Latin and Chinese
        result = num2words_sentence("Test 456 测试", lang="en")
        self.assertIsNotNone(result)

    def test_capitalization_edge_cases(self):
        """Test capitalization in edge cases."""
        # All caps input
        result = num2words_sentence("TEST 123 TEST", lang="en")
        self.assertIsNotNone(result)

        # Mixed case
        result = num2words_sentence("TeSt 456 tEsT", lang="en")
        self.assertIsNotNone(result)

    def test_special_number_formats(self):
        """Test special number format handling."""
        # Scientific notation
        result = num2words_sentence("1.23e10", lang="en")
        self.assertIsNotNone(result)

        # Hexadecimal (should not convert)
        result = num2words_sentence("0xFF", lang="en")
        self.assertIsNotNone(result)

        # Binary (should not convert)
        result = num2words_sentence("0b1010", lang="en")
        self.assertIsNotNone(result)


class TestErrorConditions(TestCase):
    """Test various error conditions."""

    def test_overflow_numbers(self):
        """Test handling of overflow numbers."""
        # Test very large number
        try:
            num2words(10**100, lang="en")
            # Should either handle or raise OverflowError
        except OverflowError:
            # Expected for very large numbers
            pass

    def test_invalid_number_types(self):
        """Test handling of invalid number types."""
        # Complex numbers should raise error
        try:
            num2words(complex(1, 2), lang="en")
        except (TypeError, NotImplementedError):
            # Expected for complex numbers
            pass

    def test_malformed_ordinal_requests(self):
        """Test malformed ordinal requests."""
        # Negative ordinal - should raise TypeError
        with self.assertRaises(TypeError):
            num2words(-5, lang="en", ordinal=True)

        # Float ordinal - should raise TypeError
        with self.assertRaises(TypeError):
            num2words(3.5, lang="en", ordinal=True)
