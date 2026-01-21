#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
End-to-End Test Runner for num2words2
Runs comprehensive tests from CSV file and reports results
"""

import argparse
import csv
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Tuple

try:
    from num2words2 import num2words
except ImportError:
    print("Error: num2words2 not installed. Please run: pip install -e .")
    sys.exit(1)


class TestResult:
    """Container for test results"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = 0
        self.skipped = 0
        self.failures = []
        self.errors_list = []

        # Statistics by category
        self.by_language = defaultdict(lambda: {'passed': 0, 'failed': 0, 'errors': 0})
        self.by_type = defaultdict(lambda: {'passed': 0, 'failed': 0, 'errors': 0})
        self.by_currency = defaultdict(lambda: {'passed': 0, 'failed': 0, 'errors': 0})


def parse_number(number_str: str):
    """Parse number string to appropriate type"""
    try:
        # Try integer first
        if '.' not in number_str:
            return int(number_str)
        # Then float
        return float(number_str)
    except ValueError:
        return number_str


def run_single_test(test_case: dict) -> Tuple[str, str, str]:
    """
    Run a single test case
    Returns: (status, actual_output, error_message)
    """
    try:
        lang = test_case.get('lang', test_case.get('language', '')).strip()
        number = parse_number(test_case['number'])
        conversion_type = test_case.get('to', test_case.get('conversion_type', 'cardinal')).strip()
        currency = test_case.get('currency', '').strip()
        expected = test_case.get('expected', test_case.get('expected_output', '')).strip()

        # Build kwargs
        kwargs = {'lang': lang}

        # Handle different conversion types
        if conversion_type == 'cardinal':
            if currency:
                kwargs['to'] = 'currency'
                kwargs['currency'] = currency
            else:
                kwargs['to'] = 'cardinal'
        elif conversion_type == 'ordinal':
            kwargs['to'] = 'ordinal'
        elif conversion_type == 'ordinal_num':
            kwargs['to'] = 'ordinal_num'
        elif conversion_type == 'year':
            kwargs['to'] = 'year'
        elif conversion_type == 'currency':
            kwargs['to'] = 'currency'
            if currency:
                kwargs['currency'] = currency
        else:
            kwargs['to'] = conversion_type

        # Run conversion
        actual = num2words(number, **kwargs)
        actual = actual.strip()

        # Compare results
        if actual == expected:
            return 'PASS', actual, None
        else:
            return 'FAIL', actual, f"Expected: {expected}, Got: {actual}"

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        return 'ERROR', None, error_msg


def print_progress(current: int, total: int, results: TestResult):
    """Print progress bar and stats"""
    percent = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current / total)

    # Use ASCII characters for Windows compatibility
    bar = '=' * filled + '-' * (bar_length - filled)

    sys.stdout.write(f'\r[{bar}] {percent:.1f}% | '
                     f'PASS: {results.passed} | FAIL: {results.failed} | ERR: {results.errors} | '
                     f'SKIP: {results.skipped} | [{current}/{total}]')
    sys.stdout.flush()


def run_tests(csv_file: str, limit: int = None, verbose: bool = False) -> TestResult:
    """
    Run all tests from CSV file

    Args:
        csv_file: Path to CSV file with test cases
        limit: Limit number of tests (None for all)
        verbose: Print detailed output for failures
    """
    results = TestResult()
    csv_path = Path(csv_file)

    # If file doesn't exist, try looking in tests directory
    if not csv_path.exists():
        # Check if we're in the project root
        tests_csv = Path('tests') / csv_file
        if tests_csv.exists():
            csv_path = tests_csv
        # Check if the file exists in current directory
        elif Path(csv_file).name == csv_file and (Path(__file__).parent / csv_file).exists():
            csv_path = Path(__file__).parent / csv_file

    if not csv_path.exists():
        print(f"Error: Test file not found: {csv_file}")
        sys.exit(1)

    print(f"\n{'='*80}")
    print(f"Running E2E Tests from: {csv_file}")
    print(f"{'='*80}\n")

    # Count total tests
    with open(csv_path, 'r', encoding='utf-8') as f:
        total_tests = sum(1 for _ in f) - 1  # Subtract header
        if limit:
            total_tests = min(total_tests, limit)

    # Run tests
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, test_case in enumerate(reader, 1):
            if limit and i > limit:
                break

            # Skip empty rows
            if not test_case.get('lang', test_case.get('language')):
                results.skipped += 1
                continue

            # Run test
            status, actual, error = run_single_test(test_case)

            # Update statistics
            lang = test_case.get('lang', test_case.get('language', ''))
            conv_type = test_case.get('to', test_case.get('conversion_type', 'cardinal'))
            currency = test_case.get('currency', 'none')

            if status == 'PASS':
                results.passed += 1
                results.by_language[lang]['passed'] += 1
                results.by_type[conv_type]['passed'] += 1
                if currency != 'none':
                    results.by_currency[currency]['passed'] += 1
            elif status == 'FAIL':
                results.failed += 1
                results.by_language[lang]['failed'] += 1
                results.by_type[conv_type]['failed'] += 1
                if currency != 'none':
                    results.by_currency[currency]['failed'] += 1
                results.failures.append({
                    'test': test_case,
                    'actual': actual,
                    'error': error
                })
            else:  # ERROR
                results.errors += 1
                results.by_language[lang]['errors'] += 1
                results.by_type[conv_type]['errors'] += 1
                if currency != 'none':
                    results.by_currency[currency]['errors'] += 1
                results.errors_list.append({
                    'test': test_case,
                    'error': error
                })

            # Show progress
            if not verbose or i % 100 == 0:
                print_progress(i, total_tests, results)

            # Verbose output for failures
            if verbose and status != 'PASS':
                print(f"\n\n{status}: {lang} | {test_case['number']} | {conv_type}")
                print(f"  Expected: {test_case.get('expected', test_case.get('expected_output', ''))}")
                if actual:
                    print(f"  Actual:   {actual}")
                if error:
                    print(f"  Error:    {error}")

    print("\n")  # New line after progress bar
    return results


