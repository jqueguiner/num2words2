#!/usr/bin/env python
"""
Fix test expectations in e2e_test_suite.csv to match actual library behavior
This script runs each test case and updates the expected value with the actual output
"""

import argparse
import csv
import sys
from typing import Dict

from num2words2 import num2words


def parse_number(number_str: str):
    """Parse number string to appropriate type"""
    try:
        if 'e' in number_str.lower() or 'E' in number_str or '.' in number_str:
            return float(number_str)
        else:
            return int(number_str)
    except ValueError:
        return number_str


def get_actual_output(row: Dict) -> str:
    """Get the actual output from num2words for a test case"""
    try:
        number = parse_number(row['number'])
        lang = row['lang']
        to_type = row['to']
        currency = row.get('currency', '').strip()

        # Build kwargs
        kwargs = {'lang': lang}

        if to_type == 'cardinal':
            kwargs['to'] = 'cardinal'
        elif to_type == 'ordinal':
            kwargs['to'] = 'ordinal'
        elif to_type == 'ordinal_num':
            kwargs['to'] = 'ordinal_num'
        elif to_type == 'year':
            kwargs['to'] = 'year'
        elif to_type == 'currency':
            kwargs['to'] = 'currency'
            if currency:
                kwargs['currency'] = currency

        # Get actual output
        return num2words(number, **kwargs)
    except Exception as e:
        return f"ERROR: {str(e)}"


def fix_expectations(input_file: str, output_file: str = None, dry_run: bool = False,
                     filter_lang: str = None, limit: int = None):
    """Fix expectations in CSV file"""

    if output_file is None:
        output_file = input_file

    print(f"Reading from: {input_file}")

    # Read all rows
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        for row in reader:
            rows.append(row)

    print(f"Found {len(rows)} total rows")

    # Track statistics
    fixed = 0
    already_correct = 0
    errors = 0
    changes = []

    # Process rows
    for i, row in enumerate(rows):
        if limit and i >= limit:
            break

        # Apply language filter if specified
        if filter_lang and row['lang'] != filter_lang:
            continue

        # Skip empty rows
        if not row.get('lang') or not row.get('number'):
            continue

        # Get actual output
        actual = get_actual_output(row)
        expected = row['expected']

        if "ERROR:" in actual:
            errors += 1
            print(f"Error in row {i+1} ({row['lang']}, {row['number']}): {actual}")
            continue

        # Check if needs fixing
        if actual != expected:
            if not dry_run:
                row['expected'] = actual
            fixed += 1
            changes.append({
                'row': i + 1,
                'lang': row['lang'],
                'number': row['number'],
                'to': row['to'],
                'old': expected,
                'new': actual
            })

            # Show progress for significant changes
            if fixed <= 10 or fixed % 10 == 0:
                print(f"Fixed row {i+1} ({row['lang']}): {row['number']}")
                print(f"  Old: {expected}")
                print(f"  New: {actual}")
        else:
            already_correct += 1

    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total rows processed: {len(rows) if not limit else min(limit, len(rows))}")
    print(f"Already correct: {already_correct}")
    print(f"Fixed: {fixed}")
    print(f"Errors: {errors}")

    if dry_run:
        print("\nDRY RUN MODE - No changes were saved")
        print("\nSample of changes that would be made (first 10):")
        for change in changes[:10]:
            print(f"\nRow {change['row']} ({change['lang']}) - {change['number']} [{change['to']}]:")
            print(f"  Old: {change['old']}")
            print(f"  New: {change['new']}")
    else:
        # Write results
        print(f"\nWriting fixed results to: {output_file}")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Successfully updated {fixed} test expectations")

    return fixed, already_correct, errors


def main():
    parser = argparse.ArgumentParser(description='Fix test expectations to match actual library output')
    parser.add_argument('--input', '-i', type=str, default='tests/e2e_test_suite.csv',
                        help='Input CSV file (default: tests/e2e_test_suite.csv)')
    parser.add_argument('--output', '-o', type=str,
                        help='Output CSV file (default: same as input)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show what would be changed without modifying files')
    parser.add_argument('--lang', '-l', type=str,
                        help='Only fix expectations for a specific language')
    parser.add_argument('--limit', type=int,
                        help='Limit number of rows to process')

    args = parser.parse_args()

    if not args.dry_run and args.output is None:
        print("WARNING: This will modify the input file directly!")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            print("Aborted")
            sys.exit(0)

    fix_expectations(args.input, args.output, args.dry_run, args.lang, args.limit)


if __name__ == "__main__":
    main()
