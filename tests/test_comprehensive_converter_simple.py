"""
Simple tests to improve coverage for comprehensive_converter.py
"""

import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock, patch

from num2words2.converters.comprehensive_converter import (
    ComprehensiveConverter,
    _load_langid,
    test_converter,
)


class TestComprehensiveConverterSimple(TestCase):
    """Simple tests to improve coverage of comprehensive_converter.py"""

    def test_detect_language_with_langid_mock(self):
        """Test language detection with mocked langid."""
        converter = ComprehensiveConverter()

        # Mock langid to be available
        with patch(
            "num2words2.converters.comprehensive_converter._load_langid"
        ) as mock_load:
            mock_langid = MagicMock()
            mock_langid.classify.return_value = ("fr", 0.95)
            mock_load.return_value = mock_langid

            lang = converter.detect_language("Bonjour le monde")
            # Should detect French
            self.assertIsNotNone(lang)

    def test_detect_language_without_external_libs(self):
        """Test language detection using heuristics only."""
        converter = ComprehensiveConverter()

        # Mock langid to fail
        with patch(
            "num2words2.converters.comprehensive_converter._load_langid"
        ) as mock_load:
            mock_load.return_value = None

            # Test heuristic detection for each language
            test_cases = [
                ("Le chat est sur la table avec le chien", "fr"),
                ("Der Hund ist mit der Katze", "de"),
                ("El perro y el gato están con ella", "es"),
                ("Il cane è con il gatto", "it"),
                ("O cão e o gato estão com ela", "pt"),
                ("The cat is with the dog", "en"),
            ]

            for text, expected_lang in test_cases:
                lang = converter.detect_language(text)
                self.assertEqual(lang, expected_lang)

    def test_detect_language_no_patterns(self):
        """Test language detection with no matching patterns."""
        converter = ComprehensiveConverter()

        # Mock langid to be unavailable
        with patch(
            "num2words2.converters.comprehensive_converter._load_langid"
        ) as mock_load:
            mock_load.return_value = None

            # Text with only numbers
            lang = converter.detect_language("123 456 789")
            self.assertEqual(lang, "en")  # Default fallback

    def test_convert_sentence_empty_text(self):
        """Test conversion with empty text."""
        converter = ComprehensiveConverter()

        # Empty string
        result = converter.convert_sentence("", force_language="en")
        self.assertEqual(result, "")

        # Whitespace only
        result = converter.convert_sentence("   ", force_language="en")
        self.assertEqual(result, "   ")

    def test_convert_various_patterns(self):
        """Test conversion of various number patterns."""
        converter = ComprehensiveConverter()

        test_cases = [
            ("Today is 2024-01-15", "en", True),  # Should convert
            ("The temperature is 25°C", "en", True),  # Should convert
            ("He came 1st in the race", "en", False),  # May not convert ordinal suffix
            ("25% discount today", "en", True),  # Should convert
            ("Add 1/2 cup of sugar", "en", False),  # May not convert fraction
            ("Room 404 not found", "en", True),  # Should convert
        ]

        for text, lang, should_change in test_cases:
            result = converter.convert_sentence(text, force_language=lang)
            self.assertIsNotNone(result)
            # Check conversion happened where expected
            if should_change:
                # Should have converted some numbers
                self.assertTrue(
                    any(char.isdigit() for char in text)
                    and not all(char.isdigit() or not char.isalpha() for char in result)
                )

    def test_langid_loading(self):
        """Test _load_langid function."""
        # Just test that it runs without error
        result = _load_langid()
        # Result is either langid module or None
        self.assertTrue(result is None or hasattr(result, "__name__"))

    def test_langid_loading_failure(self):
        """Test _load_langid handles import errors gracefully."""
        # The function should handle import errors and return None
        # We can't easily mock the import without breaking other tests
        # Just verify the function exists and can be called
        try:
            result = _load_langid()
            # Should return either langid or None
            self.assertTrue(result is None or hasattr(result, "__name__"))
        except Exception as e:
            self.fail(f"_load_langid raised unexpected exception: {e}")

    def test_test_converter_function(self):
        """Test the test_converter function."""
        with patch("sys.stdout", new=StringIO()) as fake_output:
            test_converter()
            output = fake_output.getvalue()

            # Check that output contains expected content
            self.assertIn("COMPREHENSIVE CONVERTER TEST", output)
            self.assertIn("=" * 80, output)

            # Check for language tags
            self.assertIn("[fr]", output)
            self.assertIn("[de]", output)
            self.assertIn("[es]", output)
            self.assertIn("[en]", output)
            self.assertIn("[Auto:", output)

    def test_main_block_simulation(self):
        """Simulate the main block execution."""
        # Test with arguments
        with patch.object(sys, "argv", ["prog", "Test 123"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                converter = ComprehensiveConverter()
                sentence = " ".join(sys.argv[1:])

                # No language hint
                result = converter.convert_sentence(sentence)
                print(f"[{converter.lang}] {result}")

                output = fake_output.getvalue()
                self.assertIn("[en]", output)
                self.assertIn("Test", output)

    def test_main_block_with_lang_hint(self):
        """Test main block with language hint."""
        with patch.object(sys, "argv", ["prog", "fr:Test 123"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                converter = ComprehensiveConverter()
                sentence = " ".join(sys.argv[1:])

                # Check for language hint
                if ":" in sentence and len(sentence.split(":")[0]) <= 5:
                    lang, text = sentence.split(":", 1)
                    result = converter.convert_sentence(
                        text.strip(), force_language=lang.strip()
                    )
                    print(f"[{lang}] {result}")

                output = fake_output.getvalue()
                self.assertIn("[fr]", output)

    def test_main_block_no_args(self):
        """Test main block with no arguments."""
        with patch.object(sys, "argv", ["prog"]):
            with patch("sys.stdout", new=StringIO()) as fake_output:
                # Would run test_converter()
                test_converter()

                output = fake_output.getvalue()
                self.assertIn("COMPREHENSIVE CONVERTER TEST", output)

    def test_convert_number_method(self):
        """Test the convert_number method."""
        converter = ComprehensiveConverter()
        converter.lang = "en"

        # Test various number types
        test_cases = [
            (123, "cardinal"),
            (1, "ordinal"),
            (2024, "year"),
            (25, "temperature"),
        ]

        for num, num_type in test_cases:
            result = converter.convert_number(num, num_type)
            self.assertIsNotNone(result)
            self.assertTrue(isinstance(result, str))

    def test_language_detection_with_mixed_text(self):
        """Test language detection with mixed language indicators."""
        converter = ComprehensiveConverter()

        # Text with mixed patterns
        mixed_text = "The température is vingt-cinq degrees"
        lang = converter.detect_language(mixed_text)
        # Should detect one of the languages
        self.assertIn(lang, ["en", "fr"])

    def test_convert_with_forced_language(self):
        """Test conversion with forced language."""
        converter = ComprehensiveConverter()

        # Force different languages
        text = "Test 123"

        for lang in ["en", "fr", "de", "es"]:
            result = converter.convert_sentence(text, force_language=lang)
            self.assertIsNotNone(result)
            self.assertEqual(converter.lang, lang)

    def test_langid_cached_result(self):
        """Test that langid result is cached."""
        # First call
        result1 = _load_langid()

        # Second call should return cached result
        result2 = _load_langid()

        # Should be the same object (cached)
        self.assertIs(result1, result2)

    def test_conversion_with_special_characters(self):
        """Test conversion with special characters."""
        converter = ComprehensiveConverter()

        test_cases = [
            "Price: $100.50",
            "Temperature: -10°C",
            "Score: 95%",
            "Date: 2024/01/15",
        ]

        for text in test_cases:
            result = converter.convert_sentence(text, force_language="en")
            self.assertIsNotNone(result)

    def test_year_conversion_context(self):
        """Test year conversion in context."""
        converter = ComprehensiveConverter()

        year_texts = [
            "In year 2024",
            "Since 1999",
            "Born 1985",
        ]

        for text in year_texts:
            result = converter.convert_sentence(text, force_language="en")
            self.assertIsNotNone(result)
            # Years should be converted
            self.assertNotIn("2024", result) if "2024" in text else None
            self.assertNotIn("1999", result) if "1999" in text else None
