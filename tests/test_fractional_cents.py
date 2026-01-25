# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

"""Test fractional cents support across all languages."""

from __future__ import unicode_literals

import pytest

from num2words2 import num2words


class TestFractionalCentsEN:
    """Test fractional cents in English."""

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        assert (
            num2words(1234.653, lang="en", to="currency", currency="USD")
            == "one thousand, two hundred and thirty-four dollars, sixty-five point three cents"
        )

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        assert (
            num2words(100.123, lang="en", to="currency", currency="EUR")
            == "one hundred euros, twelve point three cents"
        )

    def test_fractional_cents_negative(self):
        """Test negative amount with fractional cents."""
        assert (
            num2words(-50.456, lang="en", to="currency", currency="USD")
            == "minus fifty dollars, forty-five point six cents"
        )

    def test_no_fractional_cents(self):
        """Test that whole cents don't show fractional part."""
        assert (
            num2words(100.25, lang="en", to="currency", currency="USD")
            == "one hundred dollars, twenty-five cents"
        )


class TestFractionalCentsFR:
    """Test fractional cents in French."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        assert (
            num2words(1234.653, lang="fr", to="currency", currency="EUR")
            == "mille deux cent trente-quatre euros et soixante-cinq virgule trois centimes"
        )

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        assert (
            num2words(100.123, lang="fr", to="currency", currency="USD")
            == "cent dollars et douze virgule trois cents"
        )

    def test_fractional_cents_negative(self):
        """Test negative amount with fractional cents."""
        assert (
            num2words(-50.456, lang="fr", to="currency", currency="EUR")
            == "moins cinquante euros et quarante-cinq virgule six centimes"
        )


class TestFractionalCentsDE:
    """Test fractional cents in German."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        assert (
            num2words(1234.653, lang="de", to="currency", currency="EUR")
            == "eintausendzweihundertvierunddreißig Euro und fünfundsechzig Komma drei Cent"
        )

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        assert (
            num2words(100.123, lang="de", to="currency", currency="USD")
            == "einhundert Dollar und zwölf Komma drei Cent"
        )


class TestFractionalCentsES:
    """Test fractional cents in Spanish."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        assert (
            num2words(1234.653, lang="es", to="currency", currency="EUR")
            == "mil doscientos treinta y cuatro euros con sesenta y cinco punto tres céntimos"
        )

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        assert (
            num2words(100.123, lang="es", to="currency", currency="USD")
            == "cien dólares con doce punto tres centavos"
        )


class TestFractionalCentsIT:
    """Test fractional cents in Italian."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="it", to="currency", currency="EUR")
        assert "virgola tre" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="it", to="currency", currency="USD")
        assert "virgola tre" in result


class TestFractionalCentsPL:
    """Test fractional cents in Polish."""

    def test_fractional_cents_pln(self):
        """Test PLN with fractional cents."""
        result = num2words(1234.653, lang="pl", to="currency", currency="PLN")
        assert "przecinek trzy" in result or "przecinek drei" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="pl", to="currency", currency="USD")
        assert "przecinek" in result


class TestFractionalCentsRU:
    """Test fractional cents in Russian."""

    def test_fractional_cents_rub(self):
        """Test RUB with fractional cents."""
        result = num2words(1234.653, lang="ru", to="currency", currency="RUB")
        assert "целых три" in result or "целых три десятых" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="ru", to="currency", currency="USD")
        assert "целых" in result


class TestFractionalCentsUK:
    """Test fractional cents in Ukrainian."""

    def test_fractional_cents_uah(self):
        """Test UAH with fractional cents."""
        result = num2words(1234.653, lang="uk", to="currency", currency="UAH")
        assert "кома три" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="uk", to="currency", currency="USD")
        assert "кома" in result


class TestFractionalCentsKO:
    """Test fractional cents in Korean."""

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(1234.653, lang="ko", to="currency", currency="USD")
        assert "점 삼" in result or "점" in result

    def test_krw_no_decimals(self):
        """Test that KRW doesn't support decimals."""
        with pytest.raises(ValueError):
            num2words(100.123, lang="ko", to="currency", currency="KRW")


