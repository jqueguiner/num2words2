#!/usr/bin/env python3
"""Run E2E tests from the CSV file and show results"""

import csv

from num2words2 import num2words


def run_csv_tests():
    """Run tests from e2e_test_suite.csv"""
    csv_file = 'tests/e2e_test_suite.csv'

    passed = 0
    failed = 0
    failures = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            lang = row['lang']
            # Handle scientific notation and decimals
            try:
                if 'e' in row['number'].lower() or 'E' in row['number'] or '.' in row['number']:
                    number = float(row['number'])
                else:
                    number = int(row['number'])
            except ValueError:
                number = row['number']  # Keep as string if can't parse
            test_type = row['to']
            expected = row['expected']
            english_translation = row.get('english_translation', '')

            # Prepare kwargs
            kwargs = {'lang': lang}

            if test_type == 'cardinal':
                kwargs['to'] = 'cardinal'
            elif test_type == 'ordinal':
                kwargs['to'] = 'ordinal'
            elif test_type == 'ordinal_num':
                kwargs['to'] = 'ordinal_num'
            elif test_type == 'currency':
                kwargs['to'] = 'currency'
                if 'currency' in row and row['currency']:
                    kwargs['currency'] = row['currency']
            elif test_type == 'year':
                kwargs['to'] = 'year'

            try:
                actual = num2words(number, **kwargs)

                if actual == expected:
                    passed += 1
                else:
                    failed += 1
                    failures.append({
                        'lang': lang,
                        'number': number,
                        'type': test_type,
                        'expected': expected,
                        'actual': actual,
                        'english_translation': english_translation
                    })
            except Exception as e:
                failed += 1
                failures.append({
                    'lang': lang,
                    'number': number,
                    'type': test_type,
                    'expected': expected,
                    'actual': f"ERROR: {str(e)}",
                    'english_translation': english_translation
                })

    # Print summary
    total = passed + failed
    print("=" * 80)
    print("E2E TEST RESULTS FROM CSV")
    print("=" * 80)
    print(f"Total tests: {total}")
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print(f"Success rate: {passed/total*100:.1f}%")

    if failures and failed <= 20:
        print("\n" + "=" * 80)
        print("FAILED TESTS:")
        print("=" * 80)
        for i, f in enumerate(failures[:20], 1):
            print(f"\n{i}. {f['lang'].upper()} - {f['number']} ({f['type']})")
            print(f"   Expected: {f['expected']}")
            if f.get('english_translation'):
                print(f"   English:  {f['english_translation']}")
            print(f"   Actual:   {f['actual']}")
    elif failures:
        print(f"\n(Showing first 20 of {failed} failures)")
        for i, f in enumerate(failures[:20], 1):
            print(f"\n{i}. {f['lang'].upper()} - {f['number']} ({f['type']})")
            print(f"   Expected: {f['expected']}")
            if f.get('english_translation'):
                print(f"   English:  {f['english_translation']}")
            print(f"   Actual:   {f['actual']}")

    return passed, failed


if __name__ == "__main__":
    run_csv_tests()
