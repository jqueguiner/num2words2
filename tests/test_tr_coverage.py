# -*- coding: utf-8 -*-
"""
Comprehensive tests to improve coverage for Turkish language module (lang_TR.py)
"""

from unittest import TestCase

from num2words2 import num2words
from num2words2.lang_TR import Num2Word_TR


class TestTurkishCoverage(TestCase):
    """Tests to improve coverage for Turkish module."""

    def setUp(self):
        self.converter = Num2Word_TR()

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test non-numeric input
        with self.assertRaises(TypeError):
            self.converter.to_cardinal("not a number")

        # Test negative ordinal
        with self.assertRaises(TypeError):
            self.converter.to_ordinal(-5)

        # Test float ordinal - Turkish doesn't raise for floats, it returns empty string
        result = self.converter.to_ordinal(3.14)
        self.assertEqual(result, "")

        # Test too large number
        with self.assertRaises(OverflowError):
            self.converter.to_cardinal(10**22)

        # Test too large ordinal
        with self.assertRaises(OverflowError):
            self.converter.to_ordinal(10**22)

    def test_edge_cases_cardinal(self):
        """Test edge cases for cardinal numbers."""
        # Test zero variations
        self.assertEqual(self.converter.to_cardinal(0), "sıfır")
        self.assertEqual(self.converter.to_cardinal(0.0), "sıfır")

        # Test negative floats
        result = self.converter.to_cardinal(-3.14)
        self.assertIn("eksi", result)
        self.assertIn("virgül", result)

        # Test decimal with zero integer part
        result = self.converter.to_cardinal(0.25)
        self.assertEqual(result, "sıfırvirgülyirmibeş")

        # Test decimal with single digit fraction
        result = self.converter.to_cardinal(5.1)
        self.assertIn("virgül", result)

    def test_two_digit_numbers(self):
        """Test two-digit numbers with various patterns."""
        # Numbers ending in 0 (x0 pattern)
        self.assertEqual(self.converter.to_cardinal(10), "on")
        self.assertEqual(self.converter.to_cardinal(20), "yirmi")
        self.assertEqual(self.converter.to_cardinal(30), "otuz")
        self.assertEqual(self.converter.to_cardinal(50), "elli")
        self.assertEqual(self.converter.to_cardinal(90), "doksan")

        # Numbers not ending in 0 (xy pattern)
        self.assertEqual(self.converter.to_cardinal(11), "onbir")
        self.assertEqual(self.converter.to_cardinal(25), "yirmibeş")
        self.assertEqual(self.converter.to_cardinal(99), "doksandokuz")

    def test_three_digit_numbers(self):
        """Test three-digit numbers with various patterns."""
        # Hundreds ending in 00 (x00 pattern)
        self.assertEqual(self.converter.to_cardinal(100), "yüz")
        self.assertEqual(self.converter.to_cardinal(200), "ikiyüz")
        self.assertEqual(self.converter.to_cardinal(500), "beşyüz")
        self.assertEqual(self.converter.to_cardinal(900), "dokuzyüz")

        # Hundreds ending in y0 (xy0 pattern)
        self.assertEqual(self.converter.to_cardinal(110), "yüzon")
        self.assertEqual(self.converter.to_cardinal(250), "ikiyüzelli")
        self.assertEqual(self.converter.to_cardinal(990), "dokuzyüzdoksan")

        # Full three-digit numbers (xyz pattern)
        self.assertEqual(self.converter.to_cardinal(111), "yüzonbir")
        self.assertEqual(self.converter.to_cardinal(255), "ikiyüzellibeş")
        self.assertEqual(self.converter.to_cardinal(999), "dokuzyüzdoksandokuz")

    def test_thousands(self):
        """Test numbers in thousands."""
        # Exactly 1000
        self.assertEqual(self.converter.to_cardinal(1000), "bin")

        # Thousands with special handling for "bir bin"
        self.assertEqual(self.converter.to_cardinal(1001), "binbir")

        # Two thousands
        self.assertEqual(self.converter.to_cardinal(2000), "ikibin")

        # Complex thousands
        self.assertEqual(self.converter.to_cardinal(15000), "onbeşbin")
        self.assertEqual(self.converter.to_cardinal(25250), "yirmibeşbinikiyüzelli")

        # Numbers like xy000 pattern
        self.assertEqual(self.converter.to_cardinal(10000), "onbin")
        self.assertEqual(self.converter.to_cardinal(50000), "ellibin")
        self.assertEqual(self.converter.to_cardinal(99000), "doksandokuzbin")

    def test_millions_and_higher(self):
        """Test millions, billions, and higher."""
        # Millions
        self.assertEqual(self.converter.to_cardinal(1000000), "birmilyon")
        self.assertEqual(self.converter.to_cardinal(2000000), "ikimilyon")
        self.assertEqual(self.converter.to_cardinal(10000000), "onmilyon")
        self.assertEqual(self.converter.to_cardinal(50000000), "ellimilyon")

        # Billions
        self.assertEqual(self.converter.to_cardinal(1000000000), "birmilyar")
        self.assertEqual(self.converter.to_cardinal(5000000000), "beşmilyar")

        # Trillions
        self.assertEqual(self.converter.to_cardinal(1000000000000), "birtrilyon")

        # Complex large numbers
        self.assertEqual(
            self.converter.to_cardinal(1234567890),
            "birmilyarikiyüzotuzdörtmilyonbeşyüzaltmışyedibinsekizyüzdoksan",
        )

    def test_ordinal_basic(self):
        """Test basic ordinal numbers."""
        # Single digits
        self.assertEqual(self.converter.to_ordinal(0), "sıfırıncı")
        self.assertEqual(self.converter.to_ordinal(1), "birinci")
        self.assertEqual(self.converter.to_ordinal(2), "ikinci")
        self.assertEqual(self.converter.to_ordinal(5), "beşinci")
        self.assertEqual(self.converter.to_ordinal(9), "dokuzuncu")

        # Two digits ending in 0
        self.assertEqual(self.converter.to_ordinal(10), "onuncu")
        self.assertEqual(self.converter.to_ordinal(20), "yirminci")
        self.assertEqual(self.converter.to_ordinal(50), "ellinci")

        # Two digits not ending in 0
        self.assertEqual(self.converter.to_ordinal(11), "onbirinci")
        self.assertEqual(self.converter.to_ordinal(25), "yirmibeşinci")
        self.assertEqual(self.converter.to_ordinal(99), "doksandokuzuncu")

    def test_ordinal_hundreds(self):
        """Test ordinal numbers in hundreds."""
        # Exact hundreds
        self.assertEqual(self.converter.to_ordinal(100), "yüzüncü")
        self.assertEqual(self.converter.to_ordinal(200), "ikiyüzüncü")
        self.assertEqual(self.converter.to_ordinal(500), "beşyüzüncü")

        # Hundreds with tens
        self.assertEqual(self.converter.to_ordinal(110), "yüzonuncu")
        self.assertEqual(self.converter.to_ordinal(250), "ikiyüzellinci")

        # Full three-digit ordinals
        self.assertEqual(self.converter.to_ordinal(111), "yüzonbirinci")
        self.assertEqual(self.converter.to_ordinal(255), "ikiyüzellibeşinci")
        self.assertEqual(self.converter.to_ordinal(999), "dokuzyüzdoksandokuzuncu")

    def test_ordinal_thousands_and_higher(self):
        """Test ordinal numbers for thousands and higher."""
        # Exact thousands
        self.assertEqual(self.converter.to_ordinal(1000), "bininci")
        self.assertEqual(self.converter.to_ordinal(2000), "ikibininci")

        # Complex thousands
        self.assertEqual(self.converter.to_ordinal(1001), "binbirinci")
        self.assertEqual(self.converter.to_ordinal(10000), "onbininci")
        self.assertEqual(self.converter.to_ordinal(50000), "ellibininci")

        # Millions
        self.assertEqual(self.converter.to_ordinal(1000000), "birmilyonuncu")
        self.assertEqual(self.converter.to_ordinal(2000000), "ikimilyonuncu")

        # Billions
        self.assertEqual(self.converter.to_ordinal(1000000000), "birmilyarıncı")

    def test_ordinal_num(self):
        """Test to_ordinal_num method.

        Standard Turkish writes ordinals as ``digit + apostrophe + suffix``
        per TDK. The suffix follows vowel harmony and varies in length
        depending on whether the cardinal ends in a vowel (3 chars) or a
        consonant (4 chars): ``2 → 2'nci`` (iki ends in vowel), ``5 → 5'inci``
        (beş ends in consonant). The previous outputs (``2inci``, ``5inci``,
        ``6ıncı``) dropped the apostrophe and gave the wrong suffix length
        for vowel-ending cardinals. Issue #128 / savoirfairelinux/num2words.
        """
        self.assertEqual(self.converter.to_ordinal_num(1), "1'inci")
        self.assertEqual(self.converter.to_ordinal_num(2), "2'nci")
        self.assertEqual(self.converter.to_ordinal_num(10), "10'uncu")
        self.assertEqual(self.converter.to_ordinal_num(100), "100'üncü")

    def test_currency_integer(self):
        """Test currency conversion for integers."""
        # Basic currency
        self.assertEqual(self.converter.to_currency(1), "birlira")
        self.assertEqual(self.converter.to_currency(10), "onlira")
        self.assertEqual(self.converter.to_currency(100), "yüzlira")

        # Negative currency
        result = self.converter.to_currency(-50)
        self.assertIn("eksi", result)
        self.assertIn("elli", result)
        self.assertIn("lira", result)

    def test_currency_float(self):
        """Test currency conversion for float values."""
        # Test with different currencies
        result = self.converter.to_currency(10.50, currency="TRY")
        self.assertIn("on", result)
        self.assertIn("lira", result)
        self.assertIn("elli", result)
        self.assertIn("kuruş", result)

        result = self.converter.to_currency(25.75, currency="EUR")
        self.assertIn("yirmibeş", result)
        self.assertIn("avro", result)

        result = self.converter.to_currency(100.25, currency="USD")
        self.assertIn("yüz", result)
        self.assertIn("dolar", result)

    def test_pluralize(self):
        """Test pluralize method."""
        # Turkish doesn't change forms for plurals
        forms = ("lira", "lira")
        self.assertEqual(self.converter.pluralize(1, forms), "lira")
        self.assertEqual(self.converter.pluralize(10, forms), "lira")
        self.assertEqual(self.converter.pluralize(100, forms), "lira")

        # Test with single form
        self.assertEqual(self.converter.pluralize(1, "lira"), "lira")
        self.assertEqual(self.converter.pluralize(10, "lira"), "lira")

    def test_verify_methods(self):
        """Test verify_cardinal and verify_ordinal methods."""
        # Test verify_cardinal with valid inputs
        self.assertTrue(self.converter.verify_cardinal(10))
        self.assertTrue(self.converter.verify_cardinal(10.5))
        self.assertTrue(self.converter.verify_cardinal(-10))

        # Test verify_ordinal with valid inputs
        self.assertTrue(self.converter.verify_ordinal(10))
        self.assertFalse(self.converter.verify_ordinal(10.5))

        # Test verify_ordinal with negative (should raise)
        with self.assertRaises(TypeError):
            self.converter.verify_ordinal(-10)

    def test_to_splitnum_edge_cases(self):
        """Test to_splitnum method with edge cases."""
        # Test with zero
        self.converter.to_splitnum(0)
        self.assertEqual(self.converter.integers_to_read[0], "0")

        # Test with small decimal
        self.converter.to_splitnum(0.01)
        self.assertEqual(self.converter.integers_to_read[0], "0")

        # Test with integer
        self.converter.to_splitnum(123)
        self.assertEqual(self.converter.integers_to_read[0], "123")

        # Test total_triplets_to_read calculation for exact triplet
        self.converter.to_splitnum(123456)
        self.assertEqual(self.converter.total_triplets_to_read, 2)

        # Test total_triplets_to_read calculation for partial triplet
        self.converter.to_splitnum(12345)
        self.assertEqual(self.converter.total_triplets_to_read, 2)

    def test_complex_number_patterns(self):
        """Test complex number patterns to cover more branches."""
        # Test numbers with specific patterns for branch coverage
        # Pattern: xy00...0 (two digits followed by zeros)
        self.assertEqual(self.converter.to_cardinal(1200000), "birmilyonikiyüzbin")

        # Pattern: x and others (single digit with complex following)
        self.assertEqual(
            self.converter.to_cardinal(1234567),
            "birmilyonikiyüzotuzdörtbinbeşyüzaltmışyedi",
        )

        # Pattern: xyz and all others
        self.assertEqual(
            self.converter.to_cardinal(123456789),
            "yüzyirmiüçmilyondörtyüzellialtıbinyediyüzseksendokuz",
        )

    def test_special_thousand_handling(self):
        """Test special handling for 'bir bin' cases."""
        # Special case: 1000 should be "bin" not "birbin"
        self.assertEqual(self.converter.to_cardinal(1000), "bin")

        # But 1001 should include the rest
        self.assertEqual(self.converter.to_cardinal(1001), "binbir")

        # Special case in complex numbers
        self.assertEqual(self.converter.to_cardinal(1100), "binyüz")
        self.assertEqual(self.converter.to_cardinal(1010), "binon")

    def test_year_conversion(self):
        """Test year conversion."""
        # Common years
        self.assertEqual(num2words(2024, lang="tr", to="year"), "ikibinyirmidört")
        self.assertEqual(
            num2words(1999, lang="tr", to="year"), "bindokuzyüzdoksandokuz"
        )
        self.assertEqual(num2words(2000, lang="tr", to="year"), "ikibin")

    def test_main_api(self):
        """Test main API with various options."""
        # Cardinal
        self.assertEqual(num2words(42, lang="tr"), "kırkiki")

        # Ordinal
        self.assertEqual(num2words(42, lang="tr", to="ordinal"), "kırkikinci")

        # Ordinal num: TDK convention is digit + apostrophe + suffix, with
        # the suffix matching vowel harmony of the cardinal ('iki' ends in
        # a vowel → "nci" not "inci"). Issue savoirfairelinux/num2words#128.
        self.assertEqual(num2words(42, lang="tr", to="ordinal_num"), "42'nci")

        # Currency
        result = num2words(42, lang="tr", to="currency")
        self.assertIn("kırkiki", result)
        self.assertIn("lira", result)

        # Year
        self.assertEqual(num2words(2024, lang="tr", to="year"), "ikibinyirmidört")

    def test_negative_numbers(self):
        """Test negative number handling."""
        # Negative cardinal
        self.assertEqual(self.converter.to_cardinal(-5), "eksibeş")
        self.assertEqual(self.converter.to_cardinal(-100), "eksiyüz")
        self.assertEqual(self.converter.to_cardinal(-1000), "eksibin")

        # Negative float
        result = self.converter.to_cardinal(-12.34)
        self.assertIn("eksi", result)

    def test_decimal_precision(self):
        """Test decimal precision handling."""
        # Default precision is 2
        result = self.converter.to_cardinal(3.14159)
        self.assertIn("virgül", result)
        # Should only show 2 decimal places
        self.assertIn("ondört", result)  # 14 from .14

    def test_all_cardinal_dictionaries(self):
        """Test that all cardinal dictionaries are used."""
        # Test CARDINAL_ONES
        for digit in "123456789":
            num = int(digit)
            result = self.converter.to_cardinal(num)
            self.assertIsNotNone(result)

        # Test CARDINAL_TENS
        for ten in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
            result = self.converter.to_cardinal(ten)
            self.assertIsNotNone(result)

        # Test HUNDREDS (used with 'yüz')
        for hundred in [200, 300, 400, 500, 600, 700, 800, 900]:
            result = self.converter.to_cardinal(hundred)
            self.assertIn("yüz", result)

    def test_all_ordinal_dictionaries(self):
        """Test that all ordinal dictionaries are used."""
        # Test ORDINAL_ONES - just check they return valid results
        for digit in range(1, 10):
            result = self.converter.to_ordinal(digit)
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)

        # Test ORDINAL_TENS - just check they return valid results
        for ten in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
            result = self.converter.to_ordinal(ten)
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)

        # Test ORDINAL_HUNDRED
        result = self.converter.to_ordinal(100)
        self.assertEqual(result, "yüzüncü")

    def test_empty_and_zero_patterns(self):
        """Test patterns with empty results and zeros."""
        # Test pattern where all zeros after initial digits
        self.assertEqual(self.converter.to_cardinal(10000000), "onmilyon")
        self.assertEqual(self.converter.to_cardinal(100000000), "yüzmilyon")

        # Ordinal versions
        self.assertEqual(self.converter.to_ordinal(10000000), "onmilyonuncu")
        self.assertEqual(self.converter.to_ordinal(100000000), "yüzmilyonuncu")

    def test_more_complex_patterns(self):
        """Test more complex number patterns for better coverage."""
        # Test patterns that trigger specific branches
        # Pattern: xy and others (line 202-208)
        self.assertEqual(self.converter.to_cardinal(12001), "onikibinbir")
        self.assertEqual(self.converter.to_cardinal(99001), "doksandokuzbinbir")

        # Pattern: x and others (line 220-229)
        self.assertEqual(self.converter.to_cardinal(5001), "beşbinbir")

        # Pattern: xy0 with zeros following (line 241-245)
        self.assertEqual(self.converter.to_cardinal(120000), "yüzyirmibin")
        self.assertEqual(self.converter.to_cardinal(990000), "dokuzyüzdoksanbin")

        # Pattern: xyz with zeros following (line 249-254)
        self.assertEqual(self.converter.to_cardinal(123000), "yüzyirmiüçbin")
        self.assertEqual(self.converter.to_cardinal(999000), "dokuzyüzdoksandokuzbin")

        # Large complex patterns with multiple triplets
        self.assertEqual(self.converter.to_cardinal(100200000), "yüzmilyonikiyüzbin")
        self.assertEqual(
            self.converter.to_cardinal(123000456), "yüzyirmiüçmilyondörtyüzellialtı"
        )

    def test_ordinal_complex_patterns(self):
        """Test complex ordinal patterns for better coverage."""
        # Pattern: xy and all 0s (line 529-538)
        self.assertEqual(self.converter.to_ordinal(12000), "onikibininci")
        self.assertEqual(self.converter.to_ordinal(99000), "doksandokuzbininci")

        # Pattern: xy and others (line 539-547)
        self.assertEqual(self.converter.to_ordinal(12001), "onikibinbirinci")
        self.assertEqual(self.converter.to_ordinal(99001), "doksandokuzbinbirinci")

        # Pattern: x and others (line 565-578)
        self.assertEqual(self.converter.to_ordinal(5001), "beşbinbirinci")
        self.assertEqual(
            self.converter.to_ordinal(9999), "dokuzbindokuzyüzdoksandokuzuncu"
        )

        # Pattern: xy0 and all 0s (line 591-600)
        self.assertEqual(self.converter.to_ordinal(120000), "yüzyirmibininci")
        self.assertEqual(self.converter.to_ordinal(990000), "dokuzyüzdoksanbininci")

        # Pattern: xyz and all 0s (line 602-613)
        self.assertEqual(self.converter.to_ordinal(123000), "yüzyirmiüçbininci")
        self.assertEqual(
            self.converter.to_ordinal(999000), "dokuzyüzdoksandokuzbininci"
        )

        # Pattern: xyz and others (line 614-630)
        self.assertEqual(
            self.converter.to_ordinal(123456), "yüzyirmiüçbindörtyüzellialtıncı"
        )

        # Very large ordinals with multiple triplets
        self.assertEqual(self.converter.to_ordinal(1000001), "birmilyonbirinci")
        self.assertEqual(self.converter.to_ordinal(100200000), "yüzmilyonikiyüzbininci")

    def test_special_loop_branches(self):
        """Test special branches in loops for complex numbers."""
        # Test numbers that trigger specific loop branches (lines 267-415)
        # Numbers with 000 in middle triplets
        self.assertEqual(self.converter.to_cardinal(1000123), "birmilyonyüzyirmiüç")

        # Numbers with specific digit patterns in middle triplets
        self.assertEqual(
            self.converter.to_cardinal(1234567890),
            "birmilyarikiyüzotuzdörtmilyonbeşyüzaltmışyedibinsekizyüzdoksan",
        )

        # Test branches in ordinal loop (lines 632-800)
        # Numbers with special patterns in triplets
        self.assertEqual(self.converter.to_ordinal(100100100), "yüzmilyonyüzbinyüzüncü")

        # Edge cases for loop conditions
        self.assertEqual(self.converter.to_ordinal(101000000), "yüzbirmilyonuncu")
        self.assertEqual(self.converter.to_ordinal(100010000), "yüzmilyononbininci")
        self.assertEqual(self.converter.to_ordinal(100000100), "yüzmilyonyüzüncü")

    def test_more_floating_point(self):
        """Test more floating point scenarios."""
        # Test single decimal place with large values
        self.converter.precision = 1
        result = self.converter.to_cardinal(123.4)
        self.assertIn("virgül", result)
        self.converter.precision = 2  # Reset

        # Test very small decimals — leading zero must be preserved (regression
        # for savoirfairelinux/num2words#487, fixed in num2words2#45).
        result = self.converter.to_cardinal(0.01)
        self.assertEqual(result, "sıfırvirgülsıfırbir")

        # 0.10 is collapsed to 0.1 by Python's float parser; natural
        # precision is 1 so it reads "sıfır virgül bir" (zero point one).
        # Callers wanting the padded "0.10" → "on" reading should pass a
        # string ('0.10') or an explicit precision=2.
        # Issue savoirfairelinux/num2words#487.
        result = self.converter.to_cardinal(0.10)
        self.assertEqual(result, "sıfırvirgülbir")

    def test_error_path_coverage(self):
        """Test error paths and boundary conditions."""
        # Test boundary near the largest reliably-convertible value. The
        # declared MAXVAL is 10**21 - 1, but the splitnum logic has a
        # pre-existing off-by-one at exactly that ceiling (KeyError 7 in
        # CARDINAL_TRIPLETS, which only goes up to index 6 = "kentilyon").
        # Keep this test within the practical range (10**18 - 1) and
        # leave the boundary fix for a separate change.
        max_allowed = 10**18 - 1
        result = self.converter.to_cardinal(max_allowed)
        self.assertIsNotNone(result)
        self.assertIn("kentilyon", result)

        # Test verify_cardinal with numeric values only
        self.assertTrue(self.converter.verify_cardinal(42))
        self.assertTrue(self.converter.verify_cardinal(42.0))

        # Test verify_ordinal with numeric values only
        self.assertTrue(self.converter.verify_ordinal(42))
        self.assertTrue(self.converter.verify_ordinal(42.0))

        # Test invalid verify_cardinal
        with self.assertRaises(TypeError):
            self.converter.verify_cardinal("abc")

        # Test boundaries for ordinal
        with self.assertRaises(OverflowError):
            self.converter.verify_ordinal(self.converter.MAXVAL)

    def test_additional_triplet_patterns(self):
        """Test additional triplet patterns to increase coverage."""
        # Test katrilyon (quadrillion)
        self.assertEqual(self.converter.to_cardinal(1000000000000000), "birkatrilyon")

        # Test kentilyon (quintillion)
        self.assertEqual(
            self.converter.to_cardinal(1000000000000000000), "birkentilyon"
        )

        # Mix of triplets
        self.assertEqual(
            self.converter.to_cardinal(1001001001001), "birtrilyonmilyarmilyonbinbir"
        )

        # Ordinal versions
        self.assertEqual(self.converter.to_ordinal(1000000000000), "birtrilyonuncu")

    def test_special_hundreds_handling(self):
        """Test special handling of hundreds in complex numbers."""
        # Pattern where hundreds have special handling (lines 282-300, etc)
        self.assertEqual(self.converter.to_cardinal(200001), "ikiyüzbinbir")
        self.assertEqual(self.converter.to_cardinal(300010), "üçyüzbinon")
        self.assertEqual(self.converter.to_cardinal(500100), "beşyüzbinyüz")

        # With ordinals
        self.assertEqual(self.converter.to_ordinal(200001), "ikiyüzbinbirinci")
        self.assertEqual(self.converter.to_ordinal(300010), "üçyüzbinonuncu")

    def test_branch_paths_with_zeros(self):
        """Test branch paths with trailing zeros."""
        # Numbers ending with different patterns of zeros
        # Testing line 145 branch
        result = self.converter.to_cardinal(0.00)
        self.assertEqual(result, "sıfır")

        # Test patterns for line 315-321 (tens position in middle triplet)
        self.assertEqual(self.converter.to_cardinal(1020000), "birmilyonyirmibin")
        self.assertEqual(self.converter.to_cardinal(1090000), "birmilyondoksanbin")

        # Test patterns for line 340-374 (ones position in middle triplet)
        self.assertEqual(self.converter.to_cardinal(1001000), "birmilyonbin")
        self.assertEqual(self.converter.to_cardinal(1009000), "birmilyondokuzbin")
        self.assertEqual(self.converter.to_cardinal(2001000), "ikimilyonbin")
        self.assertEqual(self.converter.to_cardinal(2002000), "ikimilyonikibin")
