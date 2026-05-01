"""Tests for num2words2.grouping (issue #66)."""

from num2words2 import group_digits


def test_western_grouping():
    assert group_digits(1234567, locale="western") == "1,234,567"
    assert group_digits(1000) == "1,000"


def test_indian_grouping():
    assert group_digits(100000, locale="indian") == "1,00,000"
    assert group_digits(12345678, locale="indian") == "1,23,45,678"
    assert group_digits(999, locale="indian") == "999"


def test_chinese_grouping():
    assert group_digits(12345678, locale="chinese") == "1234,5678"


def test_negative():
    assert group_digits(-12345678, locale="indian") == "-1,23,45,678"


def test_zero():
    assert group_digits(0, locale="indian") == "0"


def test_custom_separator():
    assert group_digits(100000, locale="indian", separator=" ") == "1 00 000"


def test_unknown_locale_raises():
    import pytest
    with pytest.raises(ValueError):
        group_digits(100, locale="bogus")


def test_non_int_raises():
    import pytest
    with pytest.raises(TypeError):
        group_digits(1.5)
