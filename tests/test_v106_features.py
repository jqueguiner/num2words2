"""Tier-1 v1.0.6 features: maxval helper, runpy entry, precision= kwarg."""

import subprocess
import sys

import pytest

import num2words2


def test_maxval_helper():
    # Issue #582
    assert isinstance(num2words2.maxval("en"), int)
    assert num2words2.maxval("en") > 10**100
    assert num2words2.maxval("en_IN") > 10**18
    # Unknown lang raises
    with pytest.raises(NotImplementedError):
        num2words2.maxval("zzz_unknown")


def test_runpy_invocation():
    # Issue #348 — python -m num2words2 N -l X
    out = subprocess.check_output(
        [sys.executable, "-m", "num2words2", "1234", "-l", "fr"]
    ).decode().strip()
    assert out == "mille deux cent trente-quatre"


def test_runpy_list_languages():
    out = subprocess.check_output(
        [sys.executable, "-m", "num2words2", "--list-languages"]
    ).decode()
    assert "en" in out.split()
    assert "fr" in out.split()


def test_precision_kwarg():
    # Issue #580 — precision= overrides default 2-digit fractional precision.
    assert num2words2.num2words(3.14159, lang="en", precision=5) == \
        "three point one four one five nine"
    # Default precision (2) unchanged when no kwarg.
    assert num2words2.num2words(3.14, lang="en") == "three point one four"
