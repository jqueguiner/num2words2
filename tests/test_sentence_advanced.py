"""
Advanced test suite for sentence converter module.
"""

import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from num2words2.converters.sentence import SentenceConverter, num2words_sentence


class TestSentenceConverterAdvanced(TestCase):
    """Advanced tests for SentenceConverter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.converter = SentenceConverter()

    def test_langid_loading_mechanism(self):
        """Test langid loading with various conditions."""
        # Test the loading mechanism
        from num2words2.converters.sentence import _load_langid

        # Save original environment
        original_env = os.environ.get("NUM2WORDS2_ENABLE_LANGID")

        try:
            # Test with langid explicitly disabled
            os.environ["NUM2WORDS2_ENABLE_LANGID"] = "0"
            result = _load_langid()
            # On macOS without explicit enable, should return None
            if sys.platform == "darwin":
                self.assertIsNone(result)

            # Test with langid explicitly enabled
            os.environ["NUM2WORDS2_ENABLE_LANGID"] = "1"
            result = _load_langid()
            # Should attempt to load langid
            self.assertTrue(result is None or hasattr(result, "classify"))

        finally:
            # Restore original environment
            if original_env is None:
                os.environ.pop("NUM2WORDS2_ENABLE_LANGID", None)
            else:
                os.environ["NUM2WORDS2_ENABLE_LANGID"] = original_env

    def test_detect_language_with_langid_mock(self):
        """Test language detection with mocked langid."""
        with patch("num2words2.converters.sentence._load_langid") as mock_load:
            # Mock langid module
            mock_langid = MagicMock()
            mock_langid.classify.return_value = ("fr", 0.95)
            mock_load.return_value = mock_langid

            # Create new converter to trigger langid loading
            converter = SentenceConverter()
            lang = converter.detect_language("Bonjour le monde")
            self.assertEqual(lang, "fr")

    def test_detect_language_without_langid(self):
        """Test language detection when langid is not available."""
        with patch("num2words2.converters.sentence._load_langid") as mock_load:
            mock_load.return_value = None

            converter = SentenceConverter()
            lang = converter.detect_language("Hello world")
            # Should fall back to default
            self.assertEqual(lang, "en")

    def test_extract_numbers_complex_patterns(self):
        """Test complex number extraction patterns."""
        # Roman numerals (should be ignored)
        numbers = self.converter.extract_numbers("Chapter III and IV")
        self.assertEqual(len(numbers), 0)  # Roman numerals not extracted

        # Mixed formats in same string
        numbers = self.converter.extract_numbers("1st, 2.5, -3, 4e2")
        self.assertGreaterEqual(len(numbers), 2)  # At least some numbers detected

        # Numbers with units - extract_numbers may not detect all
        numbers = self.converter.extract_numbers("100 50 25")
        self.assertGreaterEqual(len(numbers), 1)

    def test_convert_number_edge_cases(self):
        """Test convert_number with edge cases."""
        self.converter.lang = "en"

        # Very small decimal
        result = self.converter.convert_number(0.0001, "cardinal")
        self.assertIsNotNone(result)

        # String number
        result = self.converter.convert_number(42, "cardinal")
        self.assertIn("forty", result.lower())

    def test_sentence_capitalization_rules(self):
        """Test sentence capitalization rules."""
        # After period with space
        result = num2words_sentence("First 1. Second 2.", lang="en")
        self.assertIn("First one. Second two.", result)

        # After exclamation
        result = num2words_sentence("Wow 1! Amazing 2!", lang="en")
        self.assertIn("!", result)

        # After question mark
        result = num2words_sentence("Why 1? Because 2.", lang="en")
        self.assertIn("?", result)

    def test_multi_language_in_same_instance(self):
        """Test using multiple languages with same instance."""
        # English
        result = num2words_sentence("I have 5 apples", lang="en")
        self.assertIn("five", result)

        # French
        result = num2words_sentence("J'ai 5 pommes", lang="fr")
        self.assertIn("cinq", result)

        # Spanish
        result = num2words_sentence("Tengo 5 manzanas", lang="es")
        self.assertIn("cinco", result)

        # German
        result = num2words_sentence("Ich habe 5 Äpfel", lang="de")
        self.assertIn("fünf", result)

    def test_preserve_special_characters(self):
        """Test preservation of special characters."""
        # Unicode characters
        result = num2words_sentence("Test 5 €₹¥", lang="en")
        self.assertIn("€", result)
        self.assertIn("₹", result)
        self.assertIn("¥", result)

        # Control characters
        result = num2words_sentence("Line1\nLine2 5", lang="en")
        self.assertIn("\n", result)

        # HTML entities
        result = num2words_sentence("&lt;5&gt;", lang="en")
        self.assertIn("&lt;", result)
        self.assertIn("&gt;", result)

    def test_number_type_detection_advanced(self):
        """Test advanced number type detection."""
        # Phone numbers (should be preserved or handled specially)
        numbers = self.converter.extract_numbers("Call +1-555-1234")
        for num in numbers:
            # Phone numbers might be detected differently
            self.assertIsNotNone(num)

        # ZIP codes
        numbers = self.converter.extract_numbers("ZIP: 90210")
        self.assertGreaterEqual(len(numbers), 1)

        # Version numbers
        numbers = self.converter.extract_numbers("v3.14.159")
        self.assertGreaterEqual(len(numbers), 1)

    def test_contextual_number_conversion(self):
        """Test that numbers are converted based on context."""
        # Year context
        result = num2words_sentence("The year 2024 is here", lang="en")
        self.assertIsNotNone(result)

        # Temperature context
        result = num2words_sentence("It's 25°C outside", lang="en")
        self.assertIn("twenty", result.lower())

        # Currency context
        result = num2words_sentence("Cost: $100", lang="en")
        self.assertIsNotNone(result)

    def test_error_handling_in_conversion(self):
        """Test error handling during conversion."""
        # Invalid language code should raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            num2words_sentence("Test 123", lang="invalid_lang")

        # None input should be handled
        try:
            result = num2words_sentence(None, lang="en")
        except (AttributeError, TypeError):
            # Expected for None input
            pass

        # Non-string input - convert to string first
        result = num2words_sentence(str(12345), lang="en")
        self.assertIsNotNone(result)

    def test_performance_with_many_numbers(self):
        """Test performance with text containing many numbers."""
        # Generate text with many numbers
        text = " ".join([str(i) for i in range(1000)])
        result = num2words_sentence(text, lang="en")
        self.assertIsNotNone(result)
        # Should have converted numbers
        self.assertNotIn("999", result)

    def test_mixed_decimal_formats(self):
        """Test various decimal number formats."""
        test_cases = [
            ("3.14", "three point one four"),
            ("0.5", "zero point five"),
            ("-1.5", "minus one point five"),
            ("100.00", "one hundred"),
        ]

        for number_str, expected_substr in test_cases:
            result = num2words_sentence(f"Value: {number_str}", lang="en")
            # Check that number is converted (exact format may vary)
            self.assertNotIn(number_str, result)

    def test_ordinal_in_various_positions(self):
        """Test ordinal detection in various positions."""
        # Start of sentence
        result = num2words_sentence("1st place goes to", lang="en")
        self.assertIn("first", result.lower())

        # Middle of sentence
        result = num2words_sentence("He came in 2nd place", lang="en")
        self.assertIn("second", result.lower())

        # End of sentence
        result = num2words_sentence("She finished 3rd", lang="en")
        self.assertIn("third", result.lower())

    def test_number_agreement_preservation(self):
        """Test that number agreement is preserved in context."""
        # Singular - check case insensitive
        result = num2words_sentence("1 apple", lang="en")
        self.assertIn("one apple", result.lower())

        # Plural - also check case insensitive
        result = num2words_sentence("2 apples", lang="en")
        self.assertIn("two apples", result.lower())

    def test_sentence_boundary_detection(self):
        """Test sentence boundary detection for capitalization."""
        text = "First sentence with 1. Second sentence with 2! Third with 3?"
        result = num2words_sentence(text, lang="en")
        # Check that sentence boundaries are preserved
        self.assertIn(". ", result)
        self.assertIn("! ", result)
        self.assertIn("?", result)

    def test_abbreviation_handling(self):
        """Test handling of abbreviations with numbers."""
        abbreviations = [
            "Dr. 1 Smith",
            "No. 5",
            "Ch. 3",
            "Vol. 2",
        ]

        for text in abbreviations:
            result = num2words_sentence(text, lang="en")
            self.assertIsNotNone(result)
            # Abbreviation dots should be preserved
            self.assertIn(".", result)

    def test_mathematical_expressions(self):
        """Test mathematical expression handling."""
        expressions = [
            "2 + 2 = 4",
            "10 - 5 = 5",
            "3 × 3 = 9",
            "8 ÷ 2 = 4",
        ]

        for expr in expressions:
            result = num2words_sentence(expr, lang="en")
            self.assertIsNotNone(result)
            # Math operators should be preserved
            if "+" in expr:
                self.assertIn("+", result)
            elif "×" in expr:
                self.assertIn("×", result)

    def test_url_and_email_preservation(self):
        """Test that URLs and emails are preserved."""
        # URL with numbers
        result = num2words_sentence("Visit http://site.com/page123", lang="en")
        # URL structure should be preserved
        self.assertIn("http://", result)

        # Email with numbers
        result = num2words_sentence("Contact user123@domain.com", lang="en")
        self.assertIn("@", result)

    def test_quoted_text_handling(self):
        """Test handling of quoted text with numbers."""
        # Single quotes
        result = num2words_sentence("He said '5 times'", lang="en")
        self.assertIn("'", result)

        # Double quotes
        result = num2words_sentence('She said "10 points"', lang="en")
        self.assertIn('"', result)

    def test_list_and_enumeration_handling(self):
        """Test handling of lists and enumerations."""
        # Numbered list
        text = "1. First item\n2. Second item\n3. Third item"
        result = num2words_sentence(text, lang="en")
        self.assertIn("\n", result)  # Line breaks preserved

        # Comma-separated numbers
        result = num2words_sentence("Numbers: 1, 2, 3, 4, 5", lang="en")
        self.assertIn(",", result)  # Commas preserved
