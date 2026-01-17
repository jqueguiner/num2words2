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

from num2words import num2words

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
    (7232, 'επτά χιλιάδες διακόσια τριάντα δύο'),
    (8000, 'οκτώ χιλιάδες'),
    (8569, 'οκτώ χιλιάδες πεντακόσια εξήντα εννέα'),
    (9000, 'εννέα χιλιάδες'),
    (9539, 'εννέα χιλιάδες πεντακόσια τριάντα εννέα'),
    (10000, 'δέκα χιλιάδες'),
    (11000, 'έντεκα χιλιάδες'),
    (12000, 'δώδεκα χιλιάδες'),
    (20000, 'είκοσι χιλιάδες'),
    (100000, 'εκατό χιλιάδες'),
    (1000000, 'ένα εκατομμύριο'),
    (1000001, 'ένα εκατομμύριο ένα'),
    (2000000, 'δύο εκατομμύρια'),
    (4000000, 'τέσσερα εκατομμύρια'),
    (4000004, 'τέσσερα εκατομμύρια τέσσερα'),
    (4300000, 'τέσσερα εκατομμύρια τριακόσιες χιλιάδες'),
    (80000000, 'ογδόντα εκατομμύρια'),
    (300000000, 'τριακόσια εκατομμύρια'),
    (1000000000, 'ένα δισεκατομμύριο'),
    (1000000000000, 'ένα τρισεκατομμύριο'),
)

TEST_CASES_ORDINAL = (
    (1, 'πρώτος'),
    (2, 'δεύτερος'),
    (3, 'τρίτος'),
    (4, 'τέταρτος'),
    (5, 'πέμπτος'),
    (8, 'όγδοος'),
    (10, 'δέκατος'),
    (11, 'ενδέκατος'),
    (12, 'δωδέκατος'),
    (14, 'δεκατέταρτος'),
    (20, 'εικοστός'),
    (21, 'εικοστός πρώτος'),
    (28, 'εικοστός όγδοος'),
    (100, 'εκατοστός'),
    (101, 'εκατοστός πρώτος'),
    (1000, 'χιλιοστός'),
    (1000000, 'εκατομμυριοστός'),
)

TEST_CASES_ORDINAL_NUM = (
    (1, '1ος'),
    (2, '2ος'),
    (3, '3ος'),
    (4, '4ος'),
    (5, '5ος'),
    (8, '8ος'),
    (11, '11ος'),
    (12, '12ος'),
    (14, '14ος'),
    (21, '21ος'),
    (28, '28ος'),
    (100, '100ος'),
    (101, '101ος'),
    (1000, '1000ος'),
    (1000000, '1000000ος'),
)

TEST_CASES_TO_CURRENCY_EUR = (
    (1.00, 'ένα ευρώ και μηδέν λεπτά'),
    (2.01, 'δύο ευρώ και ένα λεπτό'),
    (8.10, 'οκτώ ευρώ και δέκα λεπτά'),
    (12.26, 'δώδεκα ευρώ και είκοσι έξι λεπτά'),
    (21.29, 'είκοσι ένα ευρώ και είκοσι εννέα λεπτά'),
    (81.25, 'ογδόντα ένα ευρώ και είκοσι πέντε λεπτά'),
    (100.00, 'εκατό ευρώ και μηδέν λεπτά'),
)

TEST_CASES_TO_CURRENCY_USD = (
    (1.00, 'ένα δολάριο και μηδέν σεντς'),
    (2.01, 'δύο δολάρια και ένα σεντ'),
    (8.10, 'οκτώ δολάρια και δέκα σεντς'),
    (12.26, 'δώδεκα δολάρια και είκοσι έξι σεντς'),
    (21.29, 'είκοσι ένα δολάρια και είκοσι εννέα σεντς'),
    (81.25, 'ογδόντα ένα δολάρια και είκοσι πέντε σεντς'),
    (100.00, 'εκατό δολάρια και μηδέν σεντς'),
)

TEST_CASES_DECIMAL = (
    (5.5, 'πέντε κόμμα πέντε'),
    (17.42, 'δεκαεπτά κόμμα τέσσερα δύο'),
    (27.312, 'είκοσι επτά κόμμα τρία ένα δύο'),
    (53.486, 'πενήντα τρία κόμμα τέσσερα οκτώ έξι'),
    (300.42, 'τριακόσια κόμμα τέσσερα δύο'),
    (4196.42, 'τέσσερις χιλιάδες εκατό ενενήντα έξι κόμμα τέσσερα δύο'),
)


class Num2WordsELTest(TestCase):
    def test_number(self):
        for test in TEST_CASES_CARDINAL:
            self.assertEqual(num2words(test[0], lang='el'), test[1])

    def test_ordinal(self):
        for test in TEST_CASES_ORDINAL:
            self.assertEqual(
                num2words(test[0], lang='el', ordinal=True),
                test[1]
            )

    def test_ordinal_num(self):
        for test in TEST_CASES_ORDINAL_NUM:
            self.assertEqual(
                num2words(test[0], lang='el', to='ordinal_num'),
                test[1]
            )

    def test_currency_eur(self):
        for test in TEST_CASES_TO_CURRENCY_EUR:
            self.assertEqual(
                num2words(test[0], lang='el', to='currency', currency='EUR'),
                test[1]
            )

    def test_currency_usd(self):
        for test in TEST_CASES_TO_CURRENCY_USD:
            self.assertEqual(
                num2words(test[0], lang='el', to='currency', currency='USD'),
                test[1]
            )

    def test_decimal(self):
        for test in TEST_CASES_DECIMAL:
            self.assertEqual(num2words(test[0], lang='el'), test[1])

    def test_max_numbers(self):
        with self.assertRaises(OverflowError) as context:
            num2words(10 ** 700, lang='el')
        
        self.assertTrue('πολύ μεγάλος' in str(context.exception))

    def test_negative_numbers(self):
        self.assertEqual(num2words(-1, lang='el'), 'μείον ένα')
        self.assertEqual(num2words(-42, lang='el'), 'μείον σαράντα δύο')
        self.assertEqual(num2words(-100, lang='el'), 'μείον εκατό')
        self.assertEqual(num2words(-1000, lang='el'), 'μείον χίλια')

    def test_negative_decimals(self):
        self.assertEqual(num2words(-0.4, lang='el'), 'μείον μηδέν κόμμα τέσσερα')
        self.assertEqual(num2words(-0.5, lang='el'), 'μείον μηδέν κόμμα πέντε')
        self.assertEqual(num2words(-0.04, lang='el'), 'μείον μηδέν κόμμα μηδέν τέσσερα')
        self.assertEqual(num2words(-1.4, lang='el'), 'μείον ένα κόμμα τέσσερα')
        self.assertEqual(num2words(-10.25, lang='el'), 'μείον δέκα κόμμα δύο πέντε')

    def test_zero(self):
        self.assertEqual(num2words(0, lang='el'), 'μηδέν')
        self.assertEqual(num2words(0.0, lang='el'), 'μηδέν')

    def test_large_numbers(self):
        self.assertEqual(num2words(1234567890, lang='el'), 
                        'ένα δισεκατομμύριο διακόσια τριάντα τέσσερις εκατομμύρια πεντακόσιες εξήντα επτά χιλιάδες οκτακόσια ενενήντα')