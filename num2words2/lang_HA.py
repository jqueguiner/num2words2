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

from .base import Num2Word_Base


class Num2Word_HA(Num2Word_Base):
    """
    Hausa number-to-words converter.

    Supports cardinal numbers, ordinal numbers, currency conversion,
    and year representation in Hausa language.
    """

    CURRENCY_FORMS = {
        "NGN": (("naira", "naira"), ("kobo", "kobo")),
        "USD": (("dala", "dala"), ("cent", "cent")),
        "EUR": (("yuro", "yuro"), ("cent", "cent")),
        "GBP": (("fam", "fam"), ("pence", "pence")),
        "JPY": (("yen", "yen"), ("sen", "sen")),
        "CNY": (("yuan", "yuan"), ("fen", "fen")),
    }

    # Hausa numerals
    ONES = {
        0: "sifiri",
        1: "ɗaya",
        2: "biyu",
        3: "uku",
        4: "huɗu",
        5: "biyar",
        6: "shida",
        7: "bakwai",
        8: "takwas",
        9: "tara",
    }

    TEENS = {
        10: "goma",
        11: "sha ɗaya",
        12: "sha biyu",
        13: "sha uku",
        14: "sha huɗu",
        15: "sha biyar",
        16: "sha shida",
        17: "sha bakwai",
        18: "sha takwas",
        19: "sha tara",
    }

    TENS = {
        2: "ashirin",
        3: "talatin",
        4: "arba'in",
        5: "hamsin",
        6: "sittin",
        7: "saba'in",
        8: "tamanin",
        9: "casa'in",
    }

    SCALE = {
        100: "ɗari",
        1000: "dubu",
        1000000: "miliyan",
        1000000000: "biliyan",
        1000000000000: "tiriliyan",
    }

    def setup(self):
        """Setup the converter with Hausa-specific settings."""
        self.negword = "ban "
        self.pointword = "wajen"
        self.exclude_title = ["da", "wajen", "ban"]

    def to_cardinal(self, value):
        """Convert a number to its Hausa cardinal representation."""
        if value == 0:
            return self.ONES[0]

        if value < 0:
            return self.negword + self.to_cardinal(abs(value))

        # Handle floating point numbers
        if isinstance(value, float):
            return self.float_to_words(value)

        return self._int_to_hausa(value)

    def _int_to_hausa(self, number):
        """Convert an integer to Hausa words."""
        if number == 0:
            return ""

        if number < 10:
            return self.ONES[number]

        if number < 20:
            return self.TEENS[number]

        if number < 100:
            tens, units = divmod(number, 10)
            result = self.TENS[tens]
            if units > 0:
                result += " da " + self.ONES[units]
            return result

        if number < 1000:
            hundreds, remainder = divmod(number, 100)
            result = ""
            if hundreds == 1:
                result = "ɗari"
            else:
                result = "ɗari " + self.ONES[hundreds]

            if remainder > 0:
                if remainder < 10:
                    result += " da " + self._int_to_hausa(remainder)
                else:
                    result += " " + self._int_to_hausa(remainder)
            return result

        # Handle thousands and above
        for scale_value in sorted(self.SCALE.keys(), reverse=True):
            if number >= scale_value:
                quotient, remainder = divmod(number, scale_value)
                result = ""

                if scale_value == 100:
                    if quotient == 1:
                        result = "ɗari"
                    else:
                        result = "ɗari " + self._int_to_hausa(quotient)
                elif scale_value == 1000:
                    if quotient == 1:
                        result = "dubu"
                    else:
                        result = "dubu " + self._int_to_hausa(quotient)
                else:
                    # For millions, billions, etc.
                    scale_name = self.SCALE[scale_value]
                    if quotient == 1:
                        result = scale_name
                    else:
                        result = scale_name + " " + self._int_to_hausa(quotient)

                if remainder > 0:
                    if remainder < 10:
                        result += " da " + self._int_to_hausa(remainder)
                    else:
                        result += " " + self._int_to_hausa(remainder)

                return result

        return str(number)  # Fallback for very large numbers

    def to_ordinal(self, value):
        """Convert a number to its Hausa ordinal representation."""
        if value == 1:
            return "na farko"

        cardinal = self.to_cardinal(value)
        return "na " + cardinal

    def to_ordinal_num(self, value):
        """Convert a number to its ordinal representation with Arabic numerals."""
        # Using English-style ordinal suffixes as commonly used in Hausa contexts

        if 10 <= value % 100 <= 20:
            suffix = "th"
        else:
            last_digit = value % 10
            if last_digit == 1:
                suffix = "st"
            elif last_digit == 2:
                suffix = "nd"
            elif last_digit == 3:
                suffix = "rd"
            else:
                suffix = "th"

        return str(value) + suffix

    def to_year(self, value):
        """Convert a number to its Hausa year representation."""
        return self.to_cardinal(value)

    def to_currency(self, value, currency="NGN", cents=True):
        """Convert a value to its Hausa currency representation."""
        if currency not in self.CURRENCY_FORMS:
            currency = "NGN"  # Default to Nigerian Naira

        result = []
        is_negative = value < 0
        value = abs(value)

        # Check if value has fractional cents
        from decimal import Decimal

        decimal_val = Decimal(str(value))
        has_fractional_cents = (decimal_val * 100) % 1 != 0

        if cents:
            if has_fractional_cents:
                # Keep precision for fractional cents
                major_units = int(decimal_val)
                minor_units = decimal_val * 100 - (major_units * 100)
            else:
                # Convert to cents for processing
                cents_value = int(round(value * 100))
                major_units, minor_units = divmod(cents_value, 100)
        else:
            major_units = int(value)
            minor_units = 0

        currency_forms = self.CURRENCY_FORMS[currency]

        # Major currency unit
        if major_units > 0:
            major_name = currency_forms[0][0]  # Use singular form
            if major_units == 1:
                result.append(major_name + " " + self.to_cardinal(major_units))
            else:
                result.append(major_name + " " + self.to_cardinal(major_units))

        # Minor currency unit
        if minor_units > 0:
            minor_name = currency_forms[1][0]  # Use singular form
            # Handle fractional minor units
            from decimal import Decimal

            if isinstance(minor_units, Decimal):
                # Convert fractional cents (e.g., 65.3 kobo)
                minor_words = self.to_cardinal(float(minor_units))
            else:
                minor_words = self.to_cardinal(minor_units)

            if major_units > 0:
                result.append("da " + minor_name + " " + minor_words)
            else:
                result.append(minor_name + " " + minor_words)

        if not result:
            # Handle zero case
            major_name = currency_forms[0][0]
            result.append(major_name + " sifiri")

        if is_negative:
            result.insert(0, self.negword)

        return " ".join(result)

    def pluralize(self, n, forms):
        """Handle Hausa pluralization rules."""
        # Hausa doesn't have complex pluralization like some other languages
        # Generally use the first form provided
        if forms and len(forms) > 0:
            return forms[0]
        return ""

    def float_to_words(self, value):
        """Convert a floating point number to Hausa words."""
        if value == int(value):
            return self.to_cardinal(int(value))

        integer_part = int(value)
        decimal_part = value - integer_part

        # Get decimal digits
        decimal_str = str(decimal_part)[2:]  # Remove "0."

        result = self.to_cardinal(integer_part)
        result += " " + self.pointword + " "

        # Convert decimal digits
        decimal_num = int(decimal_str)
        result += self.to_cardinal(decimal_num)

        return result
