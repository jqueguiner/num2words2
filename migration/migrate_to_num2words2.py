#!/usr/bin/env python3
"""
Migration script from num2words to num2words2

This script helps migrate your codebase from num2words to num2words2 by:
1. Finding all Python files with num2words imports
2. Backing up original files
3. Updating imports to use num2words2
4. Providing a summary of changes

Usage:
    python migrate_to_num2words2.py [directory]
If no directory is specified, it will scan the current directory.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path


def find_python_files(directory):
    """Find all Python files in the given directory recursively."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip common non-source directories
        dirs[:] = [
            d
            for d in dirs
            if d
            not in {
                ".git",
                "__pycache__",
                ".tox",
                "venv",
                "env",
                ".env",
                "node_modules",
            }
        ]
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def check_file_for_num2words(file_path):
    """Check if a file contains num2words imports."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Patterns to match num2words imports
        patterns = [
            r"from\s+num2words\s+import",
            r"import\s+num2words",
            r"from\s+num2words\.",
        ]
        for pattern in patterns:
            if re.search(pattern, content):
                return True, content
        return False, content
    except (UnicodeDecodeError, IOError) as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return False, ""


def migrate_file_content(content):
    """Migrate the content of a file from num2words to num2words2."""
    changes_made = []

    # Pattern replacements - order matters!
    replacements = [
        (
            r"from\s+num2words\.([a-zA-Z_][a-zA-Z0-9_]*)\s+import",
            r"from num2words2.\1 import",
            "Updated submodule import",
        ),
        (
            r"from\s+num2words\s+import",
            "from num2words2 import",
            "Updated import statement",
        ),
        (
            r"(^|\s)import\s+num2words(?!\w)",
            r"\1import num2words2 as num2words",
            "Updated import with alias",
        ),
    ]

    new_content = content
    for pattern, replacement, description in replacements:
        matches = re.findall(pattern, new_content, re.MULTILINE)
        if matches:
            new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)
            changes_made.append(
                f"  - {description} ({len(matches)} "
                f"occurrence{'s' if len(matches) != 1 else ''})"
            )

    return new_content, changes_made


def create_backup(file_path):
    """Create a backup of the original file."""
    backup_path = f"{file_path}.num2words_backup"
    shutil.copy2(file_path, backup_path)
    return backup_path


def migrate_file(file_path, dry_run=False):
    """Migrate a single file from num2words to num2words2."""
    has_imports, content = check_file_for_num2words(file_path)

    if not has_imports:
        return None

    new_content, changes = migrate_file_content(content)

    if not changes:
        return None

    result = {"file": file_path, "changes": changes, "backup": None}

    if not dry_run:
        # Create backup
        backup_path = create_backup(file_path)
        result["backup"] = backup_path
        # Write new content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    return result


def main():
    parser = argparse.ArgumentParser(description="Migrate from num2words to num2words2")
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making " "changes",
    )
    parser.add_argument(
        "--requirements", action="store_true", help="Also check requirements files"
    )

    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)

    print(f"🔍 Scanning for num2words imports in: " f"{os.path.abspath(args.directory)}")
    print()

    # Find Python files
    if os.path.isfile(args.directory) and args.directory.endswith(".py"):
        python_files = [args.directory]
    else:
        python_files = find_python_files(args.directory)

    # Also check requirements files if requested
    req_files = []
    if args.requirements:
        req_patterns = [
            "requirements*.txt",
            "requirements*.in",
            "pyproject.toml",
            "setup.py",
            "setup.cfg",
        ]
        for pattern in req_patterns:
            req_files.extend(Path(args.directory).rglob(pattern))
        req_files = [str(f) for f in req_files]

    all_files = python_files + req_files

    if not all_files:
        print("No Python files found to scan.")
        return

    print(f"📁 Found {len(all_files)} files to scan")
    print()

    migrated_files = []

    for file_path in all_files:
        result = migrate_file(file_path, dry_run=args.dry_run)
        if result:
            migrated_files.append(result)

    # Print results
    if not migrated_files:
        print("✅ No num2words imports found. Your codebase is already clean!")
        return

    print(
        f"📝 Found num2words imports in {len(migrated_files)} "
        f"file{'s' if len(migrated_files) != 1 else ''}:"
    )
    print()

    for result in migrated_files:
        print(f"📄 {result['file']}")
        for change in result["changes"]:
            print(change)
        if result["backup"]:
            print(f"  - Backup created: {result['backup']}")
        print()

    if args.dry_run:
        print("🔍 This was a dry run. No files were modified.")
        print("Run without --dry-run to apply changes.")
    else:
        print("✅ Migration completed!")
        print()
        print("📋 Next steps:")
        print("1. Install num2words2: pip install num2words2")
        print("2. Test your code to ensure it works correctly")
        print("3. Update your requirements.txt file:")
        print("   Replace 'num2words' with 'num2words2'")
        print("4. If everything works, you can remove the backup files")

    print()
    print(
        "📚 For more information, see: "
        "https://github.com/jqueguiner/num2words#migration"
    )


if __name__ == "__main__":
    main()
