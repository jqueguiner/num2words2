from unittest import TestCase

from num2words2 import num2words
from tests.basetest import LangTest


class TestAR(LangTest, TestCase):
    lang = "ar"

    currency_tests = [
        # test_default_currency
        (1, "واحد ريال", {"currency": "SAR"}),
        (2, "اثنان ريالان", {"currency": "SAR"}),
        (10, "عشرة ريالات", {"currency": "SAR"}),
        (100, "مائة ريال", {"currency": "SAR"}),
        (652.12, "ستمائة واثنان وخمسون ريالاً واثنتا عشرة هللة", {"currency": "SAR"}),
        (324, "ثلاثمائة وأربعة وعشرون ريالاً", {"currency": "SAR"}),
        (2000, "ألفا ريال", {"currency": "SAR"}),
        (541, "خمسمائة وواحد وأربعون ريالاً", {"currency": "SAR"}),
        (10000, "عشرة آلاف ريال", {"currency": "SAR"}),
        (20000.12, "عشرون ألف ريال واثنتا عشرة هللة", {"currency": "SAR"}),
        (1000000, "مليون ريال", {"currency": "SAR"}),
        (
            923411,
            "تسعمائة وثلاثة وعشرون ألفاً وأربعمائة وأحد عشر ريالاً",
            {"currency": "SAR"},
        ),
        (63411, "ثلاثة وستون ألفاً وأربعمائة وأحد عشر ريالاً", {"currency": "SAR"}),
        (1000000.99, "مليون ريال وتسع وتسعون هللة", {"currency": "SAR"}),
        # test_currency_parm
        (1, "واحد دينار", {"currency": "KWD"}),
        (10, "عشرة جنيهات", {"currency": "EGP"}),
        (20000.12, "عشرون ألف جنيه واثنتا عشرة قرش", {"currency": "EGP"}),
        (
            923411,
            "تسعمائة وثلاثة وعشرون ألفاً وأربعمائة وأحد عشر ريالاً",
            {"currency": "SR"},
        ),
        (1000000.99, "مليون دينار وتسع وتسعون فلس", {"currency": "KWD"}),
        (1000.42, "ألف دينار وأربعمائة وعشرون مليم", {"currency": "TND"}),
        (123.21, "مائة وثلاثة وعشرون ديناراً ومئتان وعشر مليمات", {"currency": "TND"}),
    ]

    ordinal_tests = [
        (1, "اول"),
        (2, "ثاني"),
        (3, "ثالث"),
        (4, "رابع"),
        (5, "خامس"),
        (6, "سادس"),
        (9, "تاسع"),
        (20, "عشرون"),
        (94, "أربع وتسعون"),
        (102, "مائة واثنان"),
        # from issue #403
        (23, "ثلاث وعشرون"),
    ]

    ordinal_num_tests = [
        (923411, "تسعمائة وثلاثة وعشرون ألفاً وأربعمائة وأحد عشر"),
    ]

    cardinal_tests = [
        (0, "صفر"),
        # These are actually from test_cardinal, but are integers
        (200, "مئتا"),
        (700, "سبعمائة"),
        (101010, "مائة وألف ألف وعشرة"),
        (431, "أربعمائة وواحد وثلاثون"),
        (94231, "أربعة وتسعون ألفاً ومئتان وواحد وثلاثون"),
        (1431, "ألف وأربعمائة وواحد وثلاثون"),
        (740, "سبعمائة وأربعون"),
        (741, "سبعمائة وواحد وأربعون"),
        (262, "مئتان واثنان وستون"),
        (798, "سبعمائة وثمانية وتسعون"),
        (710, "سبعمائة وعشرة"),
        (711, "سبعمائة وأحد عشر"),
        (700, "سبعمائة"),
        (701, "سبعمائة وواحد"),
        (1258888, "مليون ومئتان وثمانية وخمسون ألفاً وثمانمائة وثمانية وثمانون"),
        (1100, "ألف ومائة"),
        (1000000521, "مليار وخمسمائة وواحد وعشرون"),
        # test_big_numbers (large cardinal)
        (
            1000000045000000000000003000000002000000300,
            "تريديسيليون وخمسة وأربعون ديسيليوناً وثلاثة كوينتليونات وملياران وثلاثمائة",
        ),
        (
            9999999999999999999999999999999999999999999999992,
            "تسعة كوينتينيليونات وتسعمائة وتسعة وتسعون كوادريسيليوناً وتسعمائة وتسعة وتسعون تريديسيليوناً وتسعمائة وتسعة وتسعون دوديسيليوناً وتسعمائة وتسعة وتسعون أندسيليوناً وتسعمائة وتسعة وتسعون ديسيليوناً وتسعمائة وتسعة وتسعون نونيليوناً وتسعمائة وتسعة وتسعون أوكتيليوناً وتسعمائة وتسعة وتسعون سبتيليوناً وتسعمائة وتسعة وتسعون سكستيليوناً وتسعمائة وتسعة وتسعون كوينتليوناً وتسعمائة وتسعة وتسعون كوادريليوناً وتسعمائة وتسعة وتسعون تريليوناً وتسعمائة وتسعة وتسعون ملياراً وتسعمائة وتسعة وتسعون مليوناً وتسعمائة وتسعة وتسعون ألفاً وتسعمائة واثنان وتسعون",
        ),
    ]

    float_tests = [
        # From test_cardinal
        (12.3, "اثنا عشر ، ثلاثون"),
        (12.01, "اثنا عشر ، إحدى"),
        (12.02, "اثنا عشر ، اثنتان"),
        (12.03, "اثنا عشر ، ثلاث"),
        (12.34, "اثنا عشر ، أربع وثلاثون"),
        # From test_negative_decimals
        (-0.4, "سالب ، أربعون"),
        (-0.5, "سالب ، خمسون"),
        (-1.4, "سالب واحد ، أربعون"),
    ]

    negative_tests = [
        # From test_cardinal
        (-8324, "سالب ثمانية آلاف وثلاثمائة وأربعة وعشرون"),
        # From test_big_numbers (negative large number)
        (
            -1000000000000000000000003000000002000000302,
            "سالب تريديسيليون وثلاثة كوينتليونات وملياران وثلاثمائة واثنان",
        ),
    ]

    year_tests = [
        (2000, "ألفا"),
    ]

    def test_cardinal(self):
        self._run_cardinal_tests()

    def test_ordinal(self):
        self._run_ordinal_tests()

    def test_ordinal_num(self):
        self._run_ordinal_num_tests()

    def test_year(self):
        self._run_year_tests()

    def test_currency(self):
        self._run_currency_tests()

    def test_float(self):
        self._run_float_tests()

    def test_negative(self):
        self._run_negative_tests()

    # Specific tests that don't fit the generic structure
    def test_prefix_and_suffix(self):
        # Original test had pass, keeping as is for now
        pass

    def test_max_numbers(self):
        for number in 10**51, 10**51 + 2:
            with self.assertRaises(OverflowError) as context:
                num2words(number, lang="ar")
            self.assertTrue("must be less" in str(context.exception))


