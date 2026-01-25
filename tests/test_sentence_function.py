#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the new num2words_sentence function.
"""

from num2words2 import num2words_sentence


def test_sentence_conversion():
    """Test the sentence conversion function."""

    test_cases = [
        # Auto-detection tests
        ("The temperature is 25°C today.", None, "English with temperature"),
        ("Il fait 30 degrés aujourd'hui.", None, "French with temperature"),
        ("Hoy es 15 de marzo de 2025.", None, "Spanish with date"),
        ("Der Preis beträgt €50.", None, "German with currency"),
        # Forced language tests
        ("I have 3 apples and 2 oranges.", "en", "English numbers"),
        ("J'ai acheté 5 livres pour €20.", "fr", "French with currency"),
        ("Es ist -10 Grad draußen.", "de", "German negative temperature"),
        ("Tengo 100 dólares.", "es", "Spanish currency"),
        # Complex sentences
        ("On January 1st, 2025, the temperature was -5°C.", "en", "Date + temperature"),
        ("Le 1er janvier 2025, il faisait -10°C.", "fr", "French ordinal date + temp"),
        ("El 25 de diciembre de 2024 había 30 grados.", "es", "Spanish date + temp"),
    ]

    print("=" * 80)
    print("TESTING num2words_sentence FUNCTION")
    print("=" * 80)

    for sentence, lang, description in test_cases:
        print(f"\n{description}:")
        print(f"  Input:  {sentence}")

        try:
            if lang:
                result = num2words_sentence(sentence, lang=lang)
                print(f"  Lang:   {lang}")
            else:
                result = num2words_sentence(sentence)
                print("  Lang:   Auto-detected")
            print(f"  Output: {result}")

            # Check if conversion happened
            if any(char.isdigit() for char in result):
                print("  ⚠️  WARNING: Result still contains digits")
            else:
                print("  ✅ SUCCESS: All numbers converted")

        except Exception as e:
            print(f"  ❌ ERROR: {e}")

    print("\n" + "=" * 80)


def test_api_variations():
    """Test different API names for the same function."""

    from num2words2 import convert_sentence, sentence_to_words

    print("\nTesting API variations:")
    sentence = "I have 5 cats."

    print(f"Original: {sentence}")
    print(f"num2words_sentence: {num2words_sentence(sentence)}")
    print(f"sentence_to_words:  {sentence_to_words(sentence)}")
    print(f"convert_sentence:   {convert_sentence(sentence)}")

    # All should give the same result
    assert num2words_sentence(sentence) == sentence_to_words(sentence)
    assert num2words_sentence(sentence) == convert_sentence(sentence)
    print("✅ All API variations work correctly")


def test_edge_cases():
    """Test edge cases."""

    print("\n" + "=" * 80)
    print("EDGE CASES")
    print("=" * 80)

    edge_cases = [
        ("No numbers here!", "en", "No numbers"),
        ("", "en", "Empty string"),
        ("123", "en", "Just a number"),
        ("-45.67", "en", "Negative decimal"),
        ("$1,234.56", "en", "Currency with comma"),
        ("3.14159", "en", "Pi"),
        ("In 1999, 2000, 2001 and 2002", "en", "Multiple years"),
        ("Mix: 5 apples, €10, 25°C, year 2024", "en", "Mixed types"),
    ]

    for sentence, lang, description in edge_cases:
        print(f"\n{description}:")
        print(f"  Input:  {sentence}")
        try:
            result = num2words_sentence(sentence, lang=lang)
            print(f"  Output: {result}")
        except Exception as e:
            print(f"  Error:  {e}")


if __name__ == "__main__":
    test_sentence_conversion()
    test_api_variations()
    test_edge_cases()

    print("\n" + "🎉" * 20)
    print("All tests completed!")
