from num2words2 import num2words


class LangTest:  # No longer inherits from TestCase directly
    lang = None

    cardinal_tests = []
    ordinal_tests = []
    ordinal_num_tests = []
    year_tests = []
    currency_tests = []
    float_tests = []
    negative_tests = []

    def _run_cardinal_tests(self):
        if not self.lang or not self.cardinal_tests:
            self.skipTest(f"No cardinal tests for language: {self.lang}")
        for num, expected in self.cardinal_tests:
            with self.subTest(num=num):
                self.assertEqual(num2words(num, lang=self.lang), expected)

    def _run_ordinal_tests(self):
        if not self.lang or not self.ordinal_tests:
            self.skipTest(f"No ordinal tests for language: {self.lang}")
        for num, expected in self.ordinal_tests:
            with self.subTest(num=num):
                self.assertEqual(num2words(num, to="ordinal", lang=self.lang), expected)

    def _run_ordinal_num_tests(self):
        if not self.lang or not self.ordinal_num_tests:
            self.skipTest(f"No ordinal_num tests for language: {self.lang}")
        for num, expected in self.ordinal_num_tests:
            with self.subTest(num=num):
                self.assertEqual(
                    num2words(num, to="ordinal_num", lang=self.lang), expected
                )

    def _run_year_tests(self):
        if not self.lang or not self.year_tests:
            self.skipTest(f"No year tests for language: {self.lang}")
        for num, expected, *args in self.year_tests:
            kwargs = {"to": "year", "lang": self.lang}
            if args:
                kwargs.update(args[0])
            with self.subTest(num=num, kwargs=kwargs):
                self.assertEqual(num2words(num, **kwargs), expected)

    def _run_currency_tests(self):
        if not self.lang or not self.currency_tests:
            self.skipTest(f"No currency tests for language: {self.lang}")
        for num, expected, *args in self.currency_tests:
            kwargs = {"to": "currency", "lang": self.lang}
            if args:
                kwargs.update(args[0])
            with self.subTest(num=num, kwargs=kwargs):
                self.assertEqual(num2words(num, **kwargs), expected)

    def _run_float_tests(self):
        if not self.lang or not self.float_tests:
            self.skipTest(f"No float tests for language: {self.lang}")
        for num, expected in self.float_tests:
            with self.subTest(num=num):
                self.assertEqual(num2words(num, lang=self.lang), expected)

    def _run_negative_tests(self):
        if not self.lang or not self.negative_tests:
            self.skipTest(f"No negative tests for language: {self.lang}")
        for num, expected in self.negative_tests:
            with self.subTest(num=num):
                self.assertEqual(num2words(num, lang=self.lang), expected)
