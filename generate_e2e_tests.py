#!/usr/bin/env python3
"""Generate E2E test cases for new languages and append to e2e_test_suite.csv."""

import csv
import os
import sys
import time

from openai import OpenAI

from num2words2 import num2words

# Initialize OpenAI client
if not os.getenv('OPENAI_API_KEY'):
    print("Error: OPENAI_API_KEY environment variable not set!")
    print("Please set it with: export OPENAI_API_KEY='your-key-here'")
    sys.exit(1)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# List of all newly added languages
NEW_LANGUAGES = [
    ('af', 'Afrikaans'), ('am', 'Amharic'), ('as', 'Assamese'), ('ba', 'Bashkir'),
    ('be', 'Belarusian'), ('bg', 'Bulgarian'), ('bo', 'Tibetan'), ('br', 'Breton'),
    ('bs', 'Bosnian'), ('cy', 'Welsh'), ('et', 'Estonian'), ('eu', 'Basque'),
    ('fo', 'Faroese'), ('gl', 'Galician'), ('gu', 'Gujarati'), ('ha', 'Hausa'),
    ('haw', 'Hawaiian'), ('ht', 'Haitian Creole'), ('jw', 'Javanese'), ('ka', 'Georgian'),
    ('kk', 'Kazakh'), ('km', 'Khmer'), ('la', 'Latin'), ('lb', 'Luxembourgish'),
    ('ln', 'Lingala'), ('lo', 'Lao'), ('mg', 'Malagasy'), ('mi', 'Maori'),
    ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mr', 'Marathi'), ('ms', 'Malay'),
    ('mt', 'Maltese'), ('my', 'Myanmar'), ('ne', 'Nepali'), ('nn', 'Norwegian Nynorsk'),
    ('oc', 'Occitan'), ('pa', 'Punjabi'), ('ps', 'Pashto'), ('sa', 'Sanskrit'),
    ('sd', 'Sindhi'), ('si', 'Sinhala'), ('sn', 'Shona'), ('so', 'Somali'),
    ('su', 'Sundanese'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'),
    ('tg', 'Tajik'), ('tk', 'Turkmen'), ('tl', 'Tagalog'), ('tt', 'Tatar'),
    ('ur', 'Urdu'), ('uz', 'Uzbek'), ('wo', 'Wolof'), ('yi', 'Yiddish'),
    ('yo', 'Yoruba')
]


def get_default_currency(lang_code):
    """Get default currency for a language."""
    currencies = {
        'af': 'ZAR', 'am': 'ETB', 'as': 'INR', 'ba': 'RUB', 'be': 'BYN',
        'bg': 'BGN', 'bo': 'CNY', 'br': 'EUR', 'bs': 'BAM', 'cy': 'GBP',
        'et': 'EUR', 'eu': 'EUR', 'fo': 'DKK', 'gl': 'EUR', 'gu': 'INR',
        'ha': 'NGN', 'haw': 'USD', 'ht': 'HTG', 'jw': 'IDR', 'ka': 'GEL',
        'kk': 'KZT', 'km': 'KHR', 'la': 'EUR', 'lb': 'EUR', 'ln': 'CDF',
        'lo': 'LAK', 'mg': 'MGA', 'mi': 'NZD', 'mk': 'MKD', 'ml': 'INR',
        'mr': 'INR', 'ms': 'MYR', 'mt': 'EUR', 'my': 'MMK', 'ne': 'NPR',
        'nn': 'NOK', 'oc': 'EUR', 'pa': 'INR', 'ps': 'AFN', 'sa': 'INR',
        'sd': 'PKR', 'si': 'LKR', 'sn': 'ZWL', 'so': 'SOS', 'su': 'IDR',
        'sw': 'KES', 'ta': 'INR', 'te': 'INR', 'tg': 'TJS', 'tk': 'TMT',
        'tl': 'PHP', 'tt': 'RUB', 'ur': 'PKR', 'uz': 'UZS', 'wo': 'XOF',
        'yi': 'ILS', 'yo': 'NGN'
    }
    return currencies.get(lang_code, 'USD')


def generate_test_cases_for_language(lang_code, lang_name):
    """Generate test cases for a specific language."""
    test_cases = []

    # Test numbers for each type
    cardinal_numbers = [0, 7, 42, 137, 1984, 50023, 2000000, -15, -876, 0.5, 3.14, -2.75]
    ordinal_numbers = [1, 3, 21, 100, 1523]
    ordinal_num_numbers = [1, 2, 3, 4, 11, 21, 32, 103]
    currency_amounts = [(1.50, 'main'), (0.25, 'main'), (1000.00, 'main'), (42.99, 'main'),
                        (5.00, 'EUR'), (27.50, 'EUR'), (10.00, 'GBP'), (0.01, 'GBP')]
    year_numbers = [1984, 2023, 1900, 2001]

    # Generate cardinal tests
    for num in cardinal_numbers:
        try:
            expected = num2words(num, lang=lang_code, to='cardinal')
            test_cases.append({
                'language': lang_code,
                'number': str(num),
                'conversion_type': 'cardinal',
                'currency': '',
                'expected_output': expected
            })
        except Exception as e:
            print(f"  Warning: Failed cardinal for {num} in {lang_code}: {e}")

    # Generate ordinal tests
    for num in ordinal_numbers:
        try:
            expected = num2words(num, lang=lang_code, to='ordinal')
            test_cases.append({
                'language': lang_code,
                'number': str(num),
                'conversion_type': 'ordinal',
                'currency': '',
                'expected_output': expected
            })
        except Exception as e:
            print(f"  Warning: Failed ordinal for {num} in {lang_code}: {e}")

    # Generate ordinal_num tests
    for num in ordinal_num_numbers:
        try:
            expected = num2words(num, lang=lang_code, to='ordinal_num')
            test_cases.append({
                'language': lang_code,
                'number': str(num),
                'conversion_type': 'ordinal_num',
                'currency': '',
                'expected_output': expected
            })
        except Exception as e:
            print(f"  Warning: Failed ordinal_num for {num} in {lang_code}: {e}")

    # Generate currency tests
    default_currency = get_default_currency(lang_code)
    for amount, curr_type in currency_amounts:
        try:
            currency = default_currency if curr_type == 'main' else curr_type
            expected = num2words(amount, lang=lang_code, to='currency', currency=currency)
            test_cases.append({
                'language': lang_code,
                'number': str(amount),
                'conversion_type': 'currency',
                'currency': currency,
                'expected_output': expected
            })
        except Exception as e:
            print(f"  Warning: Failed currency for {amount} {currency} in {lang_code}: {e}")

    # Generate year tests
    for num in year_numbers:
        try:
            expected = num2words(num, lang=lang_code, to='year')
            test_cases.append({
                'language': lang_code,
                'number': str(num),
                'conversion_type': 'year',
                'currency': '',
                'expected_output': expected
            })
        except Exception as e:
            print(f"  Warning: Failed year for {num} in {lang_code}: {e}")

    return test_cases


def main():
    """Main function to generate and append test cases."""
    print("=" * 70)
    print("GENERATING E2E TEST CASES FOR NEW LANGUAGES")
    print("=" * 70)

    # Read existing test suite to check what we already have
    existing_file = '/Users/jean-louisqueguiner/dev/n2w_add_languages/tests/e2e_test_suite.csv'
    existing_tests = set()

    if os.path.exists(existing_file):
        with open(existing_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Create unique key for existing tests
                key = (row.get('language', ''), row.get('number', ''),
                       row.get('conversion_type', ''), row.get('currency', ''))
                existing_tests.add(key)
        print(f"Found {len(existing_tests)} existing test cases")

    # Generate test cases for all new languages
    all_new_tests = []
    languages_processed = 0

    for lang_code, lang_name in NEW_LANGUAGES:
        print(f"\nProcessing {lang_name} ({lang_code})...")
        test_cases = generate_test_cases_for_language(lang_code, lang_name)

        # Filter out duplicates
        new_tests = []
        for tc in test_cases:
            key = (tc['language'], tc['number'], tc['conversion_type'], tc['currency'])
            if key not in existing_tests:
                new_tests.append(tc)
                existing_tests.add(key)

        if new_tests:
            all_new_tests.extend(new_tests)
            print(f"  Generated {len(new_tests)} new test cases")
        else:
            print(f"  No new test cases needed (already exist)")

        languages_processed += 1

        # Add small delay to avoid rate limits
        if languages_processed % 10 == 0:
            time.sleep(0.5)

    # Append new tests to the existing file
    if all_new_tests:
        print(f"\n" + "=" * 70)
        print(f"Appending {len(all_new_tests)} new test cases to e2e_test_suite.csv")

        fieldnames = ['language', 'number', 'conversion_type', 'currency', 'expected_output']

        with open(existing_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(all_new_tests)

        print(f"✅ Successfully added {len(all_new_tests)} test cases!")
    else:
        print("\n✅ All test cases already exist, no additions needed")

    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Languages processed: {languages_processed}")
    print(f"New test cases added: {len(all_new_tests)}")

    if all_new_tests:
        # Count by conversion type
        type_counts = {}
        for tc in all_new_tests:
            ct = tc['conversion_type']
            type_counts[ct] = type_counts.get(ct, 0) + 1

        print("\nNew tests by type:")
        for ct, count in sorted(type_counts.items()):
            print(f"  {ct:12}: {count:4} tests")

        # Count by language
        lang_counts = {}
        for tc in all_new_tests:
            lang = tc['language']
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        print(f"\nLanguages with new tests: {len(lang_counts)}")


if __name__ == "__main__":
    main()
