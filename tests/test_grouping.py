"""Tests for num2words2.grouping (issue #66)."""

import unittest

from num2words2 import group_digits, grouping


# NOTE: these assertions were previously written as bare pytest-style
# functions, which `unittest discover` (the CI runner) does not collect, so
# they never executed. Expressed as a unittest.TestCase they run under the
# CI runner and exercise num2words2.grouping. Assertions are unchanged.
class GroupDigitsTest(unittest.TestCase):
    def test_western_grouping(self):
        self.assertEqual(group_digits(1234567, locale="western"), "1,234,567")
        self.assertEqual(group_digits(1000), "1,000")

    def test_indian_grouping(self):
        self.assertEqual(group_digits(100000, locale="indian"), "1,00,000")
        self.assertEqual(group_digits(12345678, locale="indian"), "1,23,45,678")
        self.assertEqual(group_digits(999, locale="indian"), "999")

    def test_chinese_grouping(self):
        self.assertEqual(group_digits(12345678, locale="chinese"), "1234,5678")

    def test_negative(self):
        self.assertEqual(group_digits(-12345678, locale="indian"), "-1,23,45,678")

    def test_zero(self):
        self.assertEqual(group_digits(0, locale="indian"), "0")

    def test_custom_separator(self):
        self.assertEqual(
            group_digits(100000, locale="indian", separator=" "), "1 00 000"
        )

    def test_unknown_locale_raises(self):
        with self.assertRaises(ValueError):
            group_digits(100, locale="bogus")

    def test_non_int_raises(self):
        with self.assertRaises(TypeError):
            group_digits(1.5)


# The pure-Python grouping implementation is a real fallback used when the
# num2words2._rust extension is unavailable (pure-Python / sdist installs).
# Under the built CI wheel `group_digits` delegates to _rust, so the fallback
# never runs there; exercise it here by temporarily unbinding the extension.
# Assertions match the extension's output exactly (verified equal).
class GroupDigitsPurePythonTest(unittest.TestCase):
    def setUp(self):
        self._saved_rust = grouping._RUST
        grouping._RUST = None

    def tearDown(self):
        grouping._RUST = self._saved_rust

    def test_western_grouping(self):
        self.assertEqual(grouping.group_digits(1234567, locale="western"), "1,234,567")
        self.assertEqual(grouping.group_digits(1000), "1,000")

    def test_indian_grouping(self):
        self.assertEqual(grouping.group_digits(100000, locale="indian"), "1,00,000")
        self.assertEqual(
            grouping.group_digits(12345678, locale="indian"), "1,23,45,678"
        )
        self.assertEqual(grouping.group_digits(999, locale="indian"), "999")

    def test_chinese_grouping(self):
        self.assertEqual(
            grouping.group_digits(12345678, locale="chinese"), "1234,5678"
        )

    def test_negative(self):
        self.assertEqual(
            grouping.group_digits(-12345678, locale="indian"), "-1,23,45,678"
        )

    def test_zero(self):
        self.assertEqual(grouping.group_digits(0, locale="indian"), "0")

    def test_custom_separator(self):
        self.assertEqual(
            grouping.group_digits(100000, locale="indian", separator=" "),
            "1 00 000",
        )

    def test_unknown_locale_raises(self):
        with self.assertRaises(ValueError):
            grouping.group_digits(100, locale="bogus")
