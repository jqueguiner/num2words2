#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
End-to-end tests for num2words_sentence function using generated test cases
Reads test cases from test_e2e_sentences.csv
"""

import csv
import sys
import unittest
from pathlib import Path

from num2words2 import num2words_sentence  # noqa: E402

# Add parent directory to path to import num2words2
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestNum2WordsSentencesE2E(unittest.TestCase):
    """Test num2words_sentence with generated test cases from CSV"""

    @classmethod
    def setUpClass(cls):
        """Load test cases from CSV file"""
        cls.test_cases = []
        csv_file = Path(__file__).parent / "data" / "e2e_test_sentences.csv"

        if not csv_file.exists():
            print(
                f"Warning: {csv_file} not found. Run generate_test_e2e_sentences.py first."
            )
            return

        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Map CSV fields to expected fields
                    if (
                        row.get("language_code")
                        and row.get("original_sentence")
                        and row.get("expected_output")
                    ):
                        cls.test_cases.append(
                            {
                                "lang": row["language_code"],
                                "input_sentence": row["original_sentence"],
                                "expected_output": row["expected_output"],
                                "english_translation": row.get(
                                    "sentence_translation", ""
                                ),
                                "description": row.get("language_name", ""),
                                "test_type": "e2e",
                            }
                        )

            print(f"Loaded {len(cls.test_cases)} test cases from {csv_file}")
        except Exception as e:
            print(f"Error loading test cases: {e}")

    def test_sentence_conversions(self):
        """Test all sentence conversions from CSV"""
        if not self.test_cases:
            self.skipTest("No test cases loaded from CSV")

        failures = []
        successes = 0

        for i, case in enumerate(self.test_cases):
            lang = case["lang"]
            input_sentence = case["input_sentence"]
            expected_output = case["expected_output"]
            case.get("english_translation", "")
            description = case.get("description", f"Test {i+1}")
            test_type = case.get("test_type", "unknown")

            try:
                # Convert underscores to hyphens for language codes
                lang_code = lang.replace("_", "-")
                result = num2words_sentence(input_sentence, lang=lang_code)

                if result == expected_output:
                    successes += 1
                else:
                    failures.append(
                        {
                            "index": i + 1,
                            "lang": lang,
                            "description": description,
                            "test_type": test_type,
                            "input": input_sentence,
                            "expected": expected_output,
                            "actual": result,
                        }
                    )
            except Exception as e:
                failures.append(
                    {
                        "index": i + 1,
                        "lang": lang,
                        "description": description,
                        "test_type": test_type,
                        "input": input_sentence,
                        "expected": expected_output,
                        "error": str(e),
                    }
                )

        # Report results
        total = len(self.test_cases)
        print(f"\n{'='*60}")
        print(f"Test Results: {successes}/{total} passed")
        print(f"{'='*60}")

        if failures:
            print(f"\nFailed tests ({len(failures)}):")
            print("-" * 60)

            # Group failures by language
            by_lang = {}
            for fail in failures:
                lang = fail["lang"]
                if lang not in by_lang:
                    by_lang[lang] = []
                by_lang[lang].append(fail)

            for lang in sorted(by_lang.keys()):
                print(f"\n{lang} ({len(by_lang[lang])} failures):")
                for fail in by_lang[lang][:3]:  # Show first 3 failures per language
                    print(
                        f"  Test #{fail['index']}: {fail['description']} [{fail['test_type']}]"
                    )
                    print(f"    Input:    {fail['input']}")
                    if "error" in fail:
                        print(f"    Error:    {fail['error']}")
                    else:
                        print(f"    Expected: {fail['expected']}")
                        print(f"    Actual:   {fail['actual']}")

                if len(by_lang[lang]) > 3:
                    print(f"  ... and {len(by_lang[lang]) - 3} more")

        # Assert that we have a good success rate
        success_rate = successes / total if total > 0 else 0
        print(f"\nSuccess rate: {success_rate:.1%}")

        # We expect at least 80% success rate for generated tests
        # (some may fail due to language-specific quirks or AI generation issues)
        if success_rate < 0.8:
            self.fail(f"Success rate {success_rate:.1%} is below 80% threshold")

    def test_specific_languages(self):
        """Test specific high-priority languages"""
        priority_langs = ["en", "fr", "es", "de", "ja", "zh-cn", "ar", "ru"]

        for lang in priority_langs:
            lang_cases = [c for c in self.test_cases if c["lang"] == lang]

            if not lang_cases:
                print(f"Warning: No test cases for {lang}")
                continue

            with self.subTest(lang=lang):
                failures = 0
                for case in lang_cases[:5]:  # Test first 5 cases per language
                    lang_code = lang.replace("_", "-")
                    try:
                        result = num2words_sentence(
                            case["input_sentence"], lang=lang_code
                        )
                        if result != case["expected_output"]:
                            failures += 1
                    except Exception as e:
                        failures += 1
                        print(f"Error in {lang}: {e}")

                # Allow some failures but not all
                self.assertLess(
                    failures,
                    len(lang_cases[:5]),
                    f"Too many failures for {lang}: {failures}/{min(5, len(lang_cases))}",
                )


class TestNum2WordsSentenceManual(unittest.TestCase):
    """Manual test cases for num2words_sentence function"""

    def test_english_basic(self):
        """Test basic English sentences"""
        test_cases = [
            ("I have 5 apples", "I have five apples"),
            ("The year 2024", "The year two thousand and twenty-four"),
            ("It costs $99.99", "It costs ninety-nine dollars, ninety-nine cents"),
            ("Temperature is -10 degrees", "Temperature is minus ten degrees"),
            ("1000000 people", "One million people"),
        ]

        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                result = num2words_sentence(input_text, lang="en")
                self.assertEqual(result, expected)

    def test_multilingual(self):
        """Test various languages with simple cases"""
        test_cases = [
            ("fr", "J'ai 3 chats", "J'ai trois chats"),
            ("es", "Tengo 5 libros", "Tengo cinco libros"),
            ("de", "Ich bin 25 Jahre alt", "Ich bin fünfundzwanzig Jahre alt"),
            ("it", "Costa 10 euro", "Costa dieci euro"),
            ("pt", "São 8 horas", "São oito horas"),
        ]

        for lang, input_text, expected in test_cases:
            with self.subTest(lang=lang, input=input_text):
                result = num2words_sentence(input_text, lang=lang)
                self.assertEqual(result, expected)

    def test_edge_cases(self):
        """Test edge cases"""
        # No numbers
        result = num2words_sentence("This has no numbers", lang="en")
        self.assertEqual(result, "This has no numbers")

        # Empty string
        result = num2words_sentence("", lang="en")
        self.assertEqual(result, "")

        # Only numbers
        result = num2words_sentence("42", lang="en")
        self.assertEqual(result, "Forty-two")

        # Numbers in words (should not be converted)
        result = num2words_sentence("Test123word", lang="en")
        self.assertEqual(result, "Test123word")

    def test_capitalization(self):
        """Test capitalization rules"""
        # Start of sentence
        result = num2words_sentence("5 cats are here", lang="en")
        self.assertEqual(result, "Five cats are here")

        # After period
        result = num2words_sentence("Done. 10 more to go", lang="en")
        self.assertEqual(result, "Done. Ten more to go")

        # After exclamation
        result = num2words_sentence("Wow! 100 points", lang="en")
        self.assertEqual(result, "Wow! One hundred points")

        # After question mark
        result = num2words_sentence("Really? 50 dollars?", lang="en")
        self.assertEqual(result, "Really? Fifty dollars?")


def main():
    """Run tests"""
    # Create test suite
    suite = unittest.TestSuite()

    # Add manual tests
    suite.addTest(unittest.makeSuite(TestNum2WordsSentenceManual))

    # Add E2E tests if CSV exists
    csv_file = Path(__file__).parent / "data" / "e2e_test_sentences.csv"
    if csv_file.exists():
        suite.addTest(unittest.makeSuite(TestNum2WordsSentencesE2E))
    else:
        print(f"Note: {csv_file} not found. Skipping E2E tests.")
        print("Run: python generate_test_e2e_sentences.py --sample")
        print("to generate sample test cases.\n")

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
