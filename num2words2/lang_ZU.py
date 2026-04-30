# -*- coding: utf-8 -*-
# Licensed under LGPL v2.1 or later.

from __future__ import unicode_literals

from .base import Num2Word_Base


class Num2Word_ZU(Num2Word_Base):
    """Zulu number-to-words converter."""

    CURRENCY_FORMS = {
        "ZAR": (("randi", "randi"), ("isenti", "isenti")),
        "USD": (("idola", "idola"), ("isenti", "isenti")),
        "EUR": (("iyuro", "iyuro"), ("isenti", "isenti")),
    }

    def setup(self):
        self.negword = "ngaphansi kwe "
        self.pointword = "ichashazi"
        self.exclude_title = ["na", "ichashazi", "ngaphansi", "kwe"]
        self.ones = [
            "", "kunye", "kubili", "kuthathu", "kune", "kuhlanu",
            "isithupha", "isikhombisa", "isishiyagalombili", "isishiyagalolunye",
        ]
        self.tens = [
            "", "ishumi", "amashumi amabili", "amashumi amathathu", "amashumi amane", "amashumi amahlanu",
            "amashumi ayisithupha", "amashumi ayisikhombisa", "amashumi ayisishiyagalombili", "amashumi ayisishiyagalolunye",
        ]
        self.hundred = "ikhulu"
        self.thousand = "inkulungwane"
        self.million = "isigidi"

    def to_cardinal(self, number):
        n = str(number).strip()
        if n.startswith("-"):
            return (self.negword + self.to_cardinal(n[1:])).strip()
        if "." in n:
            left, right = n.split(".", 1)
            ret = self._int_to_word(int(left)) + " " + self.pointword
            for digit in right:
                ret += " " + (self.ones[int(digit)] or "iqanda")
            return ret.strip()
        return self._int_to_word(int(n))

    def _int_to_word(self, number):
        if number == 0:
            return "iqanda"
        if number < 10:
            return self.ones[number]
        if number < 100:
            t, o = divmod(number, 10)
            return self.tens[t] + (" na " + self.ones[o] if o else "")
        if number < 1000:
            h, r = divmod(number, 100)
            base = (self.ones[h] + " " if h > 1 else "") + self.hundred
            return base + (" na " + self._int_to_word(r) if r else "")
        if number < 1000000:
            t, r = divmod(number, 1000)
            base = (self._int_to_word(t) + " " if t > 1 else "") + self.thousand
            return base + (" na " + self._int_to_word(r) if r else "")
        if number < 1000000000:
            m, r = divmod(number, 1000000)
            base = (self._int_to_word(m) + " " if m > 1 else "") + self.million
            return base + (" na " + self._int_to_word(r) if r else "")
        return str(number)

    def to_ordinal(self, number):
        if number == 1:
            return "okokuqala"
        return "we-" + self.to_cardinal(number)

    def to_ordinal_num(self, number):
        return "we-" + str(number)

    def to_year(self, val, longval=True):
        return self.to_cardinal(val)

    def to_currency(self, val, currency="ZAR", cents=True, separator=" ", adjective=False):
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