def print_summary(results: TestResult, detailed: bool = False):
    """Print test results summary"""
    total = results.passed + results.failed + results.errors + results.skipped

    print(f"\n{'='*80}")
    print("TEST RESULTS SUMMARY")
    print(f"{'='*80}\n")

    # Overall results
    print(f"Total Tests:    {total:,}")
    print(f"Passed:         {results.passed:,} ({results.passed/total*100:.1f}%)")
    print(f"Failed:         {results.failed:,} ({results.failed/total*100:.1f}%)")
    print(f"Errors:         {results.errors:,} ({results.errors/total*100:.1f}%)")
    print(f"Skipped:        {results.skipped:,} ({results.skipped/total*100:.1f}%)")

    # Success rate
    success_rate = results.passed / (total - results.skipped) * 100 if (total - results.skipped) > 0 else 0
    print(f"\nSuccess Rate:   {success_rate:.2f}%")

    if detailed:
        # Results by language
        print(f"\n{'='*80}")
        print("RESULTS BY LANGUAGE")
        print(f"{'='*80}")
        for lang in sorted(results.by_language.keys()):
            stats = results.by_language[lang]
            total_lang = stats['passed'] + stats['failed'] + stats['errors']
            success = stats['passed'] / total_lang * 100 if total_lang > 0 else 0
            print(f"{lang:10} - Total: {total_lang:6,} | "
                  f"PASS: {stats['passed']:6,} ({success:.1f}%) | "
                  f"FAIL: {stats['failed']:6,} | "
                  f"ERR: {stats['errors']:6,}")

        # Results by conversion type
        print(f"\n{'='*80}")
        print("RESULTS BY CONVERSION TYPE")
        print(f"{'='*80}")
        for conv_type in sorted(results.by_type.keys()):
            stats = results.by_type[conv_type]
            total_type = stats['passed'] + stats['failed'] + stats['errors']
            success = stats['passed'] / total_type * 100 if total_type > 0 else 0
            print(f"{conv_type:12} - Total: {total_type:6,} | "
                  f"PASS: {stats['passed']:6,} ({success:.1f}%) | "
                  f"FAIL: {stats['failed']:6,} | "
                  f"ERR: {stats['errors']:6,}")

        # Show some failures
        if results.failures:
            print(f"\n{'='*80}")
            print("SAMPLE FAILURES (showing first 10)")
            print(f"{'='*80}")
            for failure in results.failures[:10]:
                test = failure['test']
                print(f"\n{test.get('lang', test.get('language', ''))} | {test['number']} | {test.get('to', test.get('conversion_type', 'cardinal'))}")
                print(f"  Expected: {test.get('expected', test.get('expected_output', ''))}")
                print(f"  Actual:   {failure['actual']}")

        # Show some errors
        if results.errors_list:
            print(f"\n{'='*80}")
            print("SAMPLE ERRORS (showing first 10)")
            print(f"{'='*80}")
            for error_item in results.errors_list[:10]:
                test = error_item['test']
                print(f"\n{test.get('lang', test.get('language', ''))} | {test['number']} | {test.get('to', test.get('conversion_type', 'cardinal'))}")
                print(f"  Error: {error_item['error']}")

    # Exit code
    if results.failed > 0 or results.errors > 0:
        threshold = 0.95  # 95% pass threshold
        if success_rate < threshold * 100:
            print(f"\n[FAIL] Tests failed (success rate {success_rate:.2f}% < {threshold*100}% threshold)")
            return 1
        else:
            print(f"\n[WARN] Tests passed with warnings (success rate {success_rate:.2f}% >= {threshold*100}% threshold)")
            return 0
    else:
        print("\n[PASS] All tests passed!")
        return 0


def main():
    parser = argparse.ArgumentParser(description='Run E2E tests for num2words2')
    parser.add_argument('--file', '-f',
                        default='e2e_test_suite.csv',
                        help='CSV file with test cases (default: e2e_test_suite.csv)')
    parser.add_argument('--limit', '-l',
                        type=int,
                        help='Limit number of tests to run')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Show detailed output for failures')
    parser.add_argument('--detailed', '-d',
                        action='store_true',
                        help='Show detailed summary statistics')
    parser.add_argument('--quick', '-q',
                        action='store_true',
                        help='Quick test with first 100 cases')

    args = parser.parse_args()

    # Quick mode
    if args.quick:
        args.limit = 100
        args.detailed = True

    # Start timer
    start_time = time.time()

    # Run tests
    results = run_tests(args.file, limit=args.limit, verbose=args.verbose)

    # Print summary
    exit_code = print_summary(results, detailed=args.detailed)

    # Print timing
    elapsed = time.time() - start_time
    print(f"\nTest completed in {elapsed:.2f} seconds")
    total_tests_run = results.passed + results.failed + results.errors
    if total_tests_run > 0:
        print(f"Average: {elapsed/total_tests_run:.4f} seconds per test")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
