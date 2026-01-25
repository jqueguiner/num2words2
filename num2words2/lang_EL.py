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

from .lang_EUR import Num2Word_EUR


class Num2Word_EL(Num2Word_EUR):
    CURRENCY_FORMS = {
        "EUR": (("ευρώ", "ευρώ"), ("λεπτό", "λεπτά")),
        "USD": (("δολάριο", "δολάρια"), ("σεντ", "σεντς")),
        "GBP": (("λίρα", "λίρες"), ("πέννα", "πένες")),
    }

    def setup(self):
        Num2Word_EUR.setup(self)

        self.negword = "μείον "
        self.pointword = "κόμμα"
        self.errmsg_nonnum = "Μόνο αριθμοί μπορούν να μετατραπούν σε λέξεις."
        self.errmsg_toobig = (
            "Αριθμός πολύ μεγάλος για να μετατραπεί σε λέξεις (abs(%s) > %s)."
        )
        self.exclude_title = ["και", "κόμμα", "μείον"]

        # Override the EU settings with Greek
        self.GIGA_SUFFIX = ""  # Don't use the EU pattern
        self.MEGA_SUFFIX = ""  # Don't use the EU pattern

        # Mid numbers: thousands and hundreds with tens
        self.mid_numwords = [
            (1000000000000, "τρισεκατομμύριο"),
            (1000000000, "δισεκατομμύριο"),
            (1000000, "εκατομμύριο"),
            (1000, "χίλια"),
            (100, "εκατό"),
            (90, "ενενήντα"),
            (80, "ογδόντα"),
            (70, "εβδομήντα"),
            (60, "εξήντα"),
            (50, "πενήντα"),
            (40, "σαράντα"),
            (30, "τριάντα"),
        ]

        # Low numbers 0-29
        self.low_numwords = [
            "είκοσι",
            "δεκαεννέα",
            "δεκαοκτώ",
            "δεκαεπτά",
            "δεκαέξι",
            "δεκαπέντε",
            "δεκατέσσερα",
            "δεκατρία",
            "δώδεκα",
            "έντεκα",
            "δέκα",
            "εννέα",
            "οκτώ",
            "επτά",
            "έξι",
            "πέντε",
            "τέσσερα",
            "τρία",
            "δύο",
            "ένα",
            "μηδέν",
        ]

        # Ordinal numbers mapping
        self.ordinals = {
            "ένα": "πρώτος",
            "δύο": "δεύτερος",
            "τρία": "τρίτος",
            "τέσσερα": "τέταρτος",
            "πέντε": "πέμπτος",
            "έξι": "έκτος",
            "επτά": "έβδομος",
            "οκτώ": "όγδοος",
            "εννέα": "έννατος",
            "δέκα": "δέκατος",
            "έντεκα": "ενδέκατος",
            "δώδεκα": "δωδέκατος",
            "είκοσι": "εικοστός",
            "εκατό": "εκατοστός",
            "χίλια": "χιλιοστός",
            "εκατομμύριο": "εκατομμυριοστός",
        }

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        # Special handling for 1
        if cnum == 1:
            if nnum == 100:
                return ("εκατό", 100)
            elif nnum == 1000:
                return ("χίλια", 1000)
            elif nnum >= 1000000:
                return ("ένα " + ntext, cnum * nnum)
            elif nnum < 1000000:
                return next

        # Handle multiplication (larger unit)
        if nnum > cnum:
            if nnum == 100:
                # Hundreds
                if cnum == 2:
                    return ("διακόσια", 200)
                elif cnum == 3:
                    return ("τριακόσια", 300)
                elif cnum == 4:
                    return ("τετρακόσια", 400)
                elif cnum == 5:
                    return ("πεντακόσια", 500)
                elif cnum == 6:
                    return ("εξακόσια", 600)
                elif cnum == 7:
                    return ("επτακόσια", 700)
                elif cnum == 8:
                    return ("οκτακόσια", 800)
                elif cnum == 9:
                    return ("εννιακόσια", 900)
            elif nnum == 1000:
                # Thousands - need feminine forms for certain numbers
                if cnum == 1:
                    # Special case: when merging compound numbers ending with 1
                    # For feminine thousands, "ένα" becomes "μία"
                    if "ένα" in ctext:
                        ctext_fem = ctext.replace("ένα", "μία")
                        return (ctext_fem + " χιλιάδες", cnum * nnum)
                    else:
                        return ("χίλια", 1000)
                elif cnum == 2:
                    return ("δύο χιλιάδες", 2000)
                elif cnum == 3:
                    return ("τρεις χιλιάδες", 3000)
                elif cnum == 4:
                    return ("τέσσερις χιλιάδες", 4000)
                elif cnum == 200:
                    return ("διακόσιες χιλιάδες", 200000)
                elif cnum == 300:
                    return ("τριακόσιες χιλιάδες", 300000)
                elif cnum == 400:
                    return ("τετρακόσιες χιλιάδες", 400000)
                elif cnum == 500:
                    return ("πεντακόσιες χιλιάδες", 500000)
                elif cnum == 600:
                    return ("εξακόσιες χιλιάδες", 600000)
                elif cnum == 700:
                    return ("επτακόσιες χιλιάδες", 700000)
                elif cnum == 800:
                    return ("οκτακόσιες χιλιάδες", 800000)
                elif cnum == 900:
                    return ("εννιακόσιες χιλιάδες", 900000)
                else:
                    # For other numbers, adjust the form for feminine thousands
                    ctext_new = ctext
                    # Convert "ένα" to "μία" for feminine thousands
                    ctext_new = ctext_new.replace("ένα", "μία")
                    # Convert all hundreds to feminine form for χιλιάδες
                    ctext_new = ctext_new.replace("διακόσια", "διακόσιες")
                    ctext_new = ctext_new.replace("τριακόσια", "τριακόσιες")
                    ctext_new = ctext_new.replace("τετρακόσια", "τετρακόσιες")
                    ctext_new = ctext_new.replace("πεντακόσια", "πεντακόσιες")
                    ctext_new = ctext_new.replace("εξακόσια", "εξακόσιες")
                    ctext_new = ctext_new.replace("επτακόσια", "επτακόσιες")
                    ctext_new = ctext_new.replace("οκτακόσια", "οκτακόσιες")
                    ctext_new = ctext_new.replace("εννιακόσια", "εννιακόσιες")
                    return (ctext_new + " χιλιάδες", cnum * nnum)
            elif nnum == 1000000:
                # Millions - need special grammar for compound numbers
                if cnum == 1:
                    return ("ένα εκατομμύριο", 1000000)
                elif cnum == 2:
                    return ("δύο εκατομμύρια", 2000000)
                elif cnum == 3:
                    return ("τρία εκατομμύρια", 3000000)
                elif cnum == 4:
                    return ("τέσσερα εκατομμύρια", 4000000)
                else:
                    # For compound numbers with millions, εκατομμύρια is neuter
                    # so we keep the neuter forms (τέσσερα, not τέσσερις)
                    return (ctext + " εκατομμύρια", cnum * nnum)
            elif nnum == 1000000000:
                # Billions
                if cnum == 1:
                    return ("ένα δισεκατομμύριο", 1000000000)
                else:
                    return (ctext + " δισεκατομμύρια", cnum * nnum)
            elif nnum == 1000000000000:
                # Trillions
                if cnum == 1:
                    return ("ένα τρισεκατομμύριο", 1000000000000)
                else:
                    return (ctext + " τρισεκατομμύρια", cnum * nnum)
            elif nnum >= 1000000:
                # Other large numbers
                if cnum == 1:
                    return ("ένα " + ntext, cnum * nnum)
                else:
                    return (ctext + " " + ntext, cnum * nnum)
            else:
                # Regular multiplication
                return (ctext + " " + ntext, cnum * nnum)

        # Handle addition (smaller unit added)
        else:
            return (ctext + " " + ntext, cnum + nnum)

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        word = self.to_cardinal(value)

        # Handle special cases first
        for cardinal, ordinal in self.ordinals.items():
            if word == cardinal:
                return ordinal

        # Handle special compound numbers
        if word == "δεκατέσσερα":
            return "δεκατέταρτος"
        elif word == "δεκατρία":
            return "δεκατρίτος"
        elif word == "ένα εκατομμύριο":
            return "εκατομμυριοστός"

        # Handle compound ordinals
        parts = word.split()
        if len(parts) > 1:
            # Handle "είκοσι ένα" -> "εικοστός πρώτος"
            if parts[0] == "είκοσι" and parts[1] == "ένα":
                return "εικοστός πρώτος"
            elif parts[0] == "είκοσι" and parts[1] in self.ordinals:
                return "εικοστός " + self.ordinals[parts[1]]
            # Handle "εκατό ένα" -> "εκατοστός πρώτος"
            elif parts[0] == "εκατό" and parts[1] == "ένα":
                return "εκατοστός πρώτος"
            elif parts[0] == "εκατό" and parts[1] in self.ordinals:
                return "εκατοστός " + self.ordinals[parts[1]]

            # For compound numbers, make only the last part ordinal
            last_part = parts[-1]
            if last_part in self.ordinals:
                # Transform first part if needed
                if parts[0] == "είκοσι":
                    parts[0] = "εικοστός"
                elif parts[0] == "εκατό":
                    parts[0] = "εκατοστός"
                parts[-1] = self.ordinals[last_part]
                return " ".join(parts)
            # Handle other compound forms
            elif last_part == "τέσσερα":
                parts[-1] = "τέταρτος"
                return " ".join(parts)

        # Default ordinal formation
        if word.endswith("α"):
            return word[:-1] + "ος"
        elif word.endswith("ο"):
            return word[:-1] + "ος"
        elif word.endswith("ι"):
            return word + "ος"
        else:
            return word + "ος"

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return str(value) + "ος"

    def _money_verbose(self, number, currency):
        if currency == "GBP" and number == 1:
            return "μία"  # Feminine form for λίρα
        return self.to_cardinal(number)

    def _cents_verbose(self, number, currency):
        if currency == "GBP" and number == 1:
            return "μία"  # Feminine form for πέννα
        return self.to_cardinal(number)

    def to_currency(
        self, val, currency="EUR", cents=True, separator=" και", adjective=False
    ):
        from decimal import Decimal

        from .currency import parse_currency_parts, prefix_currency

        # Check if value has fractional cents
        decimal_val = Decimal(str(val))
        has_fractional_cents = (decimal_val * 100) % 1 != 0

        # Fix the currency parsing issue - integers and whole floats should be treated as whole units
        if isinstance(val, int) or (isinstance(val, float) and val == int(val)):
            left, right, is_negative = parse_currency_parts(
                int(val) if isinstance(val, float) else val, is_int_with_cents=False
            )
        else:
            left, right, is_negative = parse_currency_parts(
                val, is_int_with_cents=False, keep_precision=has_fractional_cents
            )

        try:
            cr1, cr2 = self.CURRENCY_FORMS[currency]
        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"'
                % (currency, self.__class__.__name__)
            )

        if adjective and currency in self.CURRENCY_ADJECTIVES:
            cr1 = prefix_currency(self.CURRENCY_ADJECTIVES[currency], cr1)

        minus_str = "%s " % self.negword.strip() if is_negative else ""
        money_str = self._money_verbose(left, currency)

        # Explicitly check if input has decimal point or non-zero cents
        # But exclude whole number floats like 100.0
        is_whole_float = isinstance(val, float) and val == int(val)
        has_decimal = (isinstance(val, float) and not is_whole_float) or str(val).find(
            "."
        ) != -1

        # Only include cents if:
        # 1. Input has decimal point (and not a whole number) OR
        # 2. Cents are non-zero
        if (has_decimal and not is_whole_float) or right > 0:
            # Handle fractional cents
            if isinstance(right, Decimal) and has_fractional_cents:
                # Convert fractional cents (e.g., 65.3 cents)
                cents_str = (
                    self.to_cardinal_float(float(right)) if cents else str(float(right))
                )
            else:
                cents_str = (
                    self._cents_verbose(
                        int(right) if isinstance(right, Decimal) else right, currency
                    )
                    if cents
                    else self._cents_terse(
                        int(right) if isinstance(right, Decimal) else right, currency
                    )
                )

            return "%s%s %s%s %s %s" % (
                minus_str,
                money_str,
                self.pluralize(left, cr1),
                separator,
                cents_str,
                self.pluralize(right, cr2),
            )
        else:
            return "%s%s %s" % (minus_str, money_str, self.pluralize(left, cr1))

    def pluralize(self, n, forms):
        if n == 1:
            return forms[0]
        else:
            return forms[1]
