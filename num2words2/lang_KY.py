# -*- coding: utf-8 -*-
# Licensed under LGPL v2.1 or later.

from __future__ import unicode_literals

from .base import Num2Word_Base


class Num2Word_KY(Num2Word_Base):
    """Kyrgyz number-to-words converter."""

    CURRENCY_FORMS = {
        "KGS": (("som", "som"), ("tıyın", "tıyın")),
        "USD": (("dollar", "dollar"), ("sent", "sent")),
        "EUR": (("evro", "evro"), ("sent", "sent")),
        "RUB": (("rubl", "rubl"), ("kopek", "kopek")),
    }

    def setup(self):
        self.negword = "minus "
        self.pointword = "üтүр"
        self.exclude_title = ["minus", "üтүр"]
        self.ones = [
            "", "bir", "eki", "üch", "tört", "besh",
            "alty", "jeti", "segiz", "toguz",
        ]
        self.tens = [
            "", "on", "jıyırma", "otuz", "kırk", "elüü",
            "altymysh", "jetimish", "seksen", "tokson",
        ]
        self.hundred = "jüz"
        self.thousand = "min"
        self.million = "million"

    def to_cardinal(self, number):
        n = str(number).strip()
        if n.startswith("-"):
            return (self.negword + self.to_cardinal(n[1:])).strip()
        if "." in n:
            left, right = n.split(".", 1)
            ret = self._int_to_word(int(left)) + " " + self.pointword
            for digit in right:
                ret += " " + (self.ones[int(digit)] or "nöl")
            return ret.strip()
        return self._int_to_word(int(n))

    def _int_to_word(self, number):
        if number == 0:
            return "nöl"
        if number < 10:
            return self.ones[number]
        if number < 100:
            t, o = divmod(number, 10)
            return self.tens[t] + (" " + self.ones[o] if o else "")
        if number < 1000:
            h, r = divmod(number, 100)
            base = (self.ones[h] + " " if h > 1 else "") + self.hundred
            return base + (" " + self._int_to_word(r) if r else "")
        if number < 1000000:
            t, r = divmod(number, 1000)
            base = (self._int_to_word(t) + " " if t > 1 else "") + self.thousand
            return base + (" " + self._int_to_word(r) if r else "")
        if number < 1000000000:
            m, r = divmod(number, 1000000)
            base = self._int_to_word(m) + " " + self.million
            return base + (" " + self._int_to_word(r) if r else "")
        return str(number)

    def to_ordinal(self, number):
        return self.to_cardinal(number) + "-inchi"

    def to_ordinal_num(self, number):
        return str(number) + "-inchi"

    def to_year(self, val, longval=True):
        return self.to_cardinal(val)

    def to_currency(self, val, currency="KGS", cents=True, separator=" ", adjective=False):
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
