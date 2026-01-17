#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhance test coverage for languages with critically low test counts.
This script adds proper tests with actual expected values.
"""

import os
from num2words2 import num2words

def generate_en_in_tests():
    """Generate comprehensive tests for English (India) with lakh/crore system."""
    
    # Test the actual output to get correct values
    test_numbers = [
        # Basic numbers
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        # Tens
        30, 40, 50, 60, 70, 80, 90, 99,
        # Hundreds
        100, 101, 200, 500, 999,
        # Thousands
        1000, 1001, 5000, 10000, 25000, 50000, 99999,
        # Lakhs (100,000)
        100000, 200000, 500000, 999999,
        # Millions (10 lakhs)
        1000000, 2500000, 9999999,
        # Crores (10,000,000)
        10000000, 50000000, 99999999,
        100000000, 999999999
    ]
    
    print("# Additional test cases for English (India)")
    print("# Uses the lakh/crore numbering system")
    print()
    
    # Generate cardinal tests
    print("def test_cardinal_comprehensive(self):")
    print('    """Test comprehensive cardinal numbers for Indian numbering."""')
    print("    test_cases = [")
    
    for num in test_numbers:
        try:
            result = num2words(num, lang='en_IN')
            print(f"        ({num}, '{result}'),")
        except Exception as e:
            print(f"        # {num}: Error - {e}")
    
    print("    ]")
    print("    for num, expected in test_cases:")
    print("        with self.subTest(num=num):")
    print("            self.assertEqual(num2words(num, lang='en_IN'), expected)")
    print()
    
    # Test ordinals
    print("def test_ordinal(self):")
    print('    """Test ordinal numbers."""')
    print("    test_cases = [")
    
    for num in [1, 2, 3, 4, 5, 10, 11, 12, 20, 21, 100, 1000]:
        try:
            result = num2words(num, lang='en_IN', to='ordinal')
            print(f"        ({num}, '{result}'),")
        except NotImplementedError:
            print("        # Ordinals not implemented")
            break
        except Exception as e:
            print(f"        # {num}: Error - {e}")
    
    print("    ]")
    print("    for num, expected in test_cases:")
    print("        with self.subTest(num=num):")
    print("            self.assertEqual(num2words(num, lang='en_IN', to='ordinal'), expected)")
    print()
    
    # Test currency
    print("def test_currency_inr(self):")
    print('    """Test Indian Rupee currency."""')
    print("    test_cases = [")
    
    for amount in [0, 1, 2, 10, 100, 1000, 100000, 10000000]:
        try:
            result = num2words(amount, lang='en_IN', to='currency', currency='INR')
            print(f"        ({amount}, '{result}'),")
        except Exception:
            try:
                result = num2words(amount, lang='en_IN', to='currency')
                print(f"        ({amount}, '{result}'),")
            except:
                print(f"        # Currency not implemented")
                break
    
    print("    ]")
    print("    for amount, expected in test_cases:")
    print("        with self.subTest(amount=amount):")
    print("            self.assertEqual(")
    print("                num2words(amount, lang='en_IN', to='currency', currency='INR'),")
    print("                expected")
    print("            )")


def generate_tr_tests():
    """Generate comprehensive tests for Turkish."""
    
    print("\n# Additional test cases for Turkish")
    print()
    
    # Basic cardinal tests
    test_numbers = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        11, 12, 13, 14, 15, 20, 21, 30, 40, 50,
        60, 70, 80, 90, 99, 100, 101, 200, 500, 999,
        1000, 1001, 2000, 10000, 100000, 1000000
    ]
    
    print("def test_cardinal_comprehensive(self):")
    print('    """Test comprehensive cardinal numbers for Turkish."""')
    print("    test_cases = [")
    
    for num in test_numbers:
        try:
            result = num2words(num, lang='tr')
            print(f"        ({num}, '{result}'),")
        except Exception as e:
            print(f"        # {num}: Error - {e}")
    
    print("    ]")
    print("    for num, expected in test_cases:")
    print("        with self.subTest(num=num):")
    print("            self.assertEqual(num2words(num, lang='tr'), expected)")


def generate_cs_tests():
    """Generate comprehensive tests for Czech."""
    
    print("\n# Additional test cases for Czech")
    print()
    
    test_numbers = [
        0, 1, 2, 3, 4, 5, 10, 11, 12, 20, 21,
        100, 101, 200, 1000, 1001, 2000
    ]
    
    print("def test_cardinal_comprehensive(self):")
    print('    """Test comprehensive cardinal numbers for Czech."""')
    print("    test_cases = [")
    
    for num in test_numbers:
        try:
            result = num2words(num, lang='cs')
            print(f"        ({num}, '{result}'),")
        except Exception as e:
            print(f"        # {num}: Error - {e}")
    
    print("    ]")
    print("    for num, expected in test_cases:")
    print("        with self.subTest(num=num):")
    print("            self.assertEqual(num2words(num, lang='cs'), expected)")


def main():
    print("=" * 80)
    print("GENERATING PROPER TESTS FOR CRITICAL LOW-COVERAGE LANGUAGES")
    print("=" * 80)
    print()
    
    # Generate for most critical languages
    generate_en_in_tests()
    generate_tr_tests()
    generate_cs_tests()
    
    print("\n" + "=" * 80)
    print("IMPORTANT: These are actual test values from the implementation.")
    print("Copy these test methods into the respective test files.")
    print("=" * 80)


if __name__ == '__main__':
    main()