class TestFractionalCentsTH:
    """Test fractional cents in Thai."""

    def test_fractional_cents_thb(self):
        """Test THB with fractional cents."""
        result = num2words(1234.653, lang="th", to="currency", currency="THB")
        assert "จุด" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="th", to="currency", currency="USD")
        assert "จุด" in result


class TestFractionalCentsHU:
    """Test fractional cents in Hungarian."""

    def test_fractional_cents_huf(self):
        """Test HUF with fractional cents."""
        result = num2words(1234.653, lang="hu", to="currency", currency="HUF")
        assert "egész három tized" in result or "pont három" in result

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(100.123, lang="hu", to="currency", currency="EUR")
        assert "egész" in result or "pont" in result


class TestFractionalCentsSV:
    """Test fractional cents in Swedish."""

    def test_fractional_cents_sek(self):
        """Test SEK with fractional cents."""
        result = num2words(1234.653, lang="sv", to="currency", currency="SEK")
        assert "komma tre" in result

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(100.123, lang="sv", to="currency", currency="EUR")
        assert "komma" in result


class TestFractionalCentsDA:
    """Test fractional cents in Danish."""

    def test_fractional_cents_dkk(self):
        """Test DKK with fractional cents."""
        result = num2words(1234.653, lang="da", to="currency", currency="DKK")
        assert "komma tre" in result

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(100.123, lang="da", to="currency", currency="EUR")
        assert "komma" in result


class TestFractionalCentsIS:
    """Test fractional cents in Icelandic."""

    def test_fractional_cents_isk(self):
        """Test ISK with fractional cents."""
        result = num2words(1234.653, lang="is", to="currency", currency="ISK")
        assert "komma" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="is", to="currency", currency="USD")
        assert "komma" in result


class TestFractionalCentsLV:
    """Test fractional cents in Latvian."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="lv", to="currency", currency="EUR")
        assert "komats" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="lv", to="currency", currency="USD")
        assert "komats" in result


class TestFractionalCentsCA:
    """Test fractional cents in Catalan."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="ca", to="currency", currency="EUR")
        assert "punt tres" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="ca", to="currency", currency="USD")
        assert "punt" in result


class TestFractionalCentsHE:
    """Test fractional cents in Hebrew."""

    def test_fractional_cents_ils(self):
        """Test ILS with fractional cents."""
        result = num2words(1234.653, lang="he", to="currency", currency="ILS")
        assert "נקודה" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="he", to="currency", currency="USD")
        assert "נקודה" in result


class TestFractionalCentsHI:
    """Test fractional cents in Hindi."""

    def test_fractional_cents_inr(self):
        """Test INR with fractional cents."""
        result = num2words(1234.653, lang="hi", to="currency", currency="INR")
        assert "दशमलव" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="hi", to="currency", currency="USD")
        assert "दशमलव" in result


class TestFractionalCentsKZ:
    """Test fractional cents in Kazakh."""

    def test_fractional_cents_kzt(self):
        """Test KZT with fractional cents."""
        result = num2words(1234.653, lang="kz", to="currency", currency="KZT")
        assert "бүтін үш" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="kz", to="currency", currency="USD")
        assert "бүтін" in result


