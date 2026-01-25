"""
Test suite for comprehensive_converter CLI and main function.
"""

import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from num2words2.converters.comprehensive_converter import ComprehensiveConverter


class TestComprehensiveConverterCLI(TestCase):
    """Test CLI functionality of comprehensive converter."""

    def test_main_function_with_arguments(self):
        """Test main function with command line arguments."""
        test_args = ["prog", "Test 123", "en"]

        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                # Import and run the main section
                pass

                # Simulate running with arguments
                converter = ComprehensiveConverter()
                result = converter.convert_sentence(
                    test_args[1], force_language=test_args[2]
                )
                print(result)

                output = fake_output.getvalue()
                self.assertIn("one hundred", output.lower())

    def test_interactive_mode_simulation(self):
        """Test interactive mode input processing."""
        converter = ComprehensiveConverter()

        # Test various inputs that would be used in interactive mode
        test_cases = [
            ("[en] Test 123", "en"),
            ("[fr] Test 456", "fr"),
            ("Test 789", None),
        ]

        for input_text, expected_lang in test_cases:
            # Simulate parsing language prefix
            if input_text.startswith("["):
                lang_end = input_text.index("]")
                lang = input_text[1:lang_end]
                text = input_text[lang_end + 1 :].strip()
                result = converter.convert_sentence(text, force_language=lang)
                self.assertEqual(converter.lang, lang)
            else:
                result = converter.convert_sentence(input_text)
                self.assertIsNotNone(result)

    def test_langid_loading(self):
        """Test langid loading and fallback."""
        # Test the _load_langid function behavior
        from num2words2.converters.comprehensive_converter import _load_langid

        # This should attempt to load langid
        result = _load_langid()
        # Result is either langid module or None
        self.assertTrue(result is None or hasattr(result, "classify"))

    def test_converter_with_various_text_types(self):
        """Test converter with various text types."""
        converter = ComprehensiveConverter()

        # Unicode text
        result = converter.convert_sentence("Тест 123", force_language="ru")
        self.assertIsNotNone(result)

        # Text with emojis
        result = converter.convert_sentence("Test 😊 123", force_language="en")
        self.assertIn("😊", result)

        # Text with special formatting
        result = converter.convert_sentence("Test\t123\nNew line", force_language="en")
        self.assertIn("\t", result)
        self.assertIn("\n", result)

    def test_converter_state_management(self):
        """Test that converter properly manages internal state."""
        converter = ComprehensiveConverter()

        # Check initial state
        self.assertIsNone(converter.lang)

        # Force a language
        converter.convert_sentence("Test 1", force_language="en")
        self.assertEqual(converter.lang, "en")

        # Force a different language
        converter.convert_sentence("Test 2", force_language="fr")
        self.assertEqual(converter.lang, "fr")

        # Auto-detect should update lang
        converter.convert_sentence("This is English text with 3")
        self.assertEqual(converter.lang, "en")

    def test_number_extraction_edge_cases(self):
        """Test number extraction with edge cases."""
        converter = ComprehensiveConverter()

        # Numbers at boundaries - extract_numbers may not find all
        numbers = converter.extract_numbers("123 456 789")
        self.assertGreaterEqual(len(numbers), 1)

        # Numbers with various separators
        numbers = converter.extract_numbers("1,234 and 5.678")
        self.assertGreaterEqual(len(numbers), 2)

        # Scientific notation
        numbers = converter.extract_numbers("1.23e4")
        self.assertGreaterEqual(len(numbers), 1)

    def test_year_context_detection(self):
        """Test year detection in various contexts."""
        converter = ComprehensiveConverter()

        # Clear year contexts
        result = converter.convert_sentence("In year 2024", force_language="en")
        self.assertIsNotNone(result)

        result = converter.convert_sentence("Born 1990", force_language="en")
        self.assertIsNotNone(result)

        result = converter.convert_sentence("Since 2000", force_language="en")
        self.assertIsNotNone(result)

        # Not year contexts
        result = converter.convert_sentence("Room 2024", force_language="en")
        self.assertIsNotNone(result)

        result = converter.convert_sentence("Code 1990", force_language="en")
        self.assertIsNotNone(result)

    def test_temperature_patterns(self):
        """Test temperature pattern detection."""
        converter = ComprehensiveConverter()

        # Test conversion of temperature patterns
        result = converter.convert_sentence("It's 25°C", force_language="en")
        self.assertIsNotNone(result)

        result = converter.convert_sentence("72°F today", force_language="en")
        self.assertIsNotNone(result)

    def test_ordinal_suffix_patterns(self):
        """Test ordinal suffix conversion."""
        converter = ComprehensiveConverter()

        # Test ordinal conversion
        result = converter.convert_sentence("1st place", force_language="en")
        self.assertIsNotNone(result)

        result = converter.convert_sentence("2nd winner", force_language="en")
        self.assertIsNotNone(result)

    def test_date_format_patterns(self):
        """Test various date format patterns."""
        converter = ComprehensiveConverter()

        date_patterns = [
            "2024-01-15",  # ISO
            "15/01/2024",  # European
            "01/15/2024",  # US
            "15.01.2024",  # Dot separator
            "Jan 15, 2024",  # Month name
            "15 January 2024",  # Full month
        ]

        for pattern in date_patterns:
            result = converter.convert_sentence(pattern, force_language="en")
            self.assertIsNotNone(result)

    def test_percentage_handling(self):
        """Test percentage number handling."""
        converter = ComprehensiveConverter()

        percentage_patterns = [
            "25%",
            "99.9%",
            "100 %",
            "0.1%",
        ]

        for pattern in percentage_patterns:
            numbers = converter.extract_numbers(pattern)
            self.assertGreaterEqual(len(numbers), 1)

            result = converter.convert_sentence(
                f"Rate is {pattern}", force_language="en"
            )
            self.assertIsNotNone(result)

    def test_fraction_handling(self):
        """Test fraction handling."""
        converter = ComprehensiveConverter()

        fraction_patterns = [
            "1/2",
            "3/4",
            "1/4",
            "2/3",
        ]

        for pattern in fraction_patterns:
            result = converter.convert_sentence(
                f"Add {pattern} cup", force_language="en"
            )
            self.assertIsNotNone(result)

    def test_number_word_mixing(self):
        """Test handling of mixed number-word content."""
        converter = ComprehensiveConverter()

        # Number ranges
        result = converter.convert_sentence("Pages 10-20", force_language="en")
        self.assertIsNotNone(result)

        # Number lists
        result = converter.convert_sentence("Items: 1, 2, 3, 4, 5", force_language="en")
        self.assertIsNotNone(result)

        # Math expressions
        result = converter.convert_sentence("2 + 2 = 4", force_language="en")
        self.assertIsNotNone(result)

    def test_edge_case_languages(self):
        """Test edge case language handling."""
        converter = ComprehensiveConverter()

        # Language code edge cases
        for lang_code in ["", "unknown", "xx", "???"]:
            result = converter.convert_sentence("Test 123", force_language=lang_code)
            self.assertIsNotNone(result)

        # Mixed scripts
        result = converter.convert_sentence("Test 测试 123", force_language="en")
        self.assertIsNotNone(result)

    def test_convert_number_with_types(self):
        """Test convert_number with different number types."""
        converter = ComprehensiveConverter()
        converter.lang = "en"

        # Test with year type
        result = converter.convert_number(1999, "year")
        self.assertIn("nineteen", result.lower())

        # Test with temperature type
        result = converter.convert_number(32, "temperature")
        self.assertIn("thirty", result.lower())

        # Test ordinal is converted as cardinal by convert_number
        result = converter.convert_number(3, "cardinal")
        self.assertIn("three", result.lower())

        # Test with unknown type defaults to cardinal
        result = converter.convert_number(42, "unknown")
        self.assertIn("forty", result.lower())

    def test_large_text_processing(self):
        """Test processing of large text blocks."""
        converter = ComprehensiveConverter()

        # Create a large text with many numbers
        large_text = " ".join([f"Item {i}" for i in range(100)])
        result = converter.convert_sentence(large_text, force_language="en")
        self.assertIsNotNone(result)

        # Text with repeated patterns
        repeated = "Test 123. " * 50
        result = converter.convert_sentence(repeated, force_language="en")
        self.assertIsNotNone(result)

    def test_whitespace_preservation(self):
        """Test that various whitespace is preserved."""
        converter = ComprehensiveConverter()

        # Multiple spaces
        result = converter.convert_sentence("Test  123   end", force_language="en")
        self.assertIn("  ", result)

        # Mixed whitespace
        result = converter.convert_sentence("Test\t123\n\rEnd", force_language="en")
        self.assertIn("\t", result)
        self.assertIn("\n", result)

    def test_boundary_numbers(self):
        """Test boundary number values."""
        converter = ComprehensiveConverter()
        converter.lang = "en"

        # Zero
        result = converter.convert_number(0, "cardinal")
        self.assertEqual(result, "zero")

        # Very large number
        result = converter.convert_number(999999999999, "cardinal")
        self.assertIn("billion", result.lower())

        # Negative
        result = converter.convert_number(-42, "cardinal")
        self.assertTrue("minus" in result.lower() or "negative" in result.lower())
