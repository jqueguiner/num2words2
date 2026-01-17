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

TEST_CASES_CARDINAL = (
    (0, 'μηδέν'),
    (1, 'ένα'),
    (2, 'δύο'),
    (3, 'τρία'),
    (4, 'τέσσερα'),
    (5, 'πέντε'),
    (6, 'έξι'),
    (7, 'επτά'),
    (8, 'οκτώ'),
    (9, 'εννέα'),
    (10, 'δέκα'),
    (11, 'έντεκα'),
    (12, 'δώδεκα'),
    (13, 'δεκατρία'),
    (14, 'δεκατέσσερα'),
    (15, 'δεκαπέντε'),
    (16, 'δεκαέξι'),
    (17, 'δεκαεπτά'),
    (18, 'δεκαοκτώ'),
    (19, 'δεκαεννέα'),
    (20, 'είκοσι'),
    (21, 'είκοσι ένα'),
    (22, 'είκοσι δύο'),
    (25, 'είκοσι πέντε'),
    (30, 'τριάντα'),
    (31, 'τριάντα ένα'),
    (35, 'τριάντα πέντε'),
    (40, 'σαράντα'),
    (44, 'σαράντα τέσσερα'),
    (50, 'πενήντα'),
    (55, 'πενήντα πέντε'),
    (60, 'εξήντα'),
    (67, 'εξήντα επτά'),
    (70, 'εβδομήντα'),
    (78, 'εβδομήντα οκτώ'),
    (80, 'ογδόντα'),
    (89, 'ογδόντα εννέα'),
    (90, 'ενενήντα'),
    (95, 'ενενήντα πέντε'),
    (99, 'ενενήντα εννέα'),
    (100, 'εκατό'),
    (101, 'εκατό ένα'),
    (150, 'εκατό πενήντα'),
    (199, 'εκατό ενενήντα εννέα'),
    (200, 'διακόσια'),
    (203, 'διακόσια τρία'),
    (250, 'διακόσια πενήντα'),
    (300, 'τριακόσια'),
    (356, 'τριακόσια πενήντα έξι'),
    (400, 'τετρακόσια'),
    (434, 'τετρακόσια τριάντα τέσσερα'),
    (500, 'πεντακόσια'),
    (578, 'πεντακόσια εβδομήντα οκτώ'),
    (600, 'εξακόσια'),
    (689, 'εξακόσια ογδόντα εννέα'),
    (700, 'επτακόσια'),
    (729, 'επτακόσια είκοσι εννέα'),
    (800, 'οκτακόσια'),
    (894, 'οκτακόσια ενενήντα τέσσερα'),
    (900, 'εννιακόσια'),
    (999, 'εννιακόσια ενενήντα εννέα'),
    (1000, 'χίλια'),
    (1001, 'χίλια ένα'),
    (1097, 'χίλια ενενήντα επτά'),
    (1104, 'χίλια εκατό τέσσερα'),
    (1243, 'χίλια διακόσια σαράντα τρία'),
    (2000, 'δύο χιλιάδες'),
    (2385, 'δύο χιλιάδες τριακόσια ογδόντα πέντε'),
    (3000, 'τρεις χιλιάδες'),
    (3766, 'τρεις χιλιάδες επτακόσια εξήντα έξι'),
    (4000, 'τέσσερις χιλιάδες'),
    (4196, 'τέσσερις χιλιάδες εκατό ενενήντα έξι'),
    (5000, 'πέντε χιλιάδες'),
    (5846, 'πέντε χιλιάδες οκτακόσια σαράντα έξι'),
    (6000, 'έξι χιλιάδες'),
    (6459, 'έξι χιλιάδες τετρακόσια πενήντα εννέα'),
    (7000, 'επτά χιλιάδες'),
    (8000, 'οκτώ χιλιάδες'),
    (9000, 'εννέα χιλιάδες'),
    (10000, 'δέκα χιλιάδες'),
    (11000, 'έντεκα χιλιάδες'),
    (12000, 'δώδεκα χιλιάδες'),
    (13579, 'δεκατρία χιλιάδες πεντακόσια εβδομήντα εννέα'),
    (20000, 'είκοσι χιλιάδες'),
    (21000, 'είκοσι μία χιλιάδες'),
    (100000, 'εκατό χιλιάδες'),
    (200000, 'διακόσιες χιλιάδες'),
    (300000, 'τριακόσιες χιλιάδες'),
    (400000, 'τετρακόσιες χιλιάδες'),
    (500000, 'πεντακόσιες χιλιάδες'),
    (600000, 'εξακόσιες χιλιάδες'),
    (700000, 'επτακόσιες χιλιάδες'),
    (800000, 'οκτακόσιες χιλιάδες'),
    (900000, 'εννιακόσιες χιλιάδες'),
    (1000000, 'ένα εκατομμύριο'),
    (2000000, 'δύο εκατομμύρια'),
    (3000000, 'τρία εκατομμύρια'),
    (4000000, 'τέσσερα εκατομμύρια'),
    (5000000, 'πέντε εκατομμύρια'),
    (10000000, 'δέκα εκατομμύρια'),
    (50000000, 'πενήντα εκατομμύρια'),
    (100000000, 'εκατό εκατομμύρια'),
    (123456789, 'εκατό είκοσι τρία εκατομμύρια τετρακόσιες πενήντα έξι χιλιάδες επτακόσια ογδόντα εννέα'),
    (1000000000, 'ένα δισεκατομμύριο'),
    (2000000000, 'δύο δισεκατομμύρια'),
    (1000000000000, 'ένα τρισεκατομμύριο'),
    (1234567890, 'ένα δισεκατομμύριο διακόσια τριάντα τέσσερα εκατομμύρια πεντακόσιες εξήντα επτά χιλιάδες οκτακόσια ενενήντα'),
)

