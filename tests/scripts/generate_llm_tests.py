#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate test sentences with numbers using OpenAI for end-to-end testing.
This script creates realistic sentences containing numbers, dates, years, and currencies
and uses LLM to generate expected text conversions without using num2words library.
"""

import argparse
import csv
import json
import os
from typing import Dict, List

from openai import OpenAI

# List of all supported language codes and their names
LANGUAGE_MAPPING = {
    "af": "Afrikaans",
    "am": "Amharic",
    "ar": "Arabic",
    "as": "Assamese",
    "az": "Azerbaijani",
    "ba": "Bashkir",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bo": "Tibetan",
    "br": "Breton",
    "bs": "Bosnian",
    "ca": "Catalan",
    "ce": "Chechen",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "en_IN": "English (India)",
    "en_NG": "English (Nigeria)",
    "eo": "Esperanto",
    "es": "Spanish",
    "es_CO": "Spanish (Colombia)",
    "es_CR": "Spanish (Costa Rica)",
    "es_GT": "Spanish (Guatemala)",
    "es_NI": "Spanish (Nicaragua)",
    "es_VE": "Spanish (Venezuela)",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fo": "Faroese",
    "fr": "French",
    "fr_BE": "French (Belgium)",
    "fr_CH": "French (Switzerland)",
    "fr_DZ": "French (Algeria)",
    "gl": "Galician",
    "gu": "Gujarati",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "ht": "Haitian Creole",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "kz": "Kazakh",
    "la": "Latin",
    "lb": "Luxembourgish",
    "ln": "Lingala",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mg": "Malagasy",
    "mi": "Māori",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "mt": "Maltese",
    "my": "Burmese",
    "ne": "Nepali",
    "nl": "Dutch",
    "nn": "Norwegian Nynorsk",
    "no": "Norwegian",
    "oc": "Occitan",
    "pa": "Punjabi",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "pt_BR": "Portuguese (Brazil)",
    "ro": "Romanian",
    "ru": "Russian",
    "sa": "Sanskrit",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sn": "Shona",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "tet": "Tetum",
    "tg": "Tajik",
    "th": "Thai",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tr": "Turkish",
    "tt": "Tatar",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "wo": "Wolof",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zh": "Chinese",
    "zh_CN": "Chinese (Simplified)",
    "zh_HK": "Chinese (Hong Kong)",
    "zh_TW": "Chinese (Traditional)",
}

# Currency codes for different languages
CURRENCY_MAPPING = {
    "en": ["USD", "EUR", "GBP"],
    "fr": ["EUR", "USD", "CHF"],
    "de": ["EUR", "USD", "GBP"],
    "es": ["EUR", "USD", "MXN"],
    "pt": ["EUR", "BRL", "USD"],
    "pt_BR": ["BRL", "USD", "EUR"],
    "it": ["EUR", "USD", "GBP"],
    "ru": ["RUB", "USD", "EUR"],
    "ja": ["JPY", "USD", "EUR"],
    "zh": ["CNY", "USD", "EUR"],
    "zh_CN": ["CNY", "USD", "EUR"],
    "hi": ["INR", "USD", "EUR"],
    "mr": ["INR", "USD", "EUR"],
    "ar": ["SAR", "USD", "EUR"],
    # Add more as needed, default will be USD, EUR
}


def get_currency_for_language(lang_code: str) -> List[str]:
    """Get appropriate currencies for a language."""
    return CURRENCY_MAPPING.get(lang_code, ["USD", "EUR"])


def generate_test_samples(
    client: OpenAI,
    language: str,
    prompt: str,
    num_samples: int = 5,
    model: str = "gpt-4o",
    mode: str = "sentences",
) -> List[Dict]:
    """
    Generate test samples using OpenAI for a specific language.

    Args:
        client: OpenAI client
        language: Target language (e.g., 'French', 'Spanish')
        prompt: Custom prompt describing what to generate
        num_samples: Number of samples to generate
        model: OpenAI model to use (e.g., 'gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo')
        mode: 'sentences' for full sentences, 'numbers' for just number conversions

    Returns:
        List of dictionaries with test data
    """

    lang_name = LANGUAGE_MAPPING.get(language, language)
    currencies = get_currency_for_language(language)

    if mode == "numbers":
        # Numbers-only mode prompt
        system_prompt = f"""You are a language expert converting numbers to words in {lang_name}.
Provide direct number-to-word conversions without full sentences.

Your response must be valid JSON with this exact structure:
{{
    "samples": [
        {{
            "number": "42",
            "word_form": "forty-two",
            "number_type": "cardinal",
            "language_code": "{language}",
            "language_name": "{lang_name}"
        }}
    ]
}}"""
    else:
        # Sentences mode prompt
        system_prompt = f"""You are a language expert creating test sentences for number-to-words conversion in {lang_name}.
You must generate realistic sentences that contain numbers in various contexts.

IMPORTANT RULES:
1. Generate sentences in {lang_name} language
2. Include the original number in numeric form in the sentence
3. Provide the expected_output: The sentence with ALL numbers converted to words in {lang_name}
4. Numbers should appear naturally in context
5. For dates, use the format common in that language/culture
6. For currencies, use {', '.join(currencies)} with realistic amounts
7. Years should be between 1900-2030
8. Regular numbers can range from 0 to 999999

Your response must be valid JSON with this exact structure:
{{
    "samples": [
        {{
            "original_sentence": "The sentence with numbers like 42 or $10.50",
            "expected_output": "The sentence with forty-two or ten dollars and fifty cents",
            "sentence_translation": "The English translation of the original sentence",
            "numbers_found": ["42", "10.50"],
            "number_types": ["cardinal", "currency"]
        }}
    ]
}}
"""

    if mode == "numbers":
        user_prompt = f"""Generate {num_samples} number-to-word conversions in {lang_name} based on this instruction:
{prompt}

