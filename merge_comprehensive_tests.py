#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merge comprehensive test files with existing test files.
This preserves existing tests and adds comprehensive coverage.
"""

import os
import shutil
from datetime import datetime

def merge_test_files(lang_code):
    """Merge comprehensive test file with existing test file."""
    
    existing_file = f"tests/test_{lang_code}.py"
    comprehensive_file = f"tests/test_{lang_code}_comprehensive.py"
    backup_file = f"tests/test_{lang_code}.py.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Check if comprehensive file exists
    if not os.path.exists(comprehensive_file):
        return False, "No comprehensive test file found"
    
    # Check if existing file exists
    if not os.path.exists(existing_file):
        # No existing file, just rename comprehensive to main
        shutil.move(comprehensive_file, existing_file)
        return True, "Created new test file from comprehensive tests"
    
    # Read existing file
    with open(existing_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    
    # Check if already has comprehensive tests
    if 'ComprehensiveTest' in existing_content:
        return False, "Already has comprehensive tests"
    
    # Read comprehensive file
    with open(comprehensive_file, 'r', encoding='utf-8') as f:
        comprehensive_content = f.read()
    
    # Create backup
    shutil.copy2(existing_file, backup_file)
    
    # Extract the comprehensive test class
    # Find where the class definition starts
    class_start = comprehensive_content.find('class Num2Words')
    if class_start == -1:
        return False, "Could not find test class in comprehensive file"
    
    # Extract from class definition to end of file
    comprehensive_class = comprehensive_content[class_start:]
    
    # Merge the files
    # Add comprehensive tests at the end of existing file
    merged_content = existing_content.rstrip() + '\n\n\n' + comprehensive_class
    
    # Write merged content
    with open(existing_file, 'w', encoding='utf-8') as f:
        f.write(merged_content)
    
    # Remove comprehensive file after successful merge
    os.remove(comprehensive_file)
    
    return True, f"Merged successfully (backup: {backup_file})"


def main():
    print("=" * 80)
    print("MERGING COMPREHENSIVE TESTS WITH EXISTING TEST FILES")
    print("=" * 80)
    print()
    
    # Get all comprehensive test files
    comprehensive_files = []
    for filename in os.listdir('tests'):
        if filename.endswith('_comprehensive.py'):
            lang_code = filename.replace('test_', '').replace('_comprehensive.py', '')
            comprehensive_files.append(lang_code)
    
    comprehensive_files.sort()
    
    print(f"Found {len(comprehensive_files)} comprehensive test files to merge\n")
    
    # Statistics
    merged = 0
    skipped = 0
    errors = 0
    
    for lang_code in comprehensive_files:
        print(f"Processing {lang_code}...", end=" ")
        
        success, message = merge_test_files(lang_code)
        
        if success:
            print(f"✅ {message}")
            merged += 1
        else:
            print(f"⚠️  {message}")
            skipped += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("-" * 80)
    print(f"Total files processed: {len(comprehensive_files)}")
    print(f"Successfully merged: {merged}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print()
    print("Next steps:")
    print("1. Run 'python -m pytest tests/' to verify all tests work")
    print("2. Review any test failures")
    print("3. Update expected values where needed")
    print("4. Commit the improved test coverage")


if __name__ == '__main__':
    main()