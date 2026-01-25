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


from __future__ import print_function, unicode_literals

from .base import Num2Word_Base
from .compat import to_s
from .utils import get_digits, splitbyx

ZERO = ("אפס",)

ONES = {
    1: ("אחת", "אחד", "אחת", "אחד", "ראשונה", "ראשון", "ראשונות", "ראשונים"),
    2: ("שתיים", "שניים", "שתי", "שני", "שנייה", "שני", "שניות", "שניים"),
    3: ("שלוש", "שלושה", "שלוש", "שלושת", "שלישית", "שלישי", "שלישיות", "שלישיים"),
    4: ("ארבע", "ארבעה", "ארבע", "ארבעת", "רביעית", "רביעי", "רביעיות", "רביעיים"),
    5: ("חמש", "חמישה", "חמש", "חמשת", "חמישית", "חמישי", "חמישיות", "חמישיים"),
    6: ("שש", "שישה", "שש", "ששת", "שישית", "שישי", "שישיות", "שישיים"),
    7: ("שבע", "שבעה", "שבע", "שבעת", "שביעית", "שביעי", "שביעיות", "שביעיים"),
    8: ("שמונה", "שמונה", "שמונה", "שמונת", "שמינית", "שמיני", "שמיניות", "שמיניים"),
    9: ("תשע", "תשעה", "תשע", "תשעת", "תשיעית", "תשיעי", "תשיעיות", "תשיעיים"),
}

TENS = {
    0: ("עשר", "עשרה", "עשר", "עשרת", "עשירית", "עשירי", "עשיריות", "עשיריים"),
    1: ("עשרה", "עשר"),
    2: ("שתים עשרה", "שנים עשר"),
}

TWENTIES = {
    2: ("עשרים",),
    3: ("שלושים",),
    4: ("ארבעים",),
    5: ("חמישים",),
    6: ("שישים",),
    7: ("שבעים",),
    8: ("שמונים",),
    9: ("תשעים",),
}

HUNDREDS = {1: ("מאה", "מאת"), 2: ("מאתיים",), 3: ("מאות",)}

THOUSANDS = {
    1: ("אלף",),
    2: ("אלפיים",),
    3: ("אלפים", "אלפי"),
}

LARGE = {
    1: ("מיליון", "מיליוני"),
    2: ("מיליארד", "מיליארדי"),
    3: ("טריליון", "טריליוני"),
    4: ("קוודריליון", "קוודריליוני"),
    5: ("קווינטיליון", "קווינטיליוני"),
    6: ("סקסטיליון", "סקסטיליוני"),
    7: ("ספטיליון", "ספטיליוני"),
    8: ("אוקטיליון", "אוקטיליוני"),
    9: ("נוניליון", "נוניליוני"),
    10: ("דסיליון", "דסיליוני"),
    11: ("אונדסיליון", "אונדסיליוני"),
    12: ("דואודסיליון", "דואודסיליוני"),
    13: ("טרדסיליון", "טרדסיליוני"),
    14: ("קווטואורדסיליון", "קווטואורדסיליוני"),
    15: ("קווינדסיליון", "קווינדסיליוני"),
    16: ("סקסדסיליון", "סקסדסיליוני"),
    17: ("ספטנדסיליון", "ספטנדסיליוני"),
    18: ("אוקטודסיליון", "אוקטודסיליוני"),
    19: ("נובמדסיליון", "נובמדסיליוני"),
    20: ("ויגינטיליון", "ויגינטיליוני"),
}

AND = "ו"

DEF = "ה"

MAXVAL = int("1" + "0" * 66)


def chunk2word(n, i, x, gender="f", construct=False, ordinal=False, plural=False):
    words = []
    n1, n2, n3 = get_digits(x)

    if n3 > 0:
        if construct and n == 100:
            words.append(HUNDREDS[n3][1])
        elif n3 <= 2:
            words.append(HUNDREDS[n3][0])
        else:
            words.append(ONES[n3][0] + " " + HUNDREDS[3][0])

    if n2 > 1:
        words.append(TWENTIES[n2][0])

    if i == 0 or x >= 11:
        male = gender == "m" or i > 0
        cop = (2 * (construct and i == 0) + 4 * ordinal + 2 * plural) * (n < 11)
        if n2 == 1:
            if n1 == 0:
                words.append(TENS[n1][male + cop])
            elif n1 == 2:
                words.append(TENS[n1][male])
            else:
                words.append(ONES[n1][male] + " " + TENS[1][male])
        elif n1 > 0:
            words.append(ONES[n1][male + cop])

    construct_last = construct and (n % 1000**i == 0)

    if i == 1:
        if x >= 11:
            words[-1] = words[-1] + " " + THOUSANDS[1][0]
        elif n1 == 0:
            words.append(TENS[0][3] + " " + THOUSANDS[3][construct_last])
        elif n1 <= 2:
            words.append(THOUSANDS[n1][0])
        else:
            words.append(ONES[n1][3] + " " + THOUSANDS[3][construct_last])

    elif i > 1:
        if x >= 11:
            words[-1] = words[-1] + " " + LARGE[i - 1][construct_last]
        elif n1 == 0:
            words.append(
                TENS[0][1 + 2 * construct_last] + " " + LARGE[i - 1][construct_last]
            )
        elif n1 == 1:
            words.append(LARGE[i - 1][0])
        else:
            words.append(
                ONES[n1][1 + 2 * (construct_last or x == 2)]
                + " "
                + LARGE[i - 1][construct_last]
            )

    return words


