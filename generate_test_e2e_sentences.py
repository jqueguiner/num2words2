#!/usr/bin/env python
"""
Generate test cases for num2words_sentence function using OpenAI API
Usage: python generate_test_e2e_sentences.py --count 100 [--languages en fr de] [--output test_e2e_sentences.csv]
"""

import argparse
import csv
import json
import os
import sys
from typing import Dict, List, Optional

from openai import OpenAI


def get_all_languages():
    """Get all available language codes from the num2words2 library"""
    return [
        "af",
        "am",
        "ar",
        "as",
        "az",
        "ba",
        "be",
        "bg",
        "bn",
        "bo",
        "br",
        "bs",
        "ca",
        "ce",
        "cs",
        "cy",
        "da",
        "de",
        "el",
        "en",
        "en-in",
        "en-ng",
        "eo",
        "es",
        "es-co",
        "es-cr",
        "es-gt",
        "es-ni",
        "es-ve",
        "et",
        "eu",
        "fa",
        "fi",
        "fo",
        "fr",
        "fr-be",
        "fr-ch",
        "fr-dz",
        "gl",
        "gu",
        "ha",
        "haw",
        "he",
        "hi",
        "hr",
        "ht",
        "hu",
        "hy",
        "id",
        "is",
        "it",
        "ja",
        "jw",
        "ka",
        "kk",
        "km",
        "kn",
        "ko",
        "kz",
        "la",
        "lb",
        "ln",
        "lo",
        "lt",
        "lv",
        "mg",
        "mi",
        "mk",
        "ml",
        "mn",
        "mr",
        "ms",
        "mt",
        "my",
        "ne",
        "nl",
        "nn",
        "no",
        "oc",
        "pa",
        "pl",
        "ps",
        "pt",
        "pt-br",
        "ro",
        "ru",
        "sa",
        "sd",
        "si",
        "sk",
        "sl",
        "sn",
        "so",
        "sq",
        "sr",
        "su",
        "sv",
        "sw",
        "ta",
        "te",
        "tet",
        "tg",
        "th",
        "tk",
        "tl",
        "tr",
        "tt",
        "uk",
        "ur",
        "uz",
        "vi",
        "wo",
        "yi",
        "yo",
        "zh",
        "zh-cn",
        "zh-hk",
        "zh-tw",
    ]


def get_language_names():
    """Map language codes to full names for better prompts"""
    return {
        "en": "English",
        "fr": "French",
        "de": "German",
        "es": "Spanish",
        "it": "Italian",
        "pt": "Portuguese",
        "pt-br": "Brazilian Portuguese",
        "nl": "Dutch",
        "ru": "Russian",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "zh-cn": "Chinese Simplified",
        "zh-tw": "Chinese Traditional",
        "ar": "Arabic",
        "he": "Hebrew",
        "hi": "Hindi",
        "bn": "Bengali",
        "ta": "Tamil",
        "te": "Telugu",
        "th": "Thai",
        "vi": "Vietnamese",
        "tr": "Turkish",
        "pl": "Polish",
        "cs": "Czech",
        "sk": "Slovak",
        "hu": "Hungarian",
        "ro": "Romanian",
        "bg": "Bulgarian",
        "el": "Greek",
        "sv": "Swedish",
        "no": "Norwegian",
        "da": "Danish",
        "fi": "Finnish",
        "is": "Icelandic",
        "et": "Estonian",
        "lv": "Latvian",
        "lt": "Lithuanian",
        "uk": "Ukrainian",
        "be": "Belarusian",
        "sr": "Serbian",
        "hr": "Croatian",
        "sl": "Slovenian",
        "mk": "Macedonian",
        "sq": "Albanian",
        "ka": "Georgian",
        "hy": "Armenian",
        "az": "Azerbaijani",
        "kk": "Kazakh",
        "uz": "Uzbek",
        "tk": "Turkmen",
        "tg": "Tajik",
        "mn": "Mongolian",
        "fa": "Persian",
        "ur": "Urdu",
        "ps": "Pashto",
        "sd": "Sindhi",
        "pa": "Punjabi",
        "gu": "Gujarati",
        "mr": "Marathi",
        "kn": "Kannada",
        "ml": "Malayalam",
        "si": "Sinhala",
        "ne": "Nepali",
        "as": "Assamese",
        "km": "Khmer",
        "lo": "Lao",
        "my": "Burmese",
        "bo": "Tibetan",
        "am": "Amharic",
        "ha": "Hausa",
        "yo": "Yoruba",
        "sw": "Swahili",
        "sn": "Shona",
        "af": "Afrikaans",
        "id": "Indonesian",
        "ms": "Malay",
        "jw": "Javanese",
        "tl": "Tagalog",
        "haw": "Hawaiian",
        "mi": "Maori",
        "mg": "Malagasy",
        "mt": "Maltese",
        "cy": "Welsh",
        "ga": "Irish",
        "gl": "Galician",
        "eu": "Basque",
        "ca": "Catalan",
        "oc": "Occitan",
        "br": "Breton",
        "fo": "Faroese",
        "lb": "Luxembourgish",
        "yi": "Yiddish",
        "eo": "Esperanto",
        "la": "Latin",
        "sa": "Sanskrit",
        "tet": "Tetum",
        "ht": "Haitian Creole",
        "wo": "Wolof",
        "ln": "Lingala",
        "so": "Somali",
        "su": "Sundanese",
        "ce": "Chechen",
        "ba": "Bashkir",
        "tt": "Tatar",
        "bs": "Bosnian",
        "nn": "Norwegian Nynorsk",
        "kz": "Kazakh",
        "en-in": "Indian English",
        "en-ng": "Nigerian English",
        "es-co": "Colombian Spanish",
        "es-cr": "Costa Rican Spanish",
        "es-gt": "Guatemalan Spanish",
        "es-ni": "Nicaraguan Spanish",
        "es-ve": "Venezuelan Spanish",
        "fr-be": "Belgian French",
        "fr-ch": "Swiss French",
        "fr-dz": "Algerian French",
        "zh-hk": "Hong Kong Chinese",
    }


