#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def fix_blank_lines(file_path):
    """Fix E302 errors (expected 2 blank lines before class/function)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    new_lines = []
    i = 0
    
    while i < len(lines):
        # Check for import followed by class definition
        if i > 0 and lines[i].strip().startswith('class '):
            # Count blank lines before class
            blank_count = 0
            j = i - 1
            while j >= 0 and lines[j].strip() == '':
                blank_count += 1
                j -= 1
            
            # Check if previous non-blank line is an import or comment
            if j >= 0 and (lines[j].strip().startswith(('import ', 'from ')) or 
                          lines[j].strip().startswith('#')):
                # Need exactly 2 blank lines
                if blank_count != 2:
                    # Remove existing blank lines
                    while new_lines and new_lines[-1].strip() == '':
                        new_lines.pop()
                    # Add exactly 2 blank lines
                    new_lines.append('\n')
                    new_lines.append('\n')
                    modified = True
        
        new_lines.append(lines[i])
        i += 1
    
    # Remove trailing whitespace and fix W292/W293
    final_lines = []
    for line in new_lines:
        # Remove trailing whitespace
        line = line.rstrip()
        if line:
            line += '\n'
        else:
            line = '\n'
        final_lines.append(line)
    
    # Ensure file ends with newline
    if final_lines and not final_lines[-1].endswith('\n'):
        final_lines[-1] += '\n'
    elif not final_lines:
        final_lines = ['\n']
    
    # Write back if modified
    if True:  # Always write to ensure proper formatting
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        return True
    return False

def fix_long_lines(file_path):
    """Fix E501 errors (line too long)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    new_lines = []
    
    for line in lines:
        stripped = line.rstrip()
        if len(stripped) > 79:
            # Special handling for different types of lines
            if 'assertEqual' in line or 'assertRaises' in line:
                # For test assertions, break after commas
                if ', lang=' in line:
                    parts = line.split(', lang=')
                    if len(parts) == 2:
                        indent = len(line) - len(line.lstrip())
                        new_lines.append(parts[0] + ',\n')
                        new_lines.append(' ' * (indent + 4) + 'lang=' + parts[1])
                        modified = True
                        continue
                elif '", "' in line:
                    # Break between string arguments
                    match = re.match(r'(\s*self\.assert\w+\()(.+)', stripped)
                    if match:
                        indent = len(match.group(1))
                        args = match.group(2).rstrip(')')
                        # Try to split at commas
                        parts = args.split('", "')
                        if len(parts) > 1:
                            new_lines.append(match.group(1) + parts[0] + '",\n')
                            new_lines.append(' ' * indent + '"' + '", "'.join(parts[1:]) + ')\n')
                            modified = True
                            continue
            elif '# pragma:' in line or '# type:' in line or '# noqa' in line:
                # For comments, can sometimes be split
                code_part = line[:79]
                comment_part = line[79:]
                if comment_part.strip().startswith('#'):
                    new_lines.append(code_part.rstrip() + '\n')
                    new_lines.append(' ' * 4 + comment_part.strip() + '\n')
                    modified = True
                    continue
            elif 'self.assertEqual(num2words(' in line:
                # Special handling for num2words test lines
                match = re.search(r'num2words\(([^,]+),([^)]+)\)', line)
                if match:
                    indent = len(line) - len(line.lstrip())
                    start = line[:line.index('num2words(')]
                    new_lines.append(start + 'num2words(\n')
                    new_lines.append(' ' * (indent + 4) + match.group(1) + ',\n')
                    new_lines.append(' ' * (indent + 4) + match.group(2) + line[match.end():])
                    modified = True
                    continue
            
            # Default: add line as-is if we can't fix it automatically
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

# Files to fix based on flake8 output
files_to_fix = [
    'num2words2/lang_AF.py',
    'num2words2/lang_EL.py', 
    'num2words2/lang_HA.py',
    'num2words2/lang_HR.py',
    'num2words2/lang_SN.py',
    'num2words2/lang_SQ.py',
    'num2words2/lang_SW.py',
    'tests/test_af.py',
    'tests/test_el.py',
    'tests/test_en.py',
    'tests/test_sq.py',
    'tests/test_sw.py',
    'tests/test_sn.py',
    'tests/test_ha.py',
    'tests/test_hr.py'
]

print("Fixing flake8 issues...")

# First pass: fix blank lines and whitespace
for file_path in files_to_fix:
    if os.path.exists(file_path):
        if fix_blank_lines(file_path):
            print(f"Fixed blank lines in {file_path}")

# Note: Long line fixes are complex and often require manual intervention
# We'll fix the most critical ones manually after this
print("\nDone! Some E501 (line too long) errors may need manual fixing.")