def int2word(
    n, gender="f", construct=False, ordinal=False, definite=False, plural=False
):
    assert n == int(n)
    assert not construct or not ordinal
    assert ordinal or (not definite and not plural)
    if n >= MAXVAL:
        raise OverflowError("abs(%s) must be less than %s." % (n, MAXVAL))

    if n == 0:
        if ordinal:
            return DEF + ZERO[0]
        return ZERO[0]

    words = []

    chunks = list(splitbyx(str(n), 3))
    i = len(chunks)
    for x in chunks:
        i -= 1

        if x == 0:
            continue

        words += chunk2word(
            n, i, x, gender=gender, construct=construct, ordinal=ordinal, plural=plural
        )

        # https://hebrew-academy.org.il/2017/01/30/%D7%95-%D7%94%D7%97%D7%99%D7%91%D7%95%D7%A8-%D7%91%D7%9E%D7%A1%D7%A4%D7%A8%D7%99%D7%9D  # noqa
        if len(words) > 1:
            words[-1] = AND + words[-1]

    if ordinal and (n >= 11 or definite):
        words[0] = DEF + words[0]

    return " ".join(words)


class Num2Word_HE(Num2Word_Base):
    CURRENCY_FORMS = {
        "ILS": (("שקל", "שקלים"), ("אגורה", "אגורות")),
        "EUR": (("אירו", "אירו"), ("סנט", "סנטים")),
        "USD": (("דולר", "דולרים"), ("סנט", "סנטים")),
    }

    CURRENCY_GENDERS = {
        "ILS": ("m", "f"),
        "EUR": ("m", "m"),
        "USD": ("m", "m"),
    }

    def __init__(self, makaf="-"):
        super(Num2Word_HE, self).__init__()
        self.makaf = makaf

    def setup(self):
        super(Num2Word_HE, self).setup()
        self.negword = "מינוס"
        self.pointword = "נקודה"
        self.MAXVAL = MAXVAL

    def to_cardinal_float(self, value, gender="f"):
        try:
            float(value) == value
        except (ValueError, TypeError, AssertionError, AttributeError):
            raise TypeError(self.errmsg_nonnum % value)

        float_value = float(value)
        pre, post = self.float2tuple(float_value)

        post = str(post)
        post = "0" * (self.precision - len(post)) + post

        out = [self.to_cardinal(pre, gender=gender)]
        # Handle negative decimals when integer part is 0
        if float_value < 0 and pre == 0:
            out = [self.negword.strip()] + out

        if self.precision:
            out.append(self.title(self.pointword))

        for i in range(self.precision):
            curr = int(post[i])
            out.append(to_s(self.to_cardinal(curr)))

        return " ".join(out)

    def to_cardinal(self, value, gender="f", construct=False):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            # https://hebrew-academy.org.il/2019/12/03/%D7%A2%D7%9C-%D7%94%D7%91%D7%A2%D7%AA-%D7%94%D7%9E%D7%A1%D7%A4%D7%A8-%D7%94%D7%9E%D7%A2%D7%95%D7%A8%D7%91  # noqa
            return self.to_cardinal_float(value, gender=gender)

        out = ""
        if value < 0:
            value = abs(value)
            out = "%s " % self.negword.strip()

        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        return out + int2word(int(value), gender=gender, construct=construct)

    def to_ordinal(self, value, gender="m", definite=False, plural=False):
        self.verify_ordinal(value)

        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        return int2word(
            int(value), gender=gender, ordinal=True, definite=definite, plural=plural
        )

    def pluralize(self, n, forms, currency=None, prefer_singular=False):
        assert n == int(n)
        form = 1
        if n == 1 or prefer_singular and (abs(n) >= 11 or n == 0 or currency != "ILS"):
            form = 0
        return forms[form]

    def to_currency(
        self,
        val,
        currency="ILS",
        cents=True,
        separator=AND,
        adjective=False,
        prefer_singular=False,
        prefer_singular_cents=False,
    ):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            # Get the result as if it were a float
            result = super().to_currency(
                float(val),
                currency=currency,
                cents=cents,
                separator=separator,
                adjective=adjective,
            )
            # Remove zero cents patterns
            zero_patterns = [
                "zero cent",
                "nul cent",
                "null cent",
                "sıfır kuruş",
                "אפס אגורות",
                "zero sen",
                "ศูนย์สตางค์",
                "không xu",
                "शून्य पैसे",
                "শূন্য পয়সা",
                "nula lipa",
                "нула пара",
                "ноль копеек",
                "нула стотинки",
                "零分",
                "ዜሮ ሳንቲም",
                "صفر",
                "sero sent",
                "dim ceiniog",
                "ნულოვანი თეთრი",
                "нула стотинки",
            ]
            import re

            for pattern in zero_patterns:
                if pattern in result.lower():
                    # Remove the pattern and any connecting words
                    result = re.sub(
                        r"\s+(and|və|և|და|ir|და|და|و|و|与|ja|और|এবং|i|и|и|と|그리고|และ|và|dan|a|e|და)\s+"
                        + re.escape(pattern),
                        "",
                        result,
                        flags=re.IGNORECASE,
                    )
                    result = re.sub(re.escape(pattern), "", result, flags=re.IGNORECASE)
                    result = " ".join(result.split())  # Clean up extra spaces
            return result.strip()

        # For floats, call parent implementation
        return super().to_currency(
            val,
            currency=currency,
            cents=cents,
            separator=separator,
            adjective=adjective,
        )
