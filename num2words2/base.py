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

import math
from collections import OrderedDict
from decimal import Decimal

from .compat import to_s
from .currency import parse_currency_parts, prefix_currency


class Num2Word_Base(object):
    CURRENCY_FORMS = {}
    CURRENCY_ADJECTIVES = {}
    # Number of fractional subunits per main unit. Default 100 (cents).
    # Currencies with non-cent subdivisions override per-code: 3-decimal
    # currencies use 1000 (mils); 0-decimal currencies use 1.
    # Issue #256 ports savoirfairelinux/num2words#256.
    CURRENCY_PRECISION = {}

    def __init__(self):
        self.is_title = False
        self.precision = 2
        self.exclude_title = []
        self.negword = "(-) "
        self.pointword = "(.)"
        self.errmsg_nonnum = "type(%s) not in [long, int, float]"
        self.errmsg_floatord = "Cannot treat float %s as ordinal."
        self.errmsg_negord = "Cannot treat negative num %s as ordinal."
        self.errmsg_toobig = "abs(%s) must be less than %s."

        self.setup()

        # uses cards
        if any(
            hasattr(self, field)
            for field in ["high_numwords", "mid_numwords", "low_numwords"]
        ):
            self.cards = OrderedDict()
            self.set_numwords()
            self.MAXVAL = 1000 * list(self.cards.keys())[0]

    def set_numwords(self):
        self.set_high_numwords(self.high_numwords)
        self.set_mid_numwords(self.mid_numwords)
        self.set_low_numwords(self.low_numwords)

    def set_high_numwords(self, *args):
        raise NotImplementedError

    def set_mid_numwords(self, mid):
        for key, val in mid:
            self.cards[key] = val

    def set_low_numwords(self, numwords):
        for word, n in zip(numwords, range(len(numwords) - 1, -1, -1)):
            self.cards[n] = word

    def splitnum(self, value):
        for elem in self.cards:
            if elem > value:
                continue

            out = []
            if value == 0:
                div, mod = 1, 0
            else:
                div, mod = divmod(value, elem)

            if div == 1:
                out.append((self.cards[1], 1))
            else:
                if div == value:  # The system tallies, eg Roman Numerals
                    return [(div * self.cards[elem], div * elem)]
                out.append(self.splitnum(div))

            out.append((self.cards[elem], elem))

            if mod:
                out.append(self.splitnum(mod))

            return out

    def parse_minus(self, num_str):
        """Detach minus and return it as symbol with new num_str."""
        if num_str.startswith("-"):
            # Extra spacing to compensate if there is no minus.
            return "%s " % self.negword.strip(), num_str[1:]
        return "", num_str

    def str_to_number(self, value):
        return Decimal(value)

    def to_cardinal(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)

        out = ""
        if value < 0:
            value = abs(value)
            out = "%s " % self.negword.strip()

        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        val = self.splitnum(value)
        words, num = self.clean(val)
        return self.title(out + words)

    def float2tuple(self, value):
        # Decimal input keeps full precision: avoid the float() cast that
        # would silently round e.g. 98_746_251_323_029.99 to .98 at trillion
        # scale. Issue #603 ports savoirfairelinux/num2words#603.
        if isinstance(value, Decimal):
            pre = int(value)
            self.precision = abs(value.as_tuple().exponent)
            post = abs(value - Decimal(pre)) * (Decimal(10) ** self.precision)
            return pre, int(post)

        pre = int(value)

        # Simple way of finding decimal places to update the precision
        self.precision = abs(Decimal(str(value)).as_tuple().exponent)

        post = abs(value - pre) * 10**self.precision
        if abs(round(post) - post) < 0.01:
            # We generally floor all values beyond our precision (rather than
            # rounding), but in cases where we have something like 1.239999999,
            # which is probably due to python's handling of floats, we actually
            # want to consider it as 1.24 instead of 1.23
            post = int(round(post))
        else:
            post = int(math.floor(post))

        return pre, post

    def to_cardinal_float(self, value, precision=None):
        try:
            float(value) == value
        except (ValueError, TypeError, AssertionError, AttributeError):
            raise TypeError(self.errmsg_nonnum % value)

        # Caller-supplied precision overrides the per-instance default.
        # Issue #580 ports savoirfairelinux/num2words#580.
        saved_precision = self.precision
        if precision is not None:
            self.precision = int(precision)
        try:
            # Preserve Decimal precision; only float-cast plain numerics.
            # Issue #603 ports savoirfairelinux/num2words#603.
            if isinstance(value, Decimal):
                pre, post = self.float2tuple(value)
            else:
                pre, post = self.float2tuple(float(value))

            post = str(post)
            post = "0" * (self.precision - len(post)) + post

            out = [self.to_cardinal(pre)]
            if value < 0 and pre == 0:
                out = [self.negword.strip()] + out

            if self.precision:
                out.append(self.title(self.pointword))

            for i in range(self.precision):
                curr = int(post[i])
                out.append(to_s(self.to_cardinal(curr)))

            return " ".join(out)
        finally:
            self.precision = saved_precision

    def merge(self, curr, next):
        raise NotImplementedError

    def clean(self, val):
        out = val
        while len(val) != 1:
            out = []
            left, right = val[:2]
            if isinstance(left, tuple) and isinstance(right, tuple):
                out.append(self.merge(left, right))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self.clean(elem))
                    else:
                        out.append(elem)
            val = out
        return out[0]

    def title(self, value):
        if self.is_title:
            out = []
            value = value.split()
            for word in value:
                if word in self.exclude_title:
                    out.append(word)
                else:
                    out.append(word[0].upper() + word[1:])
            value = " ".join(out)
        return value

    def verify_ordinal(self, value):
        if not value == int(value):
            raise TypeError(self.errmsg_floatord % value)
        if not abs(value) == value:
            raise TypeError(self.errmsg_negord % value)

    def to_ordinal(self, value):
        return self.to_cardinal(value)

    def to_ordinal_num(self, value):
        return value

    # Trivial version
    def inflect(self, value, text):
        text = text.split("/")
        if value == 1:
            return text[0]
        return "".join(text)

    # //CHECK: generalise? Any others like pounds/shillings/pence?
    def to_splitnum(
        self,
        val,
        hightxt="",
        lowtxt="",
        jointxt="",
        divisor=100,
        longval=True,
        cents=True,
    ):
        out = []

        if isinstance(val, float):
            high, low = self.float2tuple(val)
        else:
            try:
                high, low = val
            except TypeError:
                high, low = divmod(val, divisor)

        if high:
            hightxt = self.title(self.inflect(high, hightxt))
            out.append(self.to_cardinal(high))
            if low:
                if longval:
                    if hightxt:
                        out.append(hightxt)
                    if jointxt:
                        out.append(self.title(jointxt))
            elif hightxt:
                out.append(hightxt)

        if low:
            if cents:
                out.append(self.to_cardinal(low))
            else:
                out.append("%02d" % low)
            if lowtxt and longval:
                out.append(self.title(self.inflect(low, lowtxt)))

        return " ".join(out)

    def to_year(self, value, **kwargs):
        return self.to_cardinal(value)

    def pluralize(self, n, forms):
        """
        Should resolve gettext form:
        http://docs.translatehouse.org/projects/localization-guide/en/latest/l10n/pluralforms.html
        """
        raise NotImplementedError

    def _money_verbose(self, number, currency):
        return self.to_cardinal(number)

    def _cents_verbose(self, number, currency):
        return self.to_cardinal(number)

    def _cents_terse(self, number, currency):
        # Width follows the currency's subunit precision: 2 for cents
        # (default), 3 for mils (TND/BHD/KWD/etc.). Issue #256.
        divisor = self.CURRENCY_PRECISION.get(currency, 100)
        if divisor <= 1:
            return "%d" % int(number)
        width = len(str(divisor)) - 1
        return "%0*d" % (width, int(number))

    def to_cheque(self, val, currency="USD"):
        """Bank-cheque format: ``ONE THOUSAND AND 56/100 DOLLARS``.

        Standard convention is the integer part written out as words, the
        word "AND", the fractional part as digits over the divisor (e.g.
        56/100 for cents, 005/1000 for mils), and the plural currency
        name. The whole thing is upper-cased per banking style. Issue
        #364 ports savoirfairelinux/num2words#364.
        """
        from decimal import Decimal

        try:
            cr1, _cr2 = self.CURRENCY_FORMS[currency]
        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"'
                % (currency, self.__class__.__name__)
            )

        divisor = self.CURRENCY_PRECISION.get(currency, 100)
        decimal_val = Decimal(str(val))
        is_negative = decimal_val < 0
        abs_val = abs(decimal_val)

        whole = int(abs_val)
        # Pull the fractional subunit out at the currency's precision.
        if divisor > 1:
            sub = int((abs_val - whole) * divisor)
            digits = len(str(divisor)) - 1
            fraction_str = "%0*d/%d" % (digits, sub, divisor)
        else:
            fraction_str = ""

        words = self._money_verbose(whole, currency)
        # Cheque convention always uses the plural currency name
        # ("ONE AND 00/100 DOLLARS", not "...DOLLAR"), so we take the
        # plural form unconditionally.
        unit = cr1[-1] if isinstance(cr1, tuple) else cr1

        sign = "MINUS " if is_negative else ""
        if fraction_str:
            body = "%s AND %s %s" % (words, fraction_str, unit)
        else:
            body = "%s %s" % (words, unit)
        return (sign + body).upper()

    def to_currency(
        self, val, currency="EUR", cents=True, separator=",", adjective=False
    ):
        """
        Args:
            val: Numeric value
            currency (str): Currency code
            cents (bool): Verbose cents
            separator (str): Cent separator
            adjective (bool): Prefix currency name with adjective
        Returns:
            str: Formatted string

        Handles whole numbers and decimal numbers differently
        """
        # Zero-decimal currencies (JPY, KRW, ...) have no subunit, so any
        # fractional input is rounded to a whole unit and the result skips
        # the cents segment entirely. Issue #256.
        if self.CURRENCY_PRECISION.get(currency, 100) == 1 and not isinstance(val, int):
            from decimal import ROUND_HALF_UP, Decimal
            val = int(Decimal(str(val)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

        # Handle integers separately - no cents shown
        # Only pure integers, NOT floats that happen to be whole numbers
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except KeyError:
                raise NotImplementedError(
                    'Currency code "%s" not implemented for "%s"'
                    % (currency, self.__class__.__name__)
                )

            if adjective and currency in self.CURRENCY_ADJECTIVES:
                cr1 = prefix_currency(self.CURRENCY_ADJECTIVES[currency], cr1)

            val_int = int(val) if isinstance(val, float) else val
            minus_str = "%s " % self.negword.strip() if val_int < 0 else ""
            money_str = self._money_verbose(abs(val_int), currency)

            return "%s%s %s" % (minus_str, money_str, self.pluralize(abs(val_int), cr1))

        # For floats, show full currency with subunits (cents/mils/etc.)
        # The divisor is per-currency: 100 (cents) by default, 1000 (mils)
        # for 3-decimal currencies, 1 for no-subunit currencies. Issue #256.
        from decimal import Decimal

        divisor = self.CURRENCY_PRECISION.get(currency, 100)
        decimal_val = Decimal(str(val))
        has_fractional_cents = (decimal_val * divisor) % 1 != 0

        left, right, is_negative = parse_currency_parts(
            val,
            is_int_with_cents=False,
            keep_precision=has_fractional_cents,
            divisor=divisor,
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
        has_decimal = isinstance(val, float) or str(val).find(".") != -1

        # Only include cents if:
        # 1. Input has decimal point OR
        # 2. Cents are non-zero
        if (
            has_decimal
            or (isinstance(right, Decimal) and right > 0)
            or (isinstance(right, int) and right > 0)
        ):
            # Handle fractional cents
            if isinstance(right, Decimal):
                # Split into whole cents and fraction
                whole_cents = int(right)
                fractional_part = right - whole_cents

                if fractional_part > 0:
                    # Convert fractional cents (e.g., 65.3 cents)
                    cents_str = self.to_cardinal(float(right))
                    return "%s%s %s%s %s %s" % (
                        minus_str,
                        money_str,
                        self.pluralize(left, cr1),
                        separator,
                        cents_str,
                        cr2[1] if isinstance(cr2, tuple) and len(cr2) > 1 else cr2,
                    )
                else:
                    # No fractional part, use normal processing
                    right = whole_cents

            cents_str = (
                self._cents_verbose(right, currency)
                if cents
                else self._cents_terse(right, currency)
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

    def setup(self):
        pass
