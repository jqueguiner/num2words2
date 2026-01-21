#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive test runner for unit tests and E2E tests.
"""

import importlib
import subprocess
import sys
from pathlib import Path

import pandas as pd


def run_unit_tests():
    """Run all unit tests using pytest."""
    print("=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        capture_output=True,
        text=True
    )

    # Parse output
    lines = result.stdout.strip().split('\n')
    summary_line = lines[-1] if lines else ""

    print(f"Unit Test Results: {summary_line}")

    # Extract numbers
    if "passed" in summary_line:
        parts = summary_line.split()
        passed = failed = errors = 0

        for i, part in enumerate(parts):
            if "passed" in part:
                passed = int(parts[i - 1])
            elif "failed" in part:
                failed = int(parts[i - 1])
            elif "error" in part:
                errors = int(parts[i - 1])

        total = passed + failed + errors
        pass_rate = (passed / total * 100) if total > 0 else 0

        print(f"Pass Rate: {pass_rate:.1f}% ({passed}/{total})")
        return passed, failed, errors

    return 0, 0, 0


def run_e2e_tests():
    """Run E2E tests from CSV file."""
    print("\n" + "=" * 60)
    print("RUNNING E2E TESTS")
    print("=" * 60)

    # Load test data
    csv_path = Path("tests/e2e_test_suite.csv")
    if not csv_path.exists():
        print("E2E test suite not found!")
        return 0, 0, 0

    df = pd.read_csv(csv_path)

    print(f"Total E2E test cases: {len(df)}")
    print(f"Languages tested: {df['language'].nunique()}")
    print(f"Test types: {df['conversion_type'].unique().tolist()}")
    print()

    # Run tests
    test_results = {'passed': 0, 'failed': 0, 'errors': 0}
    failures_by_type = {}
    failures_by_lang = {}

    for _, row in df.iterrows():
        lang = row['language']
        number = row['number']
        conv_type = row['conversion_type']
        expected = row['expected_output']
        currency = row.get('currency', 'EUR') if pd.notna(row.get('currency')) else 'EUR'

        try:
            # Import the language module
            module_name = f'num2words2.lang_{lang.upper()}'
            module = importlib.import_module(module_name)
            class_name = f'Num2Word_{lang.upper()}'
            converter_class = getattr(module, class_name)
            converter = converter_class()

            # Convert based on type
            if conv_type == 'cardinal':
                actual = converter.to_cardinal(number)
            elif conv_type == 'ordinal':
                actual = converter.to_ordinal(number)
            elif conv_type == 'ordinal_num':
                actual = converter.to_ordinal_num(number)
            elif conv_type == 'currency':
                actual = converter.to_currency(number, currency=currency)
            elif conv_type == 'year':
                actual = converter.to_year(number)
            else:
                actual = str(number)

            # Check result
            if str(actual).strip() == str(expected).strip():
                test_results['passed'] += 1
            else:
                test_results['failed'] += 1
                if conv_type not in failures_by_type:
                    failures_by_type[conv_type] = 0
                failures_by_type[conv_type] += 1

                if lang not in failures_by_lang:
                    failures_by_lang[lang] = 0
                failures_by_lang[lang] += 1

        except Exception:
            test_results['errors'] += 1
            if conv_type not in failures_by_type:
                failures_by_type[conv_type] = 0
            failures_by_type[conv_type] += 1

            if lang not in failures_by_lang:
                failures_by_lang[lang] = 0
            failures_by_lang[lang] += 1

    # Print results
    total = len(df)
    print("E2E Test Results:")
    print(f"  Passed: {test_results['passed']}/{total} ({test_results['passed']/total*100:.1f}%)")
    print(f"  Failed: {test_results['failed']}/{total} ({test_results['failed']/total*100:.1f}%)")
    print(f"  Errors: {test_results['errors']}/{total} ({test_results['errors']/total*100:.1f}%)")

    if failures_by_type:
        print("\nFailures by type:")
        for conv_type, count in sorted(failures_by_type.items()):
            print(f"  {conv_type}: {count} failures")

    if failures_by_lang:
        print("\nTop 10 languages with most failures:")
        for lang, count in sorted(failures_by_lang.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {lang}: {count} failures")

    return test_results['passed'], test_results['failed'], test_results['errors']


def main():
    """Main test runner."""
    print("=" * 60)
    print("COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    # Run unit tests
    unit_passed, unit_failed, unit_errors = run_unit_tests()

    # Run E2E tests
    e2e_passed, e2e_failed, e2e_errors = run_e2e_tests()

    # Overall summary
    print("\n" + "=" * 60)
    print("OVERALL TEST SUMMARY")
    print("=" * 60)

    total_passed = unit_passed + e2e_passed
    total_failed = unit_failed + e2e_failed
    total_errors = unit_errors + e2e_errors
    total_tests = total_passed + total_failed + total_errors

    print(f"Total Tests Run: {total_tests}")
    print(f"Total Passed: {total_passed} ({total_passed/total_tests*100:.1f}%)")
    print(f"Total Failed: {total_failed} ({total_failed/total_tests*100:.1f}%)")
    print(f"Total Errors: {total_errors} ({total_errors/total_tests*100:.1f}%)")

    print("\nBreakdown:")
    print(f"  Unit Tests: {unit_passed} passed, {unit_failed} failed, {unit_errors} errors")
    print(f"  E2E Tests:  {e2e_passed} passed, {e2e_failed} failed, {e2e_errors} errors")

    # Coverage report
    print("\n" + "=" * 60)
    print("CODE COVERAGE")
    print("=" * 60)

    coverage_result = subprocess.run(
        ["coverage", "report", "--omit=*/test_*,*/tests/*,*/site-packages/*,*/__pycache__/*,*/_version.py"],
        capture_output=True,
        text=True
    )

    for line in coverage_result.stdout.strip().split('\n'):
        if "TOTAL" in line:
            print(f"Overall Coverage: {line.split()[-1]}")
            break

    return 0 if total_failed == 0 and total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
