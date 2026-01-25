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

from __future__ import unicode_literals

from unittest import TestCase

from num2words2 import num2words
from num2words2.lang_HE import Num2Word_HE, int2word


class Num2WordsHETest(TestCase):
    maxDiff = None

    def test_negative(self):
        self.assertEqual(num2words(-1, lang="he"), "מינוס אחת")

    def test_0(self):
        self.assertEqual(num2words(0, lang="he"), "אפס")

    def test_1_to_10(self):
        self.assertEqual(num2words(1, lang="he"), "אחת")
        self.assertEqual(num2words(2, lang="he"), "שתיים")
        self.assertEqual(num2words(7, lang="he"), "שבע")
        self.assertEqual(num2words(10, lang="he"), "עשר")
        self.assertEqual(num2words(10, lang="he", gender="m", construct=True), "עשרת")

    def test_11_to_19(self):
        self.assertEqual(num2words(11, lang="he"), "אחת עשרה")
        self.assertEqual(num2words(11, lang="he", gender="m"), "אחד עשר")
        self.assertEqual(num2words(13, lang="he"), "שלוש עשרה")
        self.assertEqual(num2words(13, lang="he", construct=True), "שלוש עשרה")
        self.assertEqual(num2words(15, lang="he"), "חמש עשרה")
        self.assertEqual(num2words(16, lang="he"), "שש עשרה")
        self.assertEqual(num2words(16, lang="he", gender="m"), "שישה עשר")
        self.assertEqual(
            num2words(16, lang="he", gender="m", construct=True), "שישה עשר"
        )
        self.assertEqual(num2words(19, lang="he"), "תשע עשרה")

    def test_20_to_99(self):
        self.assertEqual(num2words(20, lang="he"), "עשרים")
        self.assertEqual(num2words(23, lang="he"), "עשרים ושלוש")
        self.assertEqual(num2words(23, lang="he", gender="m"), "עשרים ושלושה")
        self.assertEqual(num2words(23, lang="he", construct=True), "עשרים ושלוש")
        self.assertEqual(
            num2words(23, lang="he", gender="m", construct=True), "עשרים ושלושה"
        )
        self.assertEqual(num2words(28, lang="he"), "עשרים ושמונה")
        self.assertEqual(num2words(31, lang="he"), "שלושים ואחת")
        self.assertEqual(num2words(40, lang="he"), "ארבעים")
        self.assertEqual(num2words(66, lang="he"), "שישים ושש")
        self.assertEqual(num2words(92, lang="he"), "תשעים ושתיים")

    def test_100_to_999(self):
        self.assertEqual(num2words(100, lang="he"), "מאה")
        self.assertEqual(num2words(100, lang="he", construct=True), "מאת")
        self.assertEqual(num2words(111, lang="he"), "מאה ואחת עשרה")
        self.assertEqual(num2words(111, lang="he", construct=True), "מאה ואחת עשרה")
        self.assertEqual(num2words(150, lang="he"), "מאה וחמישים")
        self.assertEqual(num2words(196, lang="he"), "מאה תשעים ושש")
        self.assertEqual(num2words(196, lang="he", gender="m"), "מאה תשעים ושישה")
        self.assertEqual(
            num2words(196, lang="he", gender="m", construct=True), "מאה תשעים ושישה"
        )
        self.assertEqual(num2words(200, lang="he"), "מאתיים")
        self.assertEqual(num2words(200, lang="he", construct=True), "מאתיים")
        self.assertEqual(num2words(210, lang="he"), "מאתיים ועשר")
        self.assertEqual(num2words(701, lang="he"), "שבע מאות ואחת")

    def test_1000_to_9999(self):
        self.assertEqual(num2words(1000, lang="he"), "אלף")
        self.assertEqual(num2words(1000, lang="he", construct=True), "אלף")
        self.assertEqual(num2words(1001, lang="he"), "אלף ואחת")
        self.assertEqual(num2words(1002, lang="he"), "אלף ושתיים")
        self.assertEqual(num2words(1002, lang="he", gender="m"), "אלף ושניים")
        self.assertEqual(
            num2words(1002, lang="he", gender="m", construct=True), "אלף ושניים"
        )
        self.assertEqual(num2words(1003, lang="he"), "אלף ושלוש")
        self.assertEqual(num2words(1003, lang="he", gender="m"), "אלף ושלושה")
        self.assertEqual(
            num2words(1003, lang="he", gender="m", construct=True), "אלף ושלושה"
        )
        self.assertEqual(num2words(1010, lang="he"), "אלף ועשר")
        self.assertEqual(num2words(1010, lang="he", gender="m"), "אלף ועשרה")
        self.assertEqual(
            num2words(1010, lang="he", gender="m", construct=True), "אלף ועשרה"
        )
        self.assertEqual(num2words(1500, lang="he"), "אלף וחמש מאות")
        self.assertEqual(num2words(2000, lang="he"), "אלפיים")
        self.assertEqual(num2words(2000, lang="he", construct=True), "אלפיים")
        self.assertEqual(num2words(2002, lang="he"), "אלפיים ושתיים")
        self.assertEqual(num2words(2002, lang="he", construct=True), "אלפיים ושתיים")
        self.assertEqual(num2words(3000, lang="he"), "שלושת אלפים")
        self.assertEqual(num2words(3000, lang="he", construct=True), "שלושת אלפי")
        self.assertEqual(num2words(3001, lang="he"), "שלושת אלפים ואחת")
        self.assertEqual(num2words(3001, lang="he", construct=True), "שלושת אלפים ואחת")
        self.assertEqual(num2words(3100, lang="he"), "שלושת אלפים ומאה")
        self.assertEqual(num2words(3100, lang="he", construct=True), "שלושת אלפים ומאה")
        self.assertEqual(num2words(6870, lang="he"), "ששת אלפים שמונה מאות ושבעים")
        self.assertEqual(
            num2words(7378, lang="he"), "שבעת אלפים שלוש מאות שבעים ושמונה"
        )
        self.assertEqual(num2words(9999, lang="he"), "תשעת אלפים תשע מאות תשעים ותשע")

    def test_10000_to_99999(self):
        self.assertEqual(num2words(10000, lang="he"), "עשרת אלפים")
        self.assertEqual(num2words(10000, lang="he", construct=True), "עשרת אלפי")
        self.assertEqual(num2words(10001, lang="he"), "עשרת אלפים ואחת")
        self.assertEqual(num2words(10001, lang="he", construct=True), "עשרת אלפים ואחת")
        self.assertEqual(num2words(10999, lang="he"), "עשרת אלפים תשע מאות תשעים ותשע")
        self.assertEqual(num2words(11000, lang="he"), "אחד עשר אלף")
        self.assertEqual(num2words(15000, lang="he"), "חמישה עשר אלף")
        self.assertEqual(num2words(15000, lang="he", gender="m"), "חמישה עשר אלף")
        self.assertEqual(num2words(20000, lang="he"), "עשרים אלף")
        self.assertEqual(num2words(20000, lang="he", construct=True), "עשרים אלף")
        self.assertEqual(num2words(21000, lang="he"), "עשרים ואחד אלף")
        self.assertEqual(num2words(25000, lang="he"), "עשרים וחמישה אלף")
        self.assertEqual(
            num2words(25000, lang="he", construct=True), "עשרים וחמישה אלף"
        )
        self.assertEqual(num2words(68700, lang="he"), "שישים ושמונה אלף ושבע מאות")
        self.assertEqual(
            num2words(73781, lang="he"), "שבעים ושלושה אלף שבע מאות שמונים ואחת"
        )
        self.assertEqual(
            num2words(99999, lang="he"), "תשעים ותשעה אלף תשע מאות תשעים ותשע"
        )

    def test_100000_to_999999(self):
        self.assertEqual(num2words(100000, lang="he"), "מאה אלף")
        self.assertEqual(num2words(100000, lang="he", construct=True), "מאה אלף")
        self.assertEqual(num2words(100001, lang="he"), "מאה אלף ואחת")
        self.assertEqual(
            num2words(199999, lang="he"), "מאה תשעים ותשעה אלף תשע מאות תשעים ותשע"
        )
        self.assertEqual(num2words(110000, lang="he"), "מאה ועשרה אלף")
        self.assertEqual(num2words(150000, lang="he"), "מאה וחמישים אלף")
        self.assertEqual(num2words(200000, lang="he"), "מאתיים אלף")
        self.assertEqual(num2words(210000, lang="he"), "מאתיים ועשרה אלף")
        self.assertEqual(num2words(687000, lang="he"), "שש מאות שמונים ושבעה אלף")
        self.assertEqual(
            num2words(687000, lang="he", construct=True), "שש מאות שמונים ושבעה אלף"
        )
        self.assertEqual(
            num2words(737812, lang="he"),
            "שבע מאות שלושים ושבעה אלף שמונה מאות ושתים עשרה",
        )
        self.assertEqual(
            num2words(999999, lang="he"), "תשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשע"
        )

    def test_1000000_to_999999999999999(self):
        self.assertEqual(num2words(1000000, lang="he"), "מיליון")
        self.assertEqual(num2words(1000000, lang="he", construct=True), "מיליון")
        self.assertEqual(num2words(1000002, lang="he"), "מיליון ושתיים")
        self.assertEqual(num2words(1000002, lang="he", construct=True), "מיליון ושתיים")
        self.assertEqual(num2words(2000000, lang="he"), "שני מיליון")
        self.assertEqual(num2words(2000000, lang="he", construct=True), "שני מיליוני")
        self.assertEqual(num2words(3000000, lang="he"), "שלושה מיליון")
        self.assertEqual(num2words(3000000, lang="he", construct=True), "שלושת מיליוני")
        self.assertEqual(num2words(3000002, lang="he"), "שלושה מיליון ושתיים")
        self.assertEqual(
            num2words(3000002, lang="he", construct=True), "שלושה מיליון ושתיים"
        )
        self.assertEqual(num2words(10000000, lang="he"), "עשרה מיליון")
        self.assertEqual(num2words(10000000, lang="he", construct=True), "עשרת מיליוני")
        self.assertEqual(num2words(11000000, lang="he"), "אחד עשר מיליון")
        self.assertEqual(
            num2words(11000000, lang="he", construct=True), "אחד עשר מיליוני"
        )

        self.assertEqual(num2words(1000000000, lang="he"), "מיליארד")
        self.assertEqual(num2words(1000000000, lang="he", construct=True), "מיליארד")
        self.assertEqual(num2words(1000000002, lang="he"), "מיליארד ושתיים")
        self.assertEqual(
            num2words(1000000002, lang="he", construct=True), "מיליארד ושתיים"
        )
        self.assertEqual(num2words(2000000000, lang="he"), "שני מיליארד")
        self.assertEqual(
            num2words(2000000000, lang="he", construct=True), "שני מיליארדי"
        )
        self.assertEqual(num2words(3000000000, lang="he"), "שלושה מיליארד")
        self.assertEqual(
            num2words(3000000000, lang="he", construct=True), "שלושת מיליארדי"
        )
        self.assertEqual(num2words(3000000002, lang="he"), "שלושה מיליארד ושתיים")
        self.assertEqual(
            num2words(3000000002, lang="he", construct=True), "שלושה מיליארד ושתיים"
        )
        self.assertEqual(num2words(10000000000, lang="he"), "עשרה מיליארד")
        self.assertEqual(
            num2words(10000000000, lang="he", construct=True), "עשרת מיליארדי"
        )
        self.assertEqual(num2words(10000000002, lang="he"), "עשרה מיליארד ושתיים")
        self.assertEqual(
            num2words(10000000002, lang="he", construct=True), "עשרה מיליארד ושתיים"
        )
        self.assertEqual(num2words(11000000000, lang="he"), "אחד עשר מיליארד")
        self.assertEqual(
            num2words(11000000000, lang="he", construct=True), "אחד עשר מיליארדי"
        )

        self.assertEqual(num2words(1000000000000, lang="he"), "טריליון")
        self.assertEqual(num2words(1000000000000, lang="he", construct=True), "טריליון")
        self.assertEqual(num2words(1000000000002, lang="he"), "טריליון ושתיים")
        self.assertEqual(
            num2words(1000000000002, lang="he", construct=True), "טריליון ושתיים"
        )
        self.assertEqual(num2words(2000000000000, lang="he"), "שני טריליון")
        self.assertEqual(
            num2words(2000000000000, lang="he", construct=True), "שני טריליוני"
        )
        self.assertEqual(num2words(3000000000000, lang="he"), "שלושה טריליון")
        self.assertEqual(
            num2words(3000000000000, lang="he", construct=True), "שלושת טריליוני"
        )
        self.assertEqual(num2words(3000000000002, lang="he"), "שלושה טריליון ושתיים")
        self.assertEqual(
            num2words(3000000000002, lang="he", construct=True), "שלושה טריליון ושתיים"
        )
        self.assertEqual(num2words(10000000000000, lang="he"), "עשרה טריליון")
        self.assertEqual(
            num2words(10000000000000, lang="he", construct=True), "עשרת טריליוני"
        )
        self.assertEqual(num2words(10000000000002, lang="he"), "עשרה טריליון ושתיים")
        self.assertEqual(
            num2words(10000000000002, lang="he", construct=True), "עשרה טריליון ושתיים"
        )
        self.assertEqual(num2words(11000000000000, lang="he"), "אחד עשר טריליון")
        self.assertEqual(
            num2words(11000000000000, lang="he", construct=True), "אחד עשר טריליוני"
        )

        self.assertEqual(
            num2words(999999999999999, lang="he"),
            "תשע מאות תשעים ותשעה טריליון "
            "תשע מאות תשעים ותשעה מיליארד "
            "תשע מאות תשעים ותשעה מיליון "
            "תשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשע",
        )
        self.assertEqual(
            num2words(999999999999999, lang="he", gender="m"),
            "תשע מאות תשעים ותשעה טריליון "
            "תשע מאות תשעים ותשעה מיליארד "
            "תשע מאות תשעים ותשעה מיליון "
            "תשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשעה",
        )
        self.assertEqual(
            num2words(999999999999999, lang="he", construct=True),
            "תשע מאות תשעים ותשעה טריליון "
            "תשע מאות תשעים ותשעה מיליארד "
            "תשע מאות תשעים ותשעה מיליון "
            "תשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשע",
        )
        self.assertEqual(
            num2words(999999999999999, lang="he", gender="m", construct=True),
            "תשע מאות תשעים ותשעה טריליון "
            "תשע מאות תשעים ותשעה מיליארד "
            "תשע מאות תשעים ותשעה מיליון "
            "תשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשעה",
        )

    def test_pluralize(self):
        n = Num2Word_HE()
        cr1, cr2 = n.CURRENCY_FORMS["ILS"]
        self.assertEqual(n.pluralize(1, cr1), "שקל")
        self.assertEqual(n.pluralize(2, cr1), "שקלים")
        self.assertEqual(n.pluralize(1, cr2), "אגורה")
        self.assertEqual(n.pluralize(2, cr2), "אגורות")

        cr1, cr2 = n.CURRENCY_FORMS["USD"]
        self.assertEqual(n.pluralize(1, cr1), "דולר")
        self.assertEqual(n.pluralize(2, cr1), "דולרים")
        self.assertEqual(n.pluralize(1, cr2), "סנט")
        self.assertEqual(n.pluralize(2, cr2), "סנטים")

    def test_to_currency(self):
        n = Num2Word_HE()
        self.assertEqual(n.to_currency(20, currency="ILS"), "עשרים שקליםו")
        self.assertEqual(n.to_currency(100, currency="ILS"), "מאה שקליםו")
        self.assertEqual(
            n.to_currency(100.50, currency="ILS"), "מאה שקליםו חמישים אגורות"
        )
        self.assertEqual(
            n.to_currency(101.51, currency="ILS"), "מאה ואחת שקליםו חמישים ואחת אגורות"
        )
        self.assertEqual(
            n.to_currency(-101.51, currency="ILS"),
            "מינוס מאה ואחת שקליםו חמישים ואחת אגורות",
        )
        self.assertEqual(
            n.to_currency(-101.51, currency="ILS", prefer_singular=True),
            "מינוס מאה ואחת שקליםו חמישים ואחת אגורות",
        )
        self.assertEqual(
            n.to_currency(-101.51, currency="ILS", prefer_singular_cents=True),
            "מינוס מאה ואחת שקליםו חמישים ואחת אגורות",
        )
        self.assertEqual(
            n.to_currency(
                -101.51,
                currency="ILS",
                prefer_singular=True,
                prefer_singular_cents=True,
            ),
            "מינוס מאה ואחת שקליםו חמישים ואחת אגורות",
        )
        self.assertEqual(
            n.to_currency(
                5.05, currency="ILS", prefer_singular=True, prefer_singular_cents=True
            ),
            "חמש שקליםו חמש אגורות",
        )
        self.assertEqual(
            n.to_currency(
                -5.05, currency="ILS", prefer_singular=True, prefer_singular_cents=True
            ),
            "מינוס חמש שקליםו חמש אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False),
            "מינוס חמש שקליםו 05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator="ו"),
            "מינוס חמש שקליםו 05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator="ו-"),
            "מינוס חמש שקליםו- 05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator=""),
            "מינוס חמש שקלים 05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator="ועוד "),
            "מינוס חמש שקליםועוד  05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator=" ו"),
            "מינוס חמש שקלים ו 05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator=" ו-"),
            "מינוס חמש שקלים ו- 05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator=" "),
            "מינוס חמש שקלים  05 אגורות",
        )
        self.assertEqual(
            n.to_currency(-5.05, currency="ILS", cents=False, separator=" ועוד "),
            "מינוס חמש שקלים ועוד  05 אגורות",
        )
        self.assertEqual(n.to_currency(1.01, currency="ILS"), "אחת שקלו אחת אגורה")
        self.assertEqual(
            n.to_currency(-1.01, currency="ILS"), "מינוס אחת שקלו אחת אגורה"
        )
        self.assertEqual(
            n.to_currency(2.02, currency="ILS"), "שתיים שקליםו שתיים אגורות"
        )
        self.assertEqual(
            n.to_currency(1002.02, currency="ILS"), "אלף ושתיים שקליםו שתיים אגורות"
        )
        self.assertEqual(
            n.to_currency(1000002.02, currency="ILS"),
            "מיליון ושתיים שקליםו שתיים אגורות",
        )
        self.assertEqual(n.to_currency(5.05, currency="USD"), "חמש דולריםו חמש סנטים")
        self.assertEqual(
            n.to_currency(5.05, currency="USD", prefer_singular=True),
            "חמש דולריםו חמש סנטים",
        )
        self.assertEqual(
            n.to_currency(5.05, currency="USD", prefer_singular_cents=True),
            "חמש דולריםו חמש סנטים",
        )
        self.assertEqual(
            n.to_currency(
                5.05, currency="USD", prefer_singular=True, prefer_singular_cents=True
            ),
            "חמש דולריםו חמש סנטים",
        )
        n.CURRENCY_FORMS["pruta"] = (("פרוטה", "פרוטות"), ("מאית", "מאיות"))
        self.assertEqual(n.to_currency(5.05, currency="pruta"), "חמש פרוטותו חמש מאיות")

    def test_to_currency_errors(self):
        n = Num2Word_HE()
        with self.assertRaises(NotImplementedError):
            n.to_currency(1, "")

    def test_to_cardinal(self):
        n = Num2Word_HE()
        self.assertEqual(n.to_cardinal(1500), "אלף וחמש מאות")
        self.assertEqual(n.to_cardinal(1501), "אלף חמש מאות ואחת")
        self.assertEqual(num2words(1, lang="he"), "אחת")
        self.assertEqual(num2words(1, lang="he", gender="m"), "אחד")

    def test_to_ordinal(self):
        n = Num2Word_HE()
        self.assertEqual(n.to_ordinal(1001), "האלף ואחד")
        self.assertEqual(n.to_ordinal(1500), "האלף וחמש מאות")
        self.assertEqual(n.to_ordinal(1501), "האלף חמש מאות ואחד")
        self.assertEqual(n.to_ordinal(1501, definite=True), "האלף חמש מאות ואחד")
        self.assertEqual(n.to_ordinal(1), "ראשון")
        self.assertEqual(n.to_ordinal(1, definite=True), "הראשון")
        self.assertEqual(n.to_ordinal(1, gender="f"), "ראשונה")
        self.assertEqual(n.to_ordinal(1, gender="f", definite=True), "הראשונה")
        self.assertEqual(n.to_ordinal(10), "עשירי")
        self.assertEqual(n.to_ordinal(10, definite=True), "העשירי")
        self.assertEqual(n.to_ordinal(10, gender="f"), "עשירית")
        self.assertEqual(n.to_ordinal(10, gender="f", definite=True), "העשירית")
        self.assertEqual(n.to_ordinal(17), "השבעה עשר")
        self.assertEqual(n.to_ordinal(17, definite=True), "השבעה עשר")
        self.assertEqual(n.to_ordinal(17, gender="f"), "השבע עשרה")
        self.assertEqual(n.to_ordinal(17, gender="f", definite=True), "השבע עשרה")
        self.assertEqual(n.to_ordinal(0), "האפס")
        self.assertEqual(n.to_ordinal(0, definite=True), "האפס")
        self.assertEqual(n.to_ordinal(0, gender="f"), "האפס")
        self.assertEqual(n.to_ordinal(0, gender="f", definite=True), "האפס")
        self.assertEqual(
            n.to_ordinal(999999), "התשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשעה"
        )
        self.assertEqual(
            n.to_ordinal(999999, gender="f"),
            "התשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשע",
        )
        self.assertEqual(num2words(1, ordinal=True, lang="he"), "ראשון")
        self.assertEqual(num2words(1, ordinal=True, lang="he", gender="f"), "ראשונה")
        self.assertEqual(num2words(1, ordinal=True, lang="he", definite=True), "הראשון")
        self.assertEqual(
            num2words(1, ordinal=True, lang="he", gender="f", definite=True), "הראשונה"
        )

    def test_to_ordinal_plural(self):
        n = Num2Word_HE()
        self.assertEqual(n.to_ordinal(1001, plural=True), "האלף ואחד")
        self.assertEqual(n.to_ordinal(1500, plural=True), "האלף וחמש מאות")
        self.assertEqual(n.to_ordinal(1501, plural=True), "האלף חמש מאות ואחד")
        self.assertEqual(
            n.to_ordinal(1501, definite=True, plural=True), "האלף חמש מאות ואחד"
        )
        self.assertEqual(n.to_ordinal(1, plural=True), "ראשונים")
        self.assertEqual(n.to_ordinal(1, definite=True, plural=True), "הראשונים")
        self.assertEqual(n.to_ordinal(1, gender="f", plural=True), "ראשונות")
        self.assertEqual(
            n.to_ordinal(1, gender="f", definite=True, plural=True), "הראשונות"
        )
        self.assertEqual(n.to_ordinal(10, plural=True), "עשיריים")
        self.assertEqual(n.to_ordinal(10, definite=True, plural=True), "העשיריים")
        self.assertEqual(n.to_ordinal(10, gender="f", plural=True), "עשיריות")
        self.assertEqual(
            n.to_ordinal(10, gender="f", definite=True, plural=True), "העשיריות"
        )
        self.assertEqual(n.to_ordinal(17, plural=True), "השבעה עשר")
        self.assertEqual(n.to_ordinal(17, definite=True, plural=True), "השבעה עשר")
        self.assertEqual(n.to_ordinal(17, gender="f", plural=True), "השבע עשרה")
        self.assertEqual(
            n.to_ordinal(17, gender="f", definite=True, plural=True), "השבע עשרה"
        )
        self.assertEqual(n.to_ordinal(0, plural=True), "האפס")
        self.assertEqual(n.to_ordinal(0, definite=True, plural=True), "האפס")
        self.assertEqual(n.to_ordinal(0, gender="f", plural=True), "האפס")
        self.assertEqual(
            n.to_ordinal(0, gender="f", definite=True, plural=True), "האפס"
        )
        self.assertEqual(
            n.to_ordinal(999999, plural=True),
            "התשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשעה",
        )
        self.assertEqual(
            n.to_ordinal(999999, gender="f", plural=True),
            "התשע מאות תשעים ותשעה אלף תשע מאות תשעים ותשע",
        )
        self.assertEqual(num2words(1, ordinal=True, lang="he", plural=True), "ראשונים")
        self.assertEqual(
            num2words(1, ordinal=True, lang="he", gender="f", plural=True), "ראשונות"
        )
        self.assertEqual(
            num2words(1, ordinal=True, lang="he", definite=True, plural=True),
            "הראשונים",
        )
        self.assertEqual(
            num2words(
                1, ordinal=True, lang="he", gender="f", definite=True, plural=True
            ),
            "הראשונות",
        )

    def test_cardinal_for_float_number(self):
        self.assertEqual(num2words(12.5, lang="he"), "שתים עשרה נקודה חמש")
        self.assertEqual(num2words(12.51, lang="he"), "שתים עשרה נקודה חמש אחת")
        self.assertEqual(num2words(12.53, lang="he"), "שתים עשרה נקודה חמש שלוש")
        self.assertEqual(num2words(12.59, lang="he"), "שתים עשרה נקודה חמש תשע")
        self.assertEqual(num2words(12.5, lang="he", gender="m"), "שנים עשר נקודה חמש")
        self.assertEqual(
            num2words(12.51, lang="he", gender="m"), "שנים עשר נקודה חמש אחת"
        )
        self.assertEqual(
            num2words(12.53, lang="he", gender="m"), "שנים עשר נקודה חמש שלוש"
        )
        self.assertEqual(
            num2words(12.59, lang="he", gender="m"), "שנים עשר נקודה חמש תשע"
        )
        self.assertEqual(
            num2words(12.594132, lang="he", gender="m"),
            "שנים עשר נקודה חמש תשע ארבע אחת שלוש שתיים",
        )

    def test_cardinal_float_precision(self):
        n = Num2Word_HE()
        self.assertEqual(n.to_cardinal_float("1.23"), "אחת נקודה שתיים שלוש")
        n.precision = 1
        self.assertEqual(n.to_cardinal_float("1.2"), "אחת נקודה שתיים")

    def test_error_to_cardinal_float(self):
        n = Num2Word_HE()
        with self.assertRaises(TypeError):
            n.to_cardinal_float("a")

    def test_overflow(self):
        n = Num2Word_HE()
        num2words(n.MAXVAL - 1, lang="he")
        num2words(n.MAXVAL - 1, ordinal=True, lang="he")

        with self.assertRaises(OverflowError):
            num2words(n.MAXVAL, lang="he")

        with self.assertRaises(OverflowError):
            num2words(n.MAXVAL, lang="he", ordinal=True)

        with self.assertRaises(OverflowError):
            int2word(n.MAXVAL)

    def test_negative_decimals(self):
        # Comprehensive test for negative decimals including -0.4
        self.assertEqual(num2words(-0.4, lang="he"), "מינוס אפס נקודה ארבע")
        self.assertEqual(num2words(-0.5, lang="he"), "מינוס אפס נקודה חמש")
        self.assertEqual(num2words(-1.4, lang="he"), "מינוס אחת נקודה ארבע")