Include a variety of number types as appropriate."""
    else:
        user_prompt = f"""Generate {num_samples} test sentences in {lang_name} based on this instruction:
{prompt}

Include a variety of:
- Cardinal numbers (e.g., 42, 1234)
- Ordinal numbers (e.g., 1st, 2nd, 3rd)
- Years (e.g., 2024, 1999)
- Dates (e.g., January 15, 2024)
- Currency amounts (e.g., $10.50, €25.99)
- Negative numbers where appropriate
- Decimal numbers where appropriate

Make sentences realistic and diverse. Each sentence should test different aspects of number conversion."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=2000,
        )

        result = json.loads(response.choices[0].message.content)

        # Add language code to each sample
        for sample in result.get("samples", []):
            sample["language_code"] = language
            sample["language_name"] = lang_name

        return result.get("samples", [])

    except Exception as e:
        print(f"Error generating samples for {lang_name}: {e}")
        return []


def save_to_csv(
    samples: List[Dict],
    filename: str = None,
    mode: str = "sentences",
    append: bool = False,
):
    """
    Save generated samples to CSV file.

    Args:
        samples: List of sample dictionaries
        filename: Output CSV filename
        mode: Generation mode ('sentences' or 'numbers')
        append: Whether to append to existing file
    """
    if not filename:
        # Default filename based on mode
        if mode == "sentences":
            filename = "tests/data/e2e_test_sentences.csv"
        else:  # mode == 'numbers'
            filename = "tests/data/e2e_test_suite.csv"

    if not samples:
        print("No samples to save")
        return

    # Define CSV columns
    fieldnames = [
        "language_code",
        "language_name",
        "original_sentence",
        "expected_output",  # OpenAI's direct conversion
        "sentence_translation",  # English translation of the sentence
        "numbers_found",
        "number_types",
    ]

    # Check if we should append and file exists
    import os

    file_exists = os.path.exists(filename)
    write_mode = "a" if append and file_exists else "w"
    write_header = not (append and file_exists)

    with open(filename, write_mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        for sample in samples:
            # Convert lists to JSON strings for CSV storage
            if "numbers_found" in sample and isinstance(sample["numbers_found"], list):
                sample["numbers_found"] = json.dumps(sample["numbers_found"])
            if "number_types" in sample and isinstance(sample["number_types"], list):
                sample["number_types"] = json.dumps(sample["number_types"])

            # Write only the fields we want
            row = {field: sample.get(field, "") for field in fieldnames}
            writer.writerow(row)

    action = "Appended" if append and file_exists else "Saved"
    print(f"✅ {action} {len(samples)} samples to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate test sentences with numbers using OpenAI"
    )
    parser.add_argument(
        "--languages",
        type=str,
        help='Comma-separated language codes (e.g., "en,fr,es"). Leave empty for all languages.',
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Custom prompt describing what to generate (if not set, uses mode-specific defaults)",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=5,
        help="Number of samples to generate per language (default: 5)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output CSV filename (default: tests/data/e2e_test_sentences.csv for sentences mode, tests/data/e2e_test_suite.csv for numbers mode)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o, options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["sentences", "numbers"],
        default="sentences",
        help='Generation mode: "sentences" for full sentences with numbers, "numbers" for just number conversions',
    )
    parser.add_argument(
        "--append",
        action="store_true",
        default=True,
        help="Append to existing CSV file instead of overwriting (default: True)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing CSV file instead of appending",
    )

    args = parser.parse_args()

    # Setup OpenAI client
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OpenAI API key required. Set OPENAI_API_KEY or use --api-key")
        return

    client = OpenAI(api_key=api_key)

    # Determine which languages to process
    if args.languages:
        languages = [lang.strip() for lang in args.languages.split(",")]
    else:
        languages = list(LANGUAGE_MAPPING.keys())

    # Set default prompt based on mode if not provided
    if args.prompt is None:
        if args.mode == "sentences":
            args.prompt = "Generate diverse sentences with numbers, dates, currencies, and measurements"
        else:  # numbers mode
            args.prompt = "Generate various types of numbers: cardinal, ordinal, years, dates, currencies, decimals, negatives"

    print(f"🌍 Generating samples for {len(languages)} language(s)")
    print(f"🤖 Model: {args.model}")
    print(f"📝 Mode: {args.mode}")
    print(f"📝 Prompt: {args.prompt}")
    print(f"📊 Samples per language: {args.samples}")
    print("-" * 60)

    all_samples = []

    for lang_code in languages:
        lang_name = LANGUAGE_MAPPING.get(lang_code, lang_code)
        print(f"\n🔄 Processing {lang_name} ({lang_code})...")

        samples = generate_test_samples(
            client=client,
            language=lang_code,
            prompt=args.prompt,
            num_samples=args.samples,
            model=args.model,
            mode=args.mode,
        )

        if samples:
            print(f"   ✅ Generated {len(samples)} samples")
            all_samples.extend(samples)
        else:
            print("   ⚠️  No samples generated")

    # Save all samples to CSV
    if all_samples:
        print("\n" + "=" * 60)
        # Use overwrite flag to determine append behavior (append by default unless --overwrite is set)
        append = not args.overwrite
        save_to_csv(all_samples, args.output, mode=args.mode, append=append)
        print(f"\n📈 Total samples generated: {len(all_samples)}")
    else:
        print("\n❌ No samples were generated")


if __name__ == "__main__":
    main()
