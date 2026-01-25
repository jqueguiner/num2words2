# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import Num2Word_Base


class Num2Word_LO(Num2Word_Base):
    """Lao language number to words conversion."""

    CURRENCY_FORMS = {
        "LAK": (("ກີບ", "ກີບ"), ("ອັດ", "ອັດ")),
        "USD": (("ໂດລາ", "ໂດລາ"), ("ເຊັນ", "ເຊັນ")),
        "EUR": (("ເອີໂຣ", "ເອີໂຣ"), ("ເຊັນ", "ເຊັນ")),
    }

    def setup(self):
        self.negword = "ລົບ "
        self.pointword = "ຈຸດ"

        # Lao numbers 0-9
        self.ones = [
            "ສູນ",  # 0
            "ໜຶ່ງ",  # 1
            "ສອງ",  # 2
            "ສາມ",  # 3
            "ສີ່",  # 4
            "ຫ້າ",  # 5
            "ຫົກ",  # 6
            "ເຈັດ",  # 7
            "ແປດ",  # 8
            "ເກົ້າ",  # 9
        ]

    def to_cardinal(self, number):
        """Convert a number to its word representation in Lao."""
        n = str(number).strip()

        if n.startswith("-"):
            n = n[1:]
            ret = self.negword
        else:
            ret = ""

        if "." in n:
            left, right = n.split(".", 1)
            ret += self._int_to_word(int(left)) + " " + self.pointword + " "
            for digit in right:
                ret += self._int_to_word(int(digit)) + " "
            return ret.strip()
        else:
            return (ret + self._int_to_word(int(n))).strip()

    def _int_to_word(self, number):
        """Convert an integer to its word representation in Lao."""
        if number == 0:
            return self.ones[0]

        if number < 0:
            return self.negword + self._int_to_word(abs(number))
        elif number < 10:
            return self.ones[number]
        elif number == 10:
            return "ສິບ"
        elif number < 20:
            return "ສິບ" + self.ones[number - 10]
        elif number == 20:
            return "ຊາວ"
        elif number < 30:
            return "ຊາວ" + self.ones[number - 20]
        elif number < 100:
            tens_val = number // 10
            ones_val = number % 10
            tens_word = self.ones[tens_val] + "ສິບ"
            if ones_val == 0:
                return tens_word
            else:
                return tens_word + self.ones[ones_val]
        elif number < 1000:
            hundreds_val = number // 100
            remainder = number % 100
            result = self.ones[hundreds_val] + "ຮ້ອຍ"  # hundred
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 10000:
            thousands_val = number // 1000
            remainder = number % 1000
            result = self.ones[thousands_val] + "ພັນ"  # thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 100000:
            ten_thousands_val = number // 10000
            remainder = number % 10000
            result = self.ones[ten_thousands_val] + "ໝື່ນ"  # ten thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000:
            hundred_thousands_val = number // 100000
            remainder = number % 100000
            result = self.ones[hundred_thousands_val] + "ແສນ"  # hundred thousand
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        elif number < 1000000000:
            millions_val = number // 1000000
            remainder = number % 1000000
            result = self._int_to_word(millions_val) + " ລ້ານ"  # million
            if remainder:
                result += " " + self._int_to_word(remainder)
            return result
        else:
            return str(number)  # Fallback for very large numbers

    def to_ordinal(self, number):
        """Convert to ordinal in Lao."""
        cardinal = self.to_cardinal(number)
        return "ທີ່" + cardinal  # "ທີ່" is the ordinal prefix

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal."""
        return "ທີ່" + str(number)

    def to_year(self, val, longval=True):
        """Convert to year in Lao."""
        return "ປີ " + self.to_cardinal(val)

    def to_currency(
        self, val, currency="LAK", cents=True, separator=" ", adjective=False
    ):
        """Convert to currency in Lao."""
        is_negative = False
        if val < 0:
            is_negative = True
            val = abs(val)

        parts = str(val).split(".")
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0

        cr1, cr2 = self.CURRENCY_FORMS.get(currency, self.CURRENCY_FORMS["LAK"])

        left_str = self._int_to_word(left)
        result = left_str + " " + cr1[0]

        if cents and right:
            cents_str = self._int_to_word(right)
            result += separator + cents_str + " " + cr2[0]

        return (self.negword if is_negative else "") + result
