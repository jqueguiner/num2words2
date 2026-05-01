# -*- coding: utf-8 -*-
"""Coverage for the two currency features deferred until v1.0.12.

- savoirfairelinux/num2words#256 — 3-decimal currencies (BHD/KWD/TND/...).
  The subunit is mils (1/1000) instead of cents (1/100). Driven by a
  per-currency ``CURRENCY_PRECISION`` map and a ``divisor`` argument
  threaded through ``parse_currency_parts``.

- savoirfairelinux/num2words#364 — cheque format. New ``to='cheque'``
  conversion type emits the bank-style "ONE THOUSAND AND 56/100 DOLLARS"
  formatting. Uses the same per-currency precision so a BHD cheque ends
  with ``234/1000 DINARS``.
"""
from __future__ import unicode_literals

import unittest

from num2words2 import num2words


class TestThreeDecimalCurrency(unittest.TestCase):
    """savoirfairelinux/num2words#256 — 3-decimal currencies."""

    def test_bhd_with_mils(self):
        self.assertEqual(
            num2words(5.123, lang="en", to="currency", currency="BHD"),
            "five dinars, one hundred and twenty-three fils",
        )

    def test_kwd_with_mils(self):
        self.assertEqual(
            num2words(1.500, lang="en", to="currency", currency="KWD"),
            "one dinar, five hundred fils",
        )

    def test_tnd_millimes(self):
        self.assertEqual(
            num2words(0.001, lang="en", to="currency", currency="TND"),
            "zero dinars, one millime",
        )

    def test_omr_baisa(self):
        self.assertEqual(
            num2words(2.250, lang="en", to="currency", currency="OMR"),
            "two rials, two hundred and fifty baisa",
        )

    def test_jod_fils(self):
        self.assertEqual(
            num2words(10.005, lang="en", to="currency", currency="JOD"),
            "ten dinars, five fils",
        )

    def test_lyd_dirhams(self):
        out = num2words(3.999, lang="en", to="currency", currency="LYD")
        self.assertIn("dinars", out)
        self.assertIn("dirhams", out)

    def test_iqd_fils(self):
        self.assertEqual(
            num2words(1.000, lang="en", to="currency", currency="IQD"),
            "one dinar, zero fils",
        )

    def test_three_decimal_integer_no_cents(self):
        # Pure int input doesn't show the subunit segment.
        self.assertEqual(
            num2words(5, lang="en", to="currency", currency="BHD"),
            "five dinars",
        )

    def test_two_decimal_unchanged(self):
        # Default precision (cents) is preserved.
        self.assertEqual(
            num2words(1.05, lang="en", to="currency", currency="EUR"),
            "one euro, five cents",
        )
        self.assertEqual(
            num2words(1234.56, lang="en", to="currency", currency="USD"),
            "one thousand, two hundred and thirty-four dollars, fifty-six cents",
        )

    def test_negative_three_decimal(self):
        self.assertTrue(
            num2words(-1.500, lang="en", to="currency", currency="BHD").startswith(
                "minus"
            )
        )

    def test_unknown_currency_still_raises(self):
        with self.assertRaises(NotImplementedError):
            num2words(5.0, lang="en", to="currency", currency="ZZZ")


class TestChequeFormat(unittest.TestCase):
    """savoirfairelinux/num2words#364 — bank cheque format."""

    def test_basic_usd(self):
        self.assertEqual(
            num2words(1234.56, lang="en", to="cheque", currency="USD"),
            "ONE THOUSAND, TWO HUNDRED AND THIRTY-FOUR AND 56/100 DOLLARS",
        )

    def test_zero_cents(self):
        self.assertEqual(
            num2words(1.00, lang="en", to="cheque", currency="USD"),
            "ONE AND 00/100 DOLLARS",
        )

    def test_zero_value(self):
        self.assertEqual(
            num2words(0, lang="en", to="cheque", currency="USD"),
            "ZERO AND 00/100 DOLLARS",
        )

    def test_pure_integer(self):
        # Integer input still gets the cheque-style /100 suffix.
        self.assertEqual(
            num2words(1, lang="en", to="cheque", currency="USD"),
            "ONE AND 00/100 DOLLARS",
        )

    def test_million(self):
        self.assertEqual(
            num2words(1_000_000.99, lang="en", to="cheque", currency="USD"),
            "ONE MILLION AND 99/100 DOLLARS",
        )

    def test_currency_pluralised_for_one(self):
        # Cheque convention writes plural "DOLLARS" even for $1.
        out = num2words(1.00, lang="en", to="cheque", currency="USD")
        self.assertIn("DOLLARS", out)
        self.assertNotIn("DOLLAR ", out)

    def test_negative(self):
        out = num2words(-12.50, lang="en", to="cheque", currency="EUR")
        self.assertTrue(out.startswith("MINUS"))
        self.assertIn("50/100", out)

    def test_three_decimal_currency_on_cheque(self):
        # Cheque format respects the per-currency precision: 3-decimal
        # mils get xxx/1000 instead of xx/100.
        self.assertEqual(
            num2words(1.234, lang="en", to="cheque", currency="BHD"),
            "ONE AND 234/1000 DINARS",
        )

    def test_indian_rupees(self):
        self.assertEqual(
            num2words(100, lang="en", to="cheque", currency="INR"),
            "ONE HUNDRED AND 00/100 RUPEES",
        )

    def test_unknown_currency_raises(self):
        with self.assertRaises(NotImplementedError):
            num2words(1.0, lang="en", to="cheque", currency="ZZZ")


if __name__ == "__main__":
    unittest.main()