def test_ar_decimal_uses_arabic_comma_no_double_space():
    # Regression for num2words2#53 (ports savoirfairelinux/num2words#265).
    from num2words2 import num2words
    out = num2words(667851.14, lang="ar")
    assert "،" in out  # Arabic comma U+060C
    assert "," not in out  # no Latin comma
    assert "  " not in out  # no double space


def test_ar_ordinals_use_definite_article_form():
    # Regression for num2words2#54 (ports savoirfairelinux/num2words#403).
    from num2words2 import num2words

    # Single digits — distinct ordinal words with definite article.
    assert num2words(1, lang="ar", to="ordinal") == "الأول"
    assert num2words(2, lang="ar", to="ordinal") == "الثاني"
    assert num2words(10, lang="ar", to="ordinal") == "العاشر"

    # 11 uses the special الحادي root.
    assert num2words(11, lang="ar", to="ordinal") == "الحادي عشر"

    # Round tens take the definite article form.
    assert num2words(20, lang="ar", to="ordinal") == "العشرون"
    assert num2words(50, lang="ar", to="ordinal") == "الخمسون"

    # Compound 20-99: ordinal-ones + و + ال + cardinal-tens.
    assert num2words(24, lang="ar", to="ordinal") == "الرابع والعشرون"
    assert num2words(35, lang="ar", to="ordinal") == "الخامس والثلاثون"
    assert num2words(99, lang="ar", to="ordinal") == "التاسع والتسعون"

    # Hundreds: round 100, 200, …
    assert num2words(100, lang="ar", to="ordinal") == "المائة"
    assert num2words(200, lang="ar", to="ordinal") == "المئتان"

    # 100+ remainder uses بعد + ال + cardinal hundreds.
    assert num2words(122, lang="ar", to="ordinal") == "الثاني والعشرون بعد المائة"
    assert num2words(999, lang="ar", to="ordinal") == "التاسع والتسعون بعد التسعمائة"


def test_ar_ordinals_feminine():
    # Feminine forms via gender='f' kwarg.
    from num2words2.lang_AR import Num2Word_AR
    ar = Num2Word_AR()
    assert ar.to_ordinal(1, gender="f") == "الأولى"
    assert ar.to_ordinal(2, gender="f") == "الثانية"
    assert ar.to_ordinal(11, gender="f") == "الحادية عشرة"
