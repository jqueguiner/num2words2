#!/usr/bin/env python
"""
Translate the 'expected' column of e2e_test_suite.csv to English
and populate the 'english_translation' column using OpenAI GPT-4
"""

import argparse
import csv
import os
import sys
import time
from typing import Dict, List

from openai import OpenAI


def setup_openai_client():
    """Setup OpenAI client with API key from environment"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    return OpenAI(api_key=api_key)


def translate_batch(client: OpenAI, rows: List[Dict], model: str = "gpt-4", force: bool = False) -> List[str]:
    """Translate a batch of rows to English"""

    # Skip rows that already have translations or are already in English
    to_translate = []
    translations = []

    for row in rows:
        if not force and row.get('english_translation') and row['english_translation'].strip():
            # Already has translation (skip unless force mode)
            translations.append(row['english_translation'])
        elif row['lang'] == 'en':
            # Already in English, copy the expected value
            translations.append(row['expected'])
        else:
            to_translate.append(row)
            translations.append(None)  # Placeholder

    if not to_translate:
        return translations

    # Build prompt for batch translation
    prompt_lines = []
    for i, row in enumerate(to_translate):
        prompt_lines.append(f"{i+1}. Language: {row['lang']}, Text: \"{row['expected']}\"")

    prompt = "\n".join(prompt_lines)

    system_prompt = """You are a translator for the num2words library test suite.
    Translate the given text representations of numbers from various languages to English.

    IMPORTANT RULES:
    1. Keep the exact same format (cardinal, ordinal, currency, etc.)
    2. For currencies, translate the number part but keep currency names in English
    3. Return ONLY the translations, one per line, numbered to match the input
    4. If a text is already in English, return it unchanged
    5. Preserve capitalization patterns

    Example:
    Input: 1. Language: fr, Text: "un"
    Output: 1. one

    Input: 2. Language: es, Text: "ciento veintitrés"
    Output: 2. one hundred twenty-three"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Translate these number representations to English:\n\n{prompt}"}
            ],
            temperature=0.3,
            max_tokens=4000
        )

        # Parse response
        response_text = response.choices[0].message.content
        response_lines = response_text.strip().split('\n')

        # Extract translations
        trans_dict = {}
        for line in response_lines:
            if '. ' in line:
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    try:
                        idx = int(parts[0]) - 1
                        trans_dict[idx] = parts[1].strip()
                    except ValueError:
                        continue

        # Fill in translations
        trans_idx = 0
        for i, trans in enumerate(translations):
            if trans is None and trans_idx in trans_dict:
                translations[i] = trans_dict[trans_idx]
                trans_idx += 1
            elif trans is None:
                translations[i] = ""  # Failed to get translation
                trans_idx += 1

        return translations

    except Exception as e:
        print(f"Error in translation: {e}")
        # Return empty translations for failed batch
        return ["" if t is None else t for t in translations]


def translate_csv_file(input_file: str, output_file: str = None, batch_size: int = 20, model: str = "gpt-4", force: bool = False):
    """Translate all rows in the CSV file"""

    if output_file is None:
        output_file = input_file

    print(f"Reading from: {input_file}")
    print(f"Will write to: {output_file}")

    # Read all rows
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        # Ensure english_translation column exists
        if 'english_translation' not in headers:
            print("Error: 'english_translation' column not found in CSV")
            sys.exit(1)

        for row in reader:
            rows.append(row)

    print(f"Found {len(rows)} total rows")

    # Count how many need translation
    need_translation = 0
    already_translated = 0
    english_rows = 0

    for row in rows:
        if row['lang'] == 'en':
            english_rows += 1
        elif not force and row.get('english_translation') and row['english_translation'].strip():
            already_translated += 1
        else:
            need_translation += 1

    print(f"\nTranslation status:")
    print(f"  Already translated: {already_translated}")
    print(f"  English rows (skip): {english_rows}")
    print(f"  Need translation: {need_translation}")

    if need_translation == 0:
        print("\nAll rows are already translated! Nothing to do.")
        return

    print(f"\nWill translate {need_translation} rows...")

    # Setup OpenAI client
    client = setup_openai_client()

    # Process in batches
    total_translated = 0
    skipped_batches = 0

    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]

        # Check if this entire batch already has translations
        needs_translation = False
        for row in batch:
            if row['lang'] != 'en' and (force or not row.get('english_translation') or not row['english_translation'].strip()):
                needs_translation = True
                break

        if not needs_translation:
            skipped_batches += 1
            print(f"\nSkipping batch {i//batch_size + 1} (rows {i+1}-{min(i+batch_size, len(rows))}) - already translated")
            continue

        print(f"\nProcessing batch {i//batch_size + 1} (rows {i+1}-{min(i+batch_size, len(rows))})")

        # Count how many need translation in this batch
        need_trans_count = sum(1 for row in batch
                               if row['lang'] != 'en' and (force or not row.get('english_translation') or not row['english_translation'].strip()))
        print(f"  {need_trans_count} rows need translation in this batch")

        # Get translations
        translations = translate_batch(client, batch, model, force)

        # Update rows
        newly_translated = 0
        for j, trans in enumerate(translations):
            if trans and (force or not rows[i + j].get('english_translation')):
                rows[i + j]['english_translation'] = trans
                total_translated += 1
                newly_translated += 1

        print(f"  Newly translated: {newly_translated} rows")

        # Small delay to avoid rate limits
        if i + batch_size < len(rows):
            time.sleep(0.5)

    # Write back to CSV
    print(f"\nWriting results to: {output_file}")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nTranslation complete!")
    print(f"Skipped {skipped_batches} batches that were already translated")
    print(f"Total rows newly translated: {total_translated}")

    # Show some examples
    print("\nSample translations:")
    sample_count = 0
    for row in rows:
        if row.get('english_translation') and row['lang'] != 'en' and sample_count < 5:
            print(f"  {row['lang']}: \"{row['expected']}\" -> \"{row['english_translation']}\"")
            sample_count += 1


def main():
    parser = argparse.ArgumentParser(description='Translate num2words test cases to English')
    parser.add_argument('--input', '-i', type=str, default='tests/e2e_test_suite.csv',
                        help='Input CSV file (default: tests/e2e_test_suite.csv)')
    parser.add_argument('--output', '-o', type=str,
                        help='Output CSV file (default: same as input)')
    parser.add_argument('--batch-size', '-b', type=int, default=20,
                        help='Batch size for translation (default: 20)')
    parser.add_argument('--model', '-m', type=str, default='gpt-4',
                        help='OpenAI model to use (default: gpt-4)')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Force retranslation of already translated rows')

    args = parser.parse_args()

    if args.force:
        print("WARNING: Force mode will overwrite existing translations!")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            print("Aborted")
            sys.exit(0)

    translate_csv_file(args.input, args.output, args.batch_size, args.model, args.force)


if __name__ == "__main__":
    main()