def setup_openai_client():
    """Setup OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)
    return OpenAI(api_key=api_key)


def generate_sentence_test_cases(
    client: OpenAI,
    count: int = 100,
    languages: Optional[List[str]] = None,
    model: str = "gpt-4o-mini",
) -> List[Dict]:
    """Generate sentence test cases using OpenAI API"""

    system_prompt = """You are a test case generator for the num2words_sentence function.
    This function converts all numbers in a sentence to their word equivalents.

    Generate test cases in JSON format with the following structure:
    [
        {
            "lang": "<language code>",
            "input_sentence": "<sentence with numbers>",
            "expected_output": "<sentence with numbers converted to words>",
            "english_translation": "<English translation of the input sentence>",
            "description": "<brief description of what's being tested>",
            "test_type": "<type of test: basic, decimal, negative, large_number, mixed, edge_case, etc.>"
        }
    ]

    IMPORTANT RULES:
    1. The input_sentence MUST be in the specified language (not English unless lang='en')
    2. The expected_output must have ALL numbers converted to words in that language
    3. Include diverse scenarios:
       - Simple sentences with single numbers
       - Sentences with multiple numbers
       - Decimal numbers (e.g., 3.14, 19.99)
       - Negative numbers (e.g., -5, -10.5)
       - Large numbers (thousands, millions)
       - Numbers at the start of sentences (should be capitalized)
       - Numbers after punctuation marks (. ! ?)
       - Mixed formats in the same sentence
       - Edge cases like 0, 1, very large numbers
       - Numbers that are part of compound words should NOT be converted (e.g., "Test123word" stays as is)

    4. Make sentences natural and realistic for each language
    5. Test capitalization rules (numbers at sentence start should capitalize)
    6. Include culturally appropriate examples for each language

    Return ONLY the JSON array, no additional text."""

    # Get languages to test
    if languages is None:
        test_langs = get_all_languages()
    else:
        test_langs = languages

    lang_names = get_language_names()

    # Generate in batches for better results
    10 if len(test_langs) > 10 else 20
    all_test_cases = []

    # Calculate tests per language
    tests_per_language = max(1, count // len(test_langs))
    remainder = count % len(test_langs)

    for i, lang in enumerate(test_langs):
        # Add extra test for remainder distribution
        current_count = tests_per_language + (1 if i < remainder else 0)
        if current_count == 0:
            continue

        lang_name = lang_names.get(lang, lang.upper())

        user_prompt = f"""Generate EXACTLY {current_count} test cases for the '{lang}' ({lang_name}) language.

        The sentences must be in {lang_name}, not in English!
        For each test case, also provide the English translation of the input sentence.

        Include a variety of test types:
        - Basic sentences with single numbers
        - Multiple numbers in one sentence
        - Decimal numbers
        - Negative numbers
        - Large numbers (thousands, millions)
        - Numbers at start of sentence
        - Mixed number formats

        Make the sentences natural and culturally appropriate for {lang_name} speakers.

        Return ONLY the JSON array."""

        try:
            print(
                f"  Generating {current_count} test cases for {lang} ({lang_name})..."
            )
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=4000,
            )

            # Parse the JSON response
            content = response.choices[0].message.content
            # Clean up the content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            test_cases = json.loads(content.strip())

            if isinstance(test_cases, list):
                # Ensure language code is set correctly
                for case in test_cases:
                    case["lang"] = lang
                all_test_cases.extend(test_cases)
                print(f"    Generated {len(test_cases)} test cases for {lang}")
            else:
                print(f"  Warning: Expected list but got {type(test_cases)} for {lang}")

        except json.JSONDecodeError as e:
            print(f"  Error parsing JSON for {lang}: {e}")
            continue
        except Exception as e:
            print(f"  Error generating test cases for {lang}: {e}")
            continue

    print(f"\nTotal test cases generated: {len(all_test_cases)}")
    return all_test_cases[:count]  # Ensure we don't exceed requested count


def write_sentence_tests_to_csv(
    test_cases: List[Dict], output_file: str, append: bool = False
):
    """Write sentence test cases to CSV file"""

    if not test_cases:
        print("No test cases to write")
        return

    # Define CSV headers
    headers = [
        "lang",
        "input_sentence",
        "expected_output",
        "english_translation",
        "description",
        "test_type",
    ]

    try:
        mode = "a" if append else "w"
        write_header = not (append and os.path.exists(output_file))

        with open(output_file, mode, newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if write_header:
                writer.writeheader()

            for case in test_cases:
                # Ensure all required fields exist
                row = {
                    "lang": case.get("lang", ""),
                    "input_sentence": case.get("input_sentence", ""),
                    "expected_output": case.get("expected_output", ""),
                    "english_translation": case.get("english_translation", ""),
                    "description": case.get("description", ""),
                    "test_type": case.get("test_type", "basic"),
                }
                writer.writerow(row)

        print(f"Successfully wrote {len(test_cases)} test cases to {output_file}")

    except Exception as e:
        print(f"Error writing to CSV: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate num2words_sentence test cases using OpenAI"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="test_e2e_sentences.csv",
        help="Output CSV file (default: test_e2e_sentences.csv)",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=100,
        help="Total number of test cases to generate (default: 100)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini for cost efficiency)",
    )
    parser.add_argument(
        "--append",
        "-a",
        action="store_true",
        help="Append to existing CSV file instead of overwriting",
    )
    parser.add_argument(
        "--languages",
        "-l",
        type=str,
        nargs="+",
        help="Specific language codes to generate tests for (e.g., en fr de). Default: all languages",
    )
    parser.add_argument(
        "--sample",
        "-s",
        action="store_true",
        help="Generate a small sample (10 tests) for testing",
    )

    args = parser.parse_args()

    # Handle sample mode
    if args.sample:
        args.count = 10
        if not args.languages:
            args.languages = [
                "en",
                "fr",
                "es",
                "de",
                "ja",
            ]  # Sample of diverse languages
        print("Sample mode: Generating 10 test cases for", args.languages)

    # Check if file exists for append mode
    if args.append and os.path.exists(args.output):
        print(f"Appending to existing file: {args.output}")
    elif args.append:
        print(f"File {args.output} doesn't exist, creating new file")
        args.append = False
    elif os.path.exists(args.output):
        response = input(f"File {args.output} exists. Overwrite? (y/n): ")
        if response.lower() != "y":
            print("Aborted")
            sys.exit(0)

    print("\nSetting up OpenAI client...")
    client = setup_openai_client()

    print(f"Generating {args.count} sentence test cases...")
    if args.languages:
        print(f"Languages: {', '.join(args.languages)}")
    else:
        print("Languages: ALL available languages")

    test_cases = generate_sentence_test_cases(
        client, args.count, args.languages, args.model
    )

    if test_cases:
        print(f"\nGenerated {len(test_cases)} test cases")
        write_sentence_tests_to_csv(test_cases, args.output, args.append)
    else:
        print("Failed to generate test cases")
        sys.exit(1)


if __name__ == "__main__":
    main()