TEST_CASES_ORDINAL = (
    (1, 'πρώτος'),
    (2, 'δεύτερος'),
    (3, 'τρίτος'),
    (4, 'τέταρτος'),
    (5, 'πέμπτος'),
    (6, 'έκτος'),
    (7, 'έβδομος'),
    (8, 'όγδοος'),
    (9, 'έννατος'),
    (10, 'δέκατος'),
    (11, 'ενδέκατος'),
    (12, 'δωδέκατος'),
    (13, 'δεκατρίτος'),
    (14, 'δεκατέταρτος'),
    (20, 'εικοστός'),
    (21, 'εικοστός πρώτος'),
    (22, 'εικοστός δεύτερος'),
    (100, 'εκατοστός'),
    (101, 'εκατοστός πρώτος'),
    (102, 'εκατοστός δεύτερος'),
    (1000, 'χιλιοστός'),
    (1000000, 'εκατομμυριοστός'),
)

TEST_CASES_CURRENCY = (
    (0, 'μηδέν ευρώ'),
    (1, 'ένα ευρώ'),
    (2, 'δύο ευρώ'),
    (10, 'δέκα ευρώ'),
    (100, 'εκατό ευρώ'),
    (1.50, 'ένα ευρώ και πενήντα λεπτά'),
    (2.50, 'δύο ευρώ και πενήντα λεπτά'),
    (10.25, 'δέκα ευρώ και είκοσι πέντε λεπτά'),
    (100.99, 'εκατό ευρώ και ενενήντα εννέα λεπτά'),
    (0.01, 'μηδέν ευρώ και ένα λεπτό'),
    (0.05, 'μηδέν ευρώ και πέντε λεπτά'),
)

TEST_CASES_CURRENCY_USD = (
    (1, 'ένα δολάριο'),
    (2, 'δύο δολάρια'),
    (10, 'δέκα δολάρια'),
    (1.50, 'ένα δολάριο και πενήντα σεντς'),
    (2.25, 'δύο δολάρια και είκοσι πέντε σεντς'),
    (0.01, 'μηδέν δολάρια και ένα σεντ'),
)