class TestFractionalCentsLT:
    """Test fractional cents in Lithuanian."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="lt", to="currency", currency="EUR")
        assert "kablelis" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="lt", to="currency", currency="USD")
        assert "kablelis" in result


class TestFractionalCentsTE:
    """Test fractional cents in Telugu."""

    def test_fractional_cents_inr(self):
        """Test INR with fractional cents."""
        result = num2words(1234.653, lang="te", to="currency", currency="INR")
        assert "బిందువు" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="te", to="currency", currency="USD")
        assert "బిందువు" in result or "point" in result


class TestFractionalCentsKN:
    """Test fractional cents in Kannada."""

    def test_fractional_cents_inr(self):
        """Test INR with fractional cents."""
        result = num2words(1234.653, lang="kn", to="currency", currency="INR")
        assert "ಬಿಂದು" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="kn", to="currency", currency="USD")
        assert "ಬಿಂದು" in result or "point" in result


class TestFractionalCentsTG:
    """Test fractional cents in Tajik."""

    def test_fractional_cents_tjs(self):
        """Test TJS with fractional cents."""
        result = num2words(1234.653, lang="tg", to="currency", currency="TJS")
        assert "нуқта" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="tg", to="currency", currency="USD")
        assert "нуқта" in result


class TestFractionalCentsPT:
    """Test fractional cents in Portuguese."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="pt", to="currency", currency="EUR")
        assert "vírgula três" in result

    def test_fractional_cents_brl(self):
        """Test BRL with fractional cents."""
        result = num2words(100.123, lang="pt", to="currency", currency="BRL")
        assert "vírgula" in result


class TestFractionalCentsNL:
    """Test fractional cents in Dutch."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="nl", to="currency", currency="EUR")
        assert "komma drie" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="nl", to="currency", currency="USD")
        assert "komma" in result


class TestFractionalCentsFI:
    """Test fractional cents in Finnish."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="fi", to="currency", currency="EUR")
        assert "pilkku" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="fi", to="currency", currency="USD")
        assert "pilkku" in result


class TestFractionalCentsAF:
    """Test fractional cents in Afrikaans."""

    def test_fractional_cents_zar(self):
        """Test ZAR with fractional cents."""
        result = num2words(1234.653, lang="af", to="currency", currency="ZAR")
        assert "komma" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="af", to="currency", currency="USD")
        assert "komma" in result


class TestFractionalCentsEN_IN:
    """Test fractional cents in Indian English."""

    def test_fractional_cents_inr(self):
        """Test INR with fractional cents."""
        result = num2words(1234.653, lang="en_IN", to="currency", currency="INR")
        assert "point three" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="en_IN", to="currency", currency="USD")
        assert "point" in result


class TestFractionalCentsBG:
    """Test fractional cents in Bulgarian."""

    def test_fractional_cents_bgn(self):
        """Test BGN with fractional cents."""
        result = num2words(1234.653, lang="bg", to="currency", currency="BGN")
        assert "точка" in result or "запетая" in result

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(100.123, lang="bg", to="currency", currency="EUR")
        assert "точка" in result or "запетая" in result


class TestFractionalCentsHR:
    """Test fractional cents in Croatian."""

    def test_fractional_cents_hrk(self):
        """Test HRK with fractional cents."""
        result = num2words(1234.653, lang="hr", to="currency", currency="HRK")
        # Croatian should show "zarez tri" (comma three)
        assert "zarez" in result or "točka" in result

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(100.123, lang="hr", to="currency", currency="EUR")
        assert "zarez" in result or "točka" in result


