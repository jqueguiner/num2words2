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

from __future__ import division

from decimal import ROUND_HALF_UP, Decimal


def parse_currency_parts(
    value, is_int_with_cents=True, keep_precision=False, divisor=100
):
    """Split ``value`` into integer-part, fractional-subunit-part, sign.

    The default divisor of 100 corresponds to 2-decimal currencies
    (USD/EUR cents). Pass ``divisor=1000`` for 3-decimal currencies
    such as Tunisian/Bahraini/Kuwaiti/Omani/Jordanian/Libyan/Iraqi
    dinars (1 dinar = 1000 millimes/fils). Pass ``divisor=1`` for
    no-subunit currencies like JPY/KRW/VND. Issue #256 ports
    savoirfairelinux/num2words#256.
    """
    if isinstance(value, int):
        if is_int_with_cents:
            # assume cents (or whatever subunit divisor implies)
            negative = value < 0
            value = abs(value)
            integer, cents = divmod(value, divisor) if divisor else (value, 0)
        else:
            negative = value < 0
            integer, cents = abs(value), 0

    else:
        # Convert to string first to avoid float precision issues
        value = Decimal(str(value))

        if not keep_precision and divisor > 1:
            # Round to the precision implied by the divisor: 100 → .01,
            # 1000 → .001, etc. quant must be a Decimal power-of-ten.
            quant = Decimal(1) / Decimal(divisor)
            value = value.quantize(quant, rounding=ROUND_HALF_UP)

        negative = value < 0
        value = abs(value)
        integer, fraction = divmod(value, 1)
        integer = int(integer)

        if keep_precision:
            cents = fraction * divisor  # keep as Decimal
        else:
            cents = int(fraction * divisor)

    return integer, cents, negative


def prefix_currency(prefix, base):
    return tuple("%s %s" % (prefix, i) for i in base)
