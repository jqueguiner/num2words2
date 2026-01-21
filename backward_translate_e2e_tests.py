#!/usr/bin/env python
"""
Backward translate test cases - from English back to target languages
This helps generate 'expected' values for test cases where we have English translations
"""

import argparse
import csv
import os
import sys
import time
from typing import Dict, List

from openai import OpenAI

# Language name mappings for better prompts
LANGUAGE_NAMES = {
    'af': 'Afrikaans', 'am': 'Amharic', 'ar': 'Arabic', 'as': 'Assamese',
    'az': 'Azerbaijani', 'ba': 'Bashkir', 'be': 'Belarusian', 'bg': 'Bulgarian',
    'bn': 'Bengali', 'bo': 'Tibetan', 'br': 'Breton', 'bs': 'Bosnian',
    'ca': 'Catalan', 'ce': 'Chechen', 'cs': 'Czech', 'cy': 'Welsh',
    'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English',
    'eo': 'Esperanto', 'es': 'Spanish', 'et': 'Estonian', 'eu': 'Basque',
    'fa': 'Persian/Farsi', 'fi': 'Finnish', 'fo': 'Faroese', 'fr': 'French',
    'gl': 'Galician', 'gu': 'Gujarati', 'ha': 'Hausa', 'haw': 'Hawaiian',
    'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 'ht': 'Haitian Creole',
    'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'is': 'Icelandic',
    'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'ka': 'Georgian',
    'kk': 'Kazakh', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean',
    'kz': 'Kazakh', 'la': 'Latin', 'lb': 'Luxembourgish', 'ln': 'Lingala',
    'lo': 'Lao', 'lt': 'Lithuanian', 'lv': 'Latvian', 'mg': 'Malagasy',
    'mi': 'Maori', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mn': 'Mongolian',
    'mr': 'Marathi', 'ms': 'Malay', 'mt': 'Maltese', 'my': 'Myanmar/Burmese',
    'ne': 'Nepali', 'nl': 'Dutch', 'nn': 'Norwegian Nynorsk', 'no': 'Norwegian',
    'oc': 'Occitan', 'pa': 'Punjabi', 'pl': 'Polish', 'ps': 'Pashto',
    'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sa': 'Sanskrit',
    'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian',
    'sn': 'Shona', 'so': 'Somali', 'sq': 'Albanian', 'sr': 'Serbian',
    'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil',
    'te': 'Telugu', 'tet': 'Tetum', 'tg': 'Tajik', 'th': 'Thai',
    'tk': 'Turkmen', 'tl': 'Tagalog', 'tr': 'Turkish', 'tt': 'Tatar',
    'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese',
    'wo': 'Wolof', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zh': 'Chinese',
    'zh-cn': 'Chinese (Simplified)', 'zh-hk': 'Chinese (Hong Kong)',
    'zh-tw': 'Chinese (Traditional)', 'pt-br': 'Portuguese (Brazilian)',
    'es-co': 'Spanish (Colombia)', 'es-cr': 'Spanish (Costa Rica)',
    'es-gt': 'Spanish (Guatemala)', 'es-ni': 'Spanish (Nicaragua)',
    'es-ve': 'Spanish (Venezuela)', 'en-in': 'English (India)',
    'en-ng': 'English (Nigeria)', 'fr-be': 'French (Belgium)',
    'fr-ch': 'French (Switzerland)', 'fr-dz': 'French (Algeria)'
}


