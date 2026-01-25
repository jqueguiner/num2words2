#!/usr/bin/env python
"""
Generate test cases for num2words using OpenAI API
Usage: python generate_tests_with_ai.py --prompt "Your prompt here" [--output tests/e2e_test_suite.csv] [--count 100]
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
    # Complete list of all available languages from num2words2
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


def setup_openai_client():
    """Setup OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    return OpenAI(api_key=api_key)


def generate_test_cases(
    client: OpenAI,
    prompt: str,
    count: int = 100,
    languages: Optional[List[str]] = None,
    model: str = "gpt-4",
) -> List[Dict]:
    """Generate test cases using OpenAI API, handling large counts by batching"""

    system_prompt = """You are a test case generator for the num2words library.
    Generate test cases in JSON format with the following structure:
    [
        {
            "number": <numeric value>,
            "lang": "<language code>",
            "expected": "<expected text output>",
            "to": "<'cardinal', 'ordinal', 'currency', or 'year'>",
            "currency": "<currency code if to='currency', otherwise null>"
        }
    ]

    Language codes: {langs}
    Currency codes include: USD, EUR, GBP, JPY, CNY, etc.

    Generate diverse test cases including:
    - Small and large numbers
    - Decimals and negative numbers
    - Different languages
    - Cardinal, ordinal, currency, and year formats
    - Edge cases like 0, 1, very large numbers

    Return ONLY the JSON array, no additional text."""

    # Get languages to test
    if languages is None:
        test_langs = get_all_languages()
        lang_spec = "for ALL available languages in num2words"
    else:
        test_langs = languages
        lang_spec = f"ONLY for these specific languages: {', '.join(test_langs)}"

    # Format language list for system prompt
    lang_str = ", ".join(test_langs[:30]) + (
        f" and {len(test_langs)-30} more" if len(test_langs) > 30 else ""
    )
    system_prompt_formatted = system_prompt.replace("{langs}", lang_str)

    # Generate in batches for large counts
    batch_size = 20  # Smaller batches for reliability
    all_test_cases = []

    # Determine max tokens based on model
    model_limits = {
        "gpt-4": 3500,
        "gpt-4-turbo": 3500,
        "gpt-4-turbo-preview": 3500,
        "gpt-3.5-turbo": 3500,
        "gpt-4o": 12000,
        "gpt-4o-mini": 12000,
    }
    max_tokens = model_limits.get(model, 3000)

    while len(all_test_cases) < count:
        remaining = count - len(all_test_cases)
        current_batch = min(batch_size, remaining)

        # Add language specification to user prompt
        user_prompt = f"{prompt}\n\nGenerate EXACTLY {current_batch} diverse test cases {lang_spec}. Ensure the generated tests cover a good distribution across the specified languages. Return ONLY the JSON array."

        try:
            print(f"  Requesting batch of {current_batch} test cases...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt_formatted},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=max_tokens,
            )

            # Parse the JSON response
            content = response.choices[0].message.content
            # Clean up the content (remove any markdown code blocks if present)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            test_cases = json.loads(content.strip())

            if isinstance(test_cases, list):
                all_test_cases.extend(test_cases)
                print(
                    f"  Generated batch: {len(test_cases)} test cases (Total: {len(all_test_cases)}/{count})"
                )
            else:
                print(f"Warning: Expected list but got {type(test_cases)}")

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from OpenAI response: {e}")
            print(
                "Response content preview:",
                content[:500] if "content" in locals() else "No content",
            )
            # Try to continue with partial results
            if all_test_cases:
                print(
                    f"Continuing with {len(all_test_cases)} test cases generated so far"
                )
                break
            else:
                return []
        except Exception as e:
            print(f"Error generating test cases: {e}")
            # Try to continue with partial results
            if all_test_cases:
                print(
                    f"Continuing with {len(all_test_cases)} test cases generated so far"
                )
                break
            else:
                return []

    return all_test_cases[:count]  # Ensure we don't exceed requested count


def write_to_csv(test_cases: List[Dict], output_file: str, append: bool = False):
    """Write test cases to CSV file, with option to append"""

    if not test_cases:
        print("No test cases to write")
        return

    # Define CSV headers
    headers = ["number", "lang", "expected", "to", "currency", "english_translation"]

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
                    "number": case.get("number", ""),
                    "lang": case.get("lang", ""),
                    "expected": case.get("expected", ""),
                    "to": case.get("to", "cardinal"),
                    "currency": case.get("currency", ""),
                    "english_translation": "",  # Will be filled by translate script
                }
                writer.writerow(row)

        print(f"Successfully wrote {len(test_cases)} test cases to {output_file}")

    except Exception as e:
        print(f"Error writing to CSV: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate num2words test cases using OpenAI"
    )
    parser.add_argument(
        "--prompt",
        "-p",
        type=str,
        required=True,
        help="Prompt for generating test cases",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="tests/e2e_test_suite.csv",
        help="Output CSV file (default: tests/e2e_test_suite.csv)",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=100,
        help="Number of test cases to generate (default: 100)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="gpt-4",
        help="OpenAI model to use (default: gpt-4). Try gpt-4o or gpt-4o-mini for higher token limits",
    )
    parser.add_argument(
        "--append",
        "-a",
        action="store_true",
        default=True,
        help="Append to existing CSV file (default: True)",
    )
    parser.add_argument(
        "--override",
        "--overwrite",
        action="store_true",
        help="Override/overwrite the existing CSV file (default: append mode)",
    )
    parser.add_argument(
        "--languages",
        "-l",
        type=str,
        nargs="+",
        help="Specific language codes to generate tests for (e.g., en fr de). Default: all languages",
    )

    args = parser.parse_args()

    # Handle append/override logic
    if args.override:
        args.append = False  # Override means don't append
        print("WARNING: Override mode - will overwrite existing file!")
        if os.path.exists(args.output):
            response = input(f"File {args.output} exists. Overwrite? (y/n): ")
            if response.lower() != "y":
                print("Aborted")
                sys.exit(0)
    else:
        args.append = True  # Default is to append
        if os.path.exists(args.output):
            print(f"Appending to existing file: {args.output}")
        else:
            print(f"Creating new file: {args.output}")
            args.append = False  # First write, don't append

    print("\nSetting up OpenAI client...")
    client = setup_openai_client()

    print(f"Generating {args.count} test cases with prompt: {args.prompt[:100]}...")
    test_cases = generate_test_cases(
        client, args.prompt, args.count, args.languages, args.model
    )

    if test_cases:
        print(f"Generated {len(test_cases)} test cases")
        write_to_csv(test_cases, args.output, args.append)
    else:
        print("Failed to generate test cases")
        sys.exit(1)


if __name__ == "__main__":
    main()