class TestFractionalCentsSL:
    """Test fractional cents in Slovenian."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="sl", to="currency", currency="EUR")
        assert "vejica" in result or "pika" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="sl", to="currency", currency="USD")
        assert "vejica" in result or "pika" in result


class TestFractionalCentsET:
    """Test fractional cents in Estonian."""

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(1234.653, lang="et", to="currency", currency="EUR")
        assert "koma" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="et", to="currency", currency="USD")
        assert "koma" in result


class TestFractionalCentsHY:
    """Test fractional cents in Armenian."""

    def test_fractional_cents_amd(self):
        """Test AMD with fractional cents."""
        result = num2words(1234.653, lang="hy", to="currency", currency="AMD")
        assert "ամբողջ" in result or "կետ" in result

    def test_fractional_cents_usd(self):
        """Test USD with fractional cents."""
        result = num2words(100.123, lang="hy", to="currency", currency="USD")
        assert "ամբողջ" in result or "կետ" in result


class TestFractionalCentsSQ:
    """Test fractional cents in Albanian."""

    def test_fractional_cents_all(self):
        """Test ALL with fractional cents."""
        result = num2words(1234.653, lang="sq", to="currency", currency="ALL")
        assert "presje" in result or "pikë" in result or "tre" in result

    def test_fractional_cents_eur(self):
        """Test EUR with fractional cents."""
        result = num2words(100.123, lang="sq", to="currency", currency="EUR")
        assert "presje" in result or "pikë" in result or "tre" in result


# Parametrized test for all languages with basic fractional cents support
@pytest.mark.parametrize(
    "lang,currency,expected_fragment",
    [
        ("en", "USD", "point three"),
        ("fr", "EUR", "virgule trois"),
        ("de", "EUR", "Komma drei"),
        ("es", "EUR", "punto tres"),
        ("pt", "EUR", "vírgula três"),
        ("it", "EUR", "virgola tre"),
        ("nl", "EUR", "komma drie"),
        ("pl", "PLN", "przecinek"),
        ("ru", "RUB", "целых"),
        ("uk", "UAH", "кома"),
        ("ko", "USD", "점"),
        ("th", "THB", "จุด"),
        ("hu", "HUF", "egész"),
        ("sv", "SEK", "komma"),
        ("da", "DKK", "komma"),
        ("is", "ISK", "komma"),
        ("lv", "EUR", "komats"),
        ("ca", "EUR", "punt"),
        ("he", "ILS", "נקודה"),
        #     ('hi', 'INR', 'दשमलव'),
        ("kz", "KZT", "бүтін"),
        ("lt", "EUR", "kablelis"),
        ("te", "INR", "బిందువు"),
        #     ('kn', 'INR', 'ಬಿಂದు'),
        ("tg", "TJS", "нуқта"),
        ("fi", "EUR", "pilkku"),
        ("af", "ZAR", "komma"),
        ("en_IN", "INR", "point"),
    ],
)
def test_fractional_cents_parametrized(lang, currency, expected_fragment):
    """Parametrized test for fractional cents across languages."""
    result = num2words(1234.653, lang=lang, to="currency", currency=currency)
    assert (
        expected_fragment in result
    ), f"Expected '{expected_fragment}' in result for {lang}/{currency}, got: {result}"


# Test edge cases
class TestFractionalCentsEdgeCases:
    """Test edge cases for fractional cents."""

    def test_very_small_fraction(self):
        """Test very small fractional amount."""
        result = num2words(0.001, lang="en", to="currency", currency="USD")
        assert "zero dollars" in result and "point one" in result

    def test_large_fraction(self):
        """Test large fractional amount."""
        result = num2words(0.999, lang="en", to="currency", currency="USD")
        assert "ninety-nine point nine" in result

    def test_exact_half_cent(self):
        """Test exact half cent."""
        result = num2words(10.505, lang="en", to="currency", currency="USD")
        assert "fifty point five" in result

    def test_integer_input(self):
        """Test that integer input doesn't show fractional cents."""
        result = num2words(100, lang="en", to="currency", currency="USD")
        assert "point" not in result
        assert result == "one hundred dollars"

    def test_zero_with_fractional_cents(self):
        """Test zero dollars with fractional cents."""
        result = num2words(0.653, lang="en", to="currency", currency="USD")
        assert "sixty-five point three cents" in result


# Additional tests for languages with Unicode that cause issues in parametrized tests
class TestFractionalCentsUnicode:
    """Test fractional cents for languages with Unicode characters."""

    def test_hindi_fractional_cents(self):
        """Test Hindi with fractional cents."""
        result = num2words(1234.653, lang="hi", to="currency", currency="INR")
        assert "दशमलव" in result, f"Expected 'दशमलव' in Hindi result, got: {result}"

    def test_kannada_fractional_cents(self):
        """Test Kannada with fractional cents."""
        result = num2words(1234.653, lang="kn", to="currency", currency="INR")
        assert "ಬಿಂದು" in result, f"Expected 'ಬಿಂದು' in Kannada result, got: {result}"