TEST_CASES_CURRENCY_GBP = (
    (1, 'μία λίρα'),
    (2, 'δύο λίρες'),
    (10, 'δέκα λίρες'),
    (1.50, 'μία λίρα και πενήντα πένες'),
    (2.25, 'δύο λίρες και είκοσι πέντε πένες'),
    (0.01, 'μηδέν λίρες και μία πέννα'),
)


class Num2WordsELTest(TestCase):

    def test_cardinal(self):
        for number, expected in TEST_CASES_CARDINAL:
            with self.subTest(number=number):
                result = num2words(number, lang='el')
                self.assertEqual(result, expected)

    def test_ordinal(self):
        for number, expected in TEST_CASES_ORDINAL:
            with self.subTest(number=number):
                result = num2words(number, lang='el', to='ordinal')
                self.assertEqual(result, expected)

    def test_ordinal_num(self):
        self.assertEqual(num2words(1, lang='el', to='ordinal_num'), '1ος')
        self.assertEqual(num2words(22, lang='el', to='ordinal_num'), '22ος')
        self.assertEqual(num2words(100, lang='el', to='ordinal_num'), '100ος')

    def test_currency_eur(self):
        for number, expected in TEST_CASES_CURRENCY:
            with self.subTest(number=number):
                result = num2words(number, lang='el', to='currency', currency='EUR')
                self.assertEqual(result, expected)

    def test_currency_usd(self):
        for number, expected in TEST_CASES_CURRENCY_USD:
            with self.subTest(number=number):
                result = num2words(number, lang='el', to='currency', currency='USD')
                self.assertEqual(result, expected)

    def test_currency_gbp(self):
        for number, expected in TEST_CASES_CURRENCY_GBP:
            with self.subTest(number=number):
                result = num2words(number, lang='el', to='currency', currency='GBP')
                self.assertEqual(result, expected)

    def test_negative_numbers(self):
        self.assertEqual(num2words(-1, lang='el'), 'μείον ένα')
        self.assertEqual(num2words(-42, lang='el'), 'μείον σαράντα δύο')
        self.assertEqual(num2words(-100, lang='el'), 'μείον εκατό')
        self.assertEqual(num2words(-1000, lang='el'), 'μείον χίλια')

    def test_decimal_numbers(self):
        self.assertEqual(num2words(3.14, lang='el'), 'τρία κόμμα ένα τέσσερα')
        self.assertEqual(num2words(12.5, lang='el'), 'δώδεκα κόμμα πέντε')
        self.assertEqual(num2words(0.25, lang='el'), 'μηδέν κόμμα δύο πέντε')
        self.assertEqual(num2words(-5.75, lang='el'), 'μείον πέντε κόμμα επτά πέντε')

    def test_large_numbers(self):
        # Test very large numbers
        self.assertEqual(
            num2words(1234567890123, lang='el'),
            'ένα τρισεκατομμύριο διακόσια τριάντα τέσσερα δισεκατομμύρια πεντακόσια εξήντα επτά εκατομμύρια οκτακόσιες ενενήντα χιλιάδες εκατό είκοσι τρία'
        )

    def test_edge_cases(self):
        # Test numbers that require special grammatical handling
        self.assertEqual(num2words(21, lang='el'), 'είκοσι ένα')
        self.assertEqual(num2words(200, lang='el'), 'διακόσια')  # Neuter
        self.assertEqual(num2words(2000, lang='el'), 'δύο χιλιάδες')  # Feminine
        self.assertEqual(num2words(200000, lang='el'), 'διακόσιες χιλιάδες')  # Feminine hundreds with thousands
        self.assertEqual(num2words(2000000, lang='el'), 'δύο εκατομμύρια')  # Neuter millions
        self.assertEqual(num2words(200000000, lang='el'), 'διακόσια εκατομμύρια')  # Neuter hundreds with millions
