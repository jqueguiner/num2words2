#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analyze test coverage across all language test files."""

import os
import re
from collections import defaultdict
import ast

def get_test_methods(file_path):
    """Extract test method names from a test file."""
    methods = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Parse the AST to find all test methods
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    methods.append(node.name)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return sorted(set(methods))

def categorize_test(test_name):
    """Categorize test based on its name."""
    categories = {
        'cardinal': ['cardinal', 'basic', 'number', 'tens', 'hundreds', 'thousands', 'millions', 'billions'],
        'ordinal': ['ordinal'],
        'ordinal_num': ['ordinal_num'],
        'currency': ['currency', 'dollar', 'euro', 'pound'],
        'year': ['year'],
        'decimal': ['decimal', 'float', 'point'],
        'negative': ['negative', 'minus'],
        'overflow': ['overflow'],
        'large_numbers': ['large', 'big'],
        'special_cases': ['special', 'edge', 'error'],
        'default': ['default']
    }
    
    test_lower = test_name.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in test_lower:
                return category
    return 'other'

# Standard test categories that should be present
STANDARD_CATEGORIES = {
    'cardinal': 'Basic cardinal number conversion',
    'ordinal': 'Ordinal number conversion (first, second, etc.)',
    'ordinal_num': 'Ordinal number with suffix (1st, 2nd, etc.)',
    'currency': 'Currency conversion',
    'year': 'Year representation',
    'decimal': 'Decimal/float number handling',
    'negative': 'Negative number handling'
}

def main():
    test_dir = 'tests'
    language_tests = {}
    
    # Scan all test files
    for filename in os.listdir(test_dir):
        if filename.startswith('test_') and filename.endswith('.py'):
            # Extract language code
            lang_code = filename[5:-3]  # Remove 'test_' and '.py'
            
            # Skip non-language tests
            if lang_code in ['utils', 'errors', 'cli', 'converters']:
                continue
                
            file_path = os.path.join(test_dir, filename)
            test_methods = get_test_methods(file_path)
            
            # Categorize tests
            categories = defaultdict(list)
            for method in test_methods:
                category = categorize_test(method)
                categories[category].append(method)
            
            language_tests[lang_code] = {
                'methods': test_methods,
                'categories': dict(categories),
                'count': len(test_methods)
            }
    
    # Use English as reference
    reference_lang = 'en'
    if reference_lang not in language_tests:
        print(f"Warning: Reference language '{reference_lang}' not found!")
        return
    
    reference_categories = set(language_tests[reference_lang]['categories'].keys())
    
    print("=" * 80)
    print("TEST COVERAGE ANALYSIS - Comparing all languages to English (reference)")
    print("=" * 80)
    print()
    
    # Summary statistics
    print("SUMMARY STATISTICS:")
    print(f"Total languages analyzed: {len(language_tests)}")
    print(f"Reference (English) test count: {language_tests[reference_lang]['count']}")
    print(f"Reference test categories: {', '.join(sorted(reference_categories))}")
    print()
    
    # Detailed comparison
    print("DETAILED LANGUAGE COMPARISON:")
    print("-" * 80)
    
    # Sort languages by test count (ascending to highlight those needing work)
    sorted_langs = sorted(language_tests.items(), key=lambda x: x[1]['count'])
    
    for lang, data in sorted_langs:
        if lang == reference_lang:
            continue
            
        lang_categories = set(data['categories'].keys())
        missing_categories = reference_categories - lang_categories
        extra_categories = lang_categories - reference_categories
        
        # Determine status
        if data['count'] == 0:
            status = "❌ NO TESTS"
        elif data['count'] < language_tests[reference_lang]['count'] * 0.5:
            status = "⚠️  LOW COVERAGE"
        elif missing_categories:
            status = "⚠️  MISSING CATEGORIES"
        else:
            status = "✅ GOOD"
        
        print(f"\n{lang.upper()} ({status}):")
        print(f"  Test count: {data['count']} (English has {language_tests[reference_lang]['count']})")
        print(f"  Categories: {', '.join(sorted(lang_categories)) if lang_categories else 'None'}")
        
        if missing_categories:
            print(f"  Missing categories: {', '.join(sorted(missing_categories))}")
        if extra_categories:
            print(f"  Extra categories: {', '.join(sorted(extra_categories))}")
    
    print("\n" + "=" * 80)
    print("LANGUAGES NEEDING ATTENTION (sorted by priority):")
    print("-" * 80)
    
    needs_attention = []
    for lang, data in language_tests.items():
        if lang == reference_lang:
            continue
        
        lang_categories = set(data['categories'].keys())
        missing_categories = reference_categories - lang_categories
        
        # Calculate priority score (higher = needs more attention)
        priority = 0
        if data['count'] == 0:
            priority = 100
        else:
            # Factor in test count difference
            count_diff = language_tests[reference_lang]['count'] - data['count']
            priority += count_diff * 2
            
            # Factor in missing categories
            priority += len(missing_categories) * 10
        
        if priority > 0:
            needs_attention.append((priority, lang, data['count'], missing_categories))
    
    # Sort by priority (highest first)
    needs_attention.sort(reverse=True)
    
    for priority, lang, count, missing_cats in needs_attention[:20]:  # Show top 20
        print(f"  {lang.upper():10} - Priority: {priority:3} | Tests: {count:3} | Missing: {', '.join(sorted(missing_cats)) if missing_cats else 'None'}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("-" * 80)
    print("Each language should ideally have tests for:")
    for category, description in STANDARD_CATEGORIES.items():
        print(f"  • {category}: {description}")

if __name__ == '__main__':
    main()