"""
Simple tests to improve coverage for low-coverage language modules.
Focus on exercising code paths rather than exact output validation.
"""

from unittest import TestCase

from num2words2 import num2words


class TestLowCoverageLanguages(TestCase):
    """Simple tests to improve coverage for various language modules."""

    def test_turkish_coverage(self):
        """Exercise Turkish language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 15, 20, 25, 100, 1000, 10000, 1000000]:
            result = num2words(num, lang="tr")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 3, 10, 100]:
            result = num2words(num, lang="tr", to="ordinal")
            self.assertIsNotNone(result)

        # Ordinal numbers
        for num in [1, 5, 10]:
            result = num2words(num, lang="tr", to="ordinal_num")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="tr", to="currency", currency="TRY")
        self.assertIsNotNone(result)

        result = num2words(50, lang="tr", to="currency", currency="USD")
        self.assertIsNotNone(result)

        # Negative numbers
        result = num2words(-10, lang="tr")
        self.assertIn("eksi", result)

        # Decimal numbers
        result = num2words(3.14, lang="tr")
        self.assertIn("virgül", result)

        # Year
        result = num2words(2024, lang="tr", to="year")
        self.assertIsNotNone(result)

    def test_albanian_coverage(self):
        """Exercise Albanian language code paths."""
        # Basic numbers
        for num in [0, 1, 2, 10, 20, 100, 1000]:
            result = num2words(num, lang="sq")
            self.assertIsNotNone(result)

        # Compound numbers
        for num in [11, 25, 101, 1001]:
            result = num2words(num, lang="sq")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 3, 10]:
            result = num2words(num, lang="sq", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="sq", to="currency")
        self.assertIsNotNone(result)

        # Negative and decimal
        result = num2words(-10, lang="sq")
        self.assertIsNotNone(result)

        result = num2words(3.14, lang="sq")
        self.assertIsNotNone(result)

    def test_gujarati_coverage(self):
        """Exercise Gujarati language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 100, 1000]:
            result = num2words(num, lang="gu")
            self.assertIsNotNone(result)

        # Indian number system
        for num in [100000, 10000000]:  # Lakh and Crore
            result = num2words(num, lang="gu")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 3, 10]:
            result = num2words(num, lang="gu", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="gu", to="currency", currency="INR")
        self.assertIsNotNone(result)

    def test_marathi_coverage(self):
        """Exercise Marathi language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 100, 1000]:
            result = num2words(num, lang="mr")
            self.assertIsNotNone(result)

        # Compound numbers
        for num in [42, 250]:
            result = num2words(num, lang="mr")
            self.assertIsNotNone(result)

        # Indian number system
        for num in [100000, 10000000]:  # Lakh and Crore
            result = num2words(num, lang="mr")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 3, 10]:
            result = num2words(num, lang="mr", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="mr", to="currency", currency="INR")
        self.assertIsNotNone(result)

    def test_malay_coverage(self):
        """Exercise Malay language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 100, 1000]:
            result = num2words(num, lang="ms")
            self.assertIsNotNone(result)

        # Compound numbers
        for num in [11, 21, 99]:
            result = num2words(num, lang="ms")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 10]:
            result = num2words(num, lang="ms", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="ms", to="currency", currency="MYR")
        self.assertIsNotNone(result)

        # Negative and decimal
        result = num2words(-10, lang="ms")
        self.assertIsNotNone(result)

        result = num2words(3.14, lang="ms")
        self.assertIsNotNone(result)

    def test_swedish_coverage(self):
        """Exercise Swedish language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 100, 1000]:
            result = num2words(num, lang="sv")
            self.assertIsNotNone(result)

        # Compound numbers
        for num in [21, 42, 99]:
            result = num2words(num, lang="sv")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 3, 10]:
            result = num2words(num, lang="sv", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="sv", to="currency", currency="SEK")
        self.assertIsNotNone(result)

        # Year
        result = num2words(2024, lang="sv", to="year")
        self.assertIsNotNone(result)

    def test_danish_coverage(self):
        """Exercise Danish language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 100, 1000]:
            result = num2words(num, lang="da")
            self.assertIsNotNone(result)

        # Danish special counting (vigesimal)
        for num in [50, 60, 70, 80, 90]:
            result = num2words(num, lang="da")
            self.assertIsNotNone(result)

        # Compound numbers
        for num in [51, 75, 99]:
            result = num2words(num, lang="da")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 10]:
            result = num2words(num, lang="da", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="da", to="currency", currency="DKK")
        self.assertIsNotNone(result)

    def test_shona_coverage(self):
        """Exercise Shona language code paths."""
        # Basic numbers
        for num in [0, 1, 2, 10, 100, 1000]:
            result = num2words(num, lang="sn")
            self.assertIsNotNone(result)

        # Compound numbers
        for num in [11, 20]:
            result = num2words(num, lang="sn")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2]:
            result = num2words(num, lang="sn", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="sn", to="currency")
        self.assertIsNotNone(result)

    def test_swahili_coverage(self):
        """Exercise Swahili language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 100, 1000]:
            result = num2words(num, lang="sw")
            self.assertIsNotNone(result)

        # Compound numbers
        for num in [11, 25, 99]:
            result = num2words(num, lang="sw")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2]:
            result = num2words(num, lang="sw", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="sw", to="currency", currency="KES")
        self.assertIsNotNone(result)

    def test_telugu_coverage(self):
        """Exercise Telugu language code paths."""
        # Basic numbers
        for num in [0, 1, 10, 100, 1000]:
            result = num2words(num, lang="te")
            self.assertIsNotNone(result)

        # Indian number system
        for num in [100000, 10000000]:  # Lakh and Crore
            result = num2words(num, lang="te")
            self.assertIsNotNone(result)

        # Ordinals
        for num in [1, 2, 3, 10]:
            result = num2words(num, lang="te", to="ordinal")
            self.assertIsNotNone(result)

        # Currency
        result = num2words(100.50, lang="te", to="currency", currency="INR")
        self.assertIsNotNone(result)

    def test_greek_additional_coverage(self):
        """Exercise additional Greek language code paths."""
        # Large ordinals
        for num in [10000, 100000, 1000000]:
            result = num2words(num, lang="el", to="ordinal")
            self.assertIsNotNone(result)

        # Ordinal num format
        for num in [1, 2, 3, 10, 21, 100]:
            result = num2words(num, lang="el", to="ordinal_num")
            self.assertIsNotNone(result)

        # Currency with different values
        result = num2words(-50.50, lang="el", to="currency")
        self.assertIsNotNone(result)

        # Year conversion
        for year in [1999, 2000, 2024, 1821]:
            result = num2words(year, lang="el", to="year")
            self.assertIsNotNone(result)

    def test_slovenian_additional_coverage(self):
        """Exercise additional Slovenian language code paths."""
        # Test merge operations with large numbers
        for num in [1000001, 2000000, 1000000000]:
            result = num2words(num, lang="sl")
            self.assertIsNotNone(result)

        # Test various ordinals
        for num in [100, 200, 1000, 10000]:
            result = num2words(num, lang="sl", to="ordinal")
            self.assertIsNotNone(result)

        # Test negative currency
        result = num2words(-100.50, lang="sl", to="currency")
        self.assertIsNotNone(result)
