# -*- coding: utf-8 -*-
# Licensed under LGPL v2.1 or later.

from __future__ import unicode_literals

from .base import Num2Word_Base


class Num2Word_LUS(Num2Word_Base):
    """Mizo number-to-words converter (also used for `miz` alias)."""

    CURRENCY_FORMS = {
        "INR": (("rupee", "rupee"), ("paisa", "paisa")),
        "USD": (("dollar", "dollar"), ("cent", "cent")),
        "EUR": (("euro", "euro"), ("cent", "cent")),
    }

    def setup(self):
        self.negword = "phak "
        self.pointword = "decimal"
        self.exclude_title = ["leh", "phak", "decimal"]
        self.ones = [
            "", "pakhat", "pahnih", "pathum", "pali", "panga",
            "paruk", "pasarih", "pariat", "pakua",
        ]
        self.tens = [
            "", "sawm", "sawmhnih", "sawmthum", "sawmli", "sawmnga",
            "sawmruk", "sawmsarih", "sawmriat", "sawmkua",
        ]
        self.hundred = "za"
        self.thousand = "sang"
        self.million = "nuai"

    def to_cardinal(self, number):
        n = str(number).strip()
        if n.startswith("-"):
            return (self.negword + self.to_cardinal(n[1:])).strip()
        if "." in n:
            left, right = n.split(".", 1)
            ret = self._int_to_word(int(left)) + " " + self.pointword
            for digit in right:
                ret += " " + (self.ones[int(digit)] or "a awmlo")
            return ret.strip()
        return self._int_to_word(int(n))

    def _int_to_word(self, number):
        if number == 0:
            return "a awmlo"
        if number < 10:
            return self.ones[number]
        if number < 100:
            t, o = divmod(number, 10)
            return self.tens[t] + (" leh " + self.ones[o] if o else "")
        if number < 1000:
            h, r = divmod(number, 100)
            base = self.ones[h] + " " + self.hundred
            return base + (" leh " + self._int_to_word(r) if r else "")
        if number < 1000000:
            t, r = divmod(number, 1000)
            base = self._int_to_word(t) + " " + self.thousand
            return base + (" " + self._int_to_word(r) if r else "")
        if number < 1000000000:
            m, r = divmod(number, 1000000)
            base = self._int_to_word(m) + " " + self.million
            return base + (" " + self._int_to_word(r) if r else "")
        return str(number)

    def to_ordinal(self, number):
        return self.to_cardinal(number) + "-na"

    def to_ordinal_num(self, number):
        return str(number) + "-na"

    def to_year(self, val, longval=True):
        return self.to_cardinal(val)

    def to_currency(self, val, currency="INR", cents=True, separator=" ", adjective=False):
        is_negative = val < 0
        val = abs(val)
        parts = str(val).split(".")
        left = int(parts[0]) if parts[0] else 0
        right = int(parts[1][:2].ljust(2, "0")) if len(parts) > 1 and parts[1] else 0
        cr1, cr2 = self.CURRENCY_FORMS.get(currency, list(self.CURRENCY_FORMS.values())[0])
        result = self._int_to_word(left) + " " + (cr1[1] if left != 1 else cr1[0])
        if cents and right:
            result += separator + self._int_to_word(right) + " " + (cr2[1] if right != 1 else cr2[0])
        if is_negative:
            result = self.negword + result
        return result.strip()

    def pluralize(self, n, forms):
        if not forms:
            return ""
        return forms[0] if n == 1 else forms[-1]