def setup_openai_client():
    """Setup OpenAI client with API key from environment"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    return OpenAI(api_key=api_key)


def backward_translate_batch(client: OpenAI, rows: List[Dict], model: str = "gpt-4", validate: bool = False) -> List[str]:
    """Translate from English to target languages"""

    # Group by target language for more efficient translation
    lang_groups = {}
    for i, row in enumerate(rows):
        lang = row['lang']
        if lang == 'en':
            continue  # Skip English rows

        if lang not in lang_groups:
            lang_groups[lang] = []
        lang_groups[lang].append((i, row))

    # Results array
    translations = [None] * len(rows)

    # For English rows, just copy the expected value
    for i, row in enumerate(rows):
        if row['lang'] == 'en':
            translations[i] = row.get('expected', row.get('english_translation', ''))

    # Process each language group
    for lang, items in lang_groups.items():
        if not items:
            continue

        lang_name = LANGUAGE_NAMES.get(lang, lang.upper())

        # Build prompt
        prompt_lines = []
        for idx, (orig_idx, row) in enumerate(items):
            english_text = row.get('english_translation', '') or row.get('expected', '')
            if english_text:
                prompt_lines.append(f"{idx+1}. \"{english_text}\"")

        if not prompt_lines:
            continue

        prompt = "\n".join(prompt_lines)

        system_prompt = f"""You are an expert translator for the num2words library.
        Translate number words from English to {lang_name} ({lang}).

        CRITICAL RULES:
        1. Translate ONLY the number words, maintaining the exact numerical meaning
        2. Use the proper {lang_name} number word conventions
        3. For cardinal numbers: use standard {lang_name} number words
        4. For ordinal numbers: use {lang_name} ordinal forms
        5. For currency: translate the number part to {lang_name}, keep currency indicators
        6. Maintain lowercase unless the language requires capitalization
        7. Return ONLY the translations, one per line, numbered to match input
        8. Be extremely precise - these are test cases that must match exactly

        Examples for {lang_name}:
        - Cardinal: "one" -> appropriate {lang_name} word for 1
        - Ordinal: "first" -> appropriate {lang_name} ordinal for 1st
        - Large numbers: follow {lang_name} conventions for thousands, millions, etc.
        """

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate these English number words to {lang_name}:\n\n{prompt}"}
                ],
                temperature=0.2,  # Lower temperature for more consistent translations
                max_tokens=4000
            )

            # Parse response
            response_text = response.choices[0].message.content
            response_lines = response_text.strip().split('\n')

            # Extract translations
            for line in response_lines:
                if '. ' in line:
                    parts = line.split('. ', 1)
                    if len(parts) == 2:
                        try:
                            idx = int(parts[0]) - 1
                            if idx < len(items):
                                orig_idx = items[idx][0]
                                translations[orig_idx] = parts[1].strip().strip('"')
                        except ValueError:
                            continue

        except Exception as e:
            print(f"  Error translating to {lang_name}: {e}")

    # Fill in any missing translations with empty string
    for i in range(len(translations)):
        if translations[i] is None:
            translations[i] = ""

    return translations


def backward_translate_csv(input_file: str, output_file: str = None, batch_size: int = 20,
                           model: str = "gpt-4", validate: bool = False, overwrite: bool = False):
    """Backward translate CSV file from English to target languages"""

    if output_file is None:
        # Create a new filename
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_backward{ext}"

    print(f"Reading from: {input_file}")
    print(f"Will write to: {output_file}")

    # Read all rows
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        for row in reader:
            rows.append(row)

    print(f"Found {len(rows)} rows to process")

    # Setup OpenAI client
    client = setup_openai_client()

    # Process in batches
    total_translated = 0
    validation_matches = 0
    validation_mismatches = []

    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]

        # Check if we need to process this batch
        needs_processing = False
        for row in batch:
            if row['lang'] != 'en':
                if overwrite or not row.get('expected'):
                    needs_processing = True
                    break
                elif validate and row.get('english_translation'):
                    needs_processing = True
                    break

        if not needs_processing:
            print(f"\nSkipping batch {i//batch_size + 1} (rows {i+1}-{min(i+batch_size, len(rows))})")
            continue

        print(f"\nProcessing batch {i//batch_size + 1} (rows {i+1}-{min(i+batch_size, len(rows))})")

        # Get backward translations
        translations = backward_translate_batch(client, batch, model, validate)

        # Update rows
        newly_translated = 0
        for j, trans in enumerate(translations):
            if trans:
                row_idx = i + j

                if validate and rows[row_idx].get('expected'):
                    # Validation mode - compare with existing
                    if trans.lower() == rows[row_idx]['expected'].lower():
                        validation_matches += 1
                    else:
                        validation_mismatches.append({
                            'row': row_idx + 1,
                            'lang': rows[row_idx]['lang'],
                            'number': rows[row_idx]['number'],
                            'original': rows[row_idx]['expected'],
                            'backward': trans,
                            'english': rows[row_idx].get('english_translation', '')
                        })

                if overwrite or not rows[row_idx].get('expected'):
                    rows[row_idx]['expected'] = trans
                    newly_translated += 1
                    total_translated += 1

        print(f"  Translated: {newly_translated} rows")

        # Small delay to avoid rate limits
        if i + batch_size < len(rows):
            time.sleep(0.5)

    # Write results
    print(f"\nWriting results to: {output_file}")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nBackward translation complete!")
    print(f"Total rows translated: {total_translated}")

    if validate:
        print(f"\nValidation Results:")
        print(f"  Matches: {validation_matches}")
        print(f"  Mismatches: {len(validation_mismatches)}")

        if validation_mismatches:
            print("\nSample mismatches (first 10):")
            for mm in validation_mismatches[:10]:
                print(f"  Row {mm['row']} ({mm['lang']}): {mm['number']}")
                print(f"    Original:  {mm['original']}")
                print(f"    Backward:  {mm['backward']}")
                print(f"    English:   {mm['english']}")


def main():
    parser = argparse.ArgumentParser(description='Backward translate test cases from English to target languages')
    parser.add_argument('--input', '-i', type=str, default='tests/e2e_test_suite.csv',
                        help='Input CSV file (default: tests/e2e_test_suite.csv)')
    parser.add_argument('--output', '-o', type=str,
                        help='Output CSV file (default: input_backward.csv)')
    parser.add_argument('--batch-size', '-b', type=int, default=20,
                        help='Batch size for translation (default: 20)')
    parser.add_argument('--model', '-m', type=str, default='gpt-4',
                        help='OpenAI model to use (default: gpt-4)')
    parser.add_argument('--validate', '-v', action='store_true',
                        help='Validate backward translations against original expected values')
    parser.add_argument('--overwrite', '-w', action='store_true',
                        help='Overwrite existing expected values')

    args = parser.parse_args()

    if args.overwrite:
        print("WARNING: Overwrite mode will replace existing 'expected' values!")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            print("Aborted")
            sys.exit(0)

    backward_translate_csv(args.input, args.output, args.batch_size, args.model,
                           args.validate, args.overwrite)


if __name__ == "__main__":
    main()
