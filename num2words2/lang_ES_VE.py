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

from .lang_ES import Num2Word_ES


class Num2Word_ES_VE(Num2Word_ES):
    def __init__(self):
        super(Num2Word_ES_VE, self).__init__()
        # Copy parent currency forms and update for Venezuela
        self.CURRENCY_FORMS = self.CURRENCY_FORMS.copy()
        self.CURRENCY_FORMS.update(
            {
                "VES": (("bolívar", "bolívares"), ("centavo", "centavos")),
                "VEB": (
                    ("bolívar", "bolívares"),
                    ("centavo", "centavos"),
                ),  # Old currency
                "USD": (("dólar", "dólares"), ("centavo", "centavos")),
            }
        )

    def to_currency(
        self,
        val,
        currency="VES",
        cents=True,
        separator=" y",
        adjective=False,
        old=False,
    ):
        # Handle the old parameter for backward compatibility
        if old:
            # For old Venezuelan Bolívar (VEB)
            currency = "VEB" if currency == "VES" else currency

        # Use parent class implementation with our currency forms
        result = super(Num2Word_ES_VE, self).to_currency(
            val,
            currency=currency,
            cents=cents,
            separator=separator,
            adjective=adjective,
        )
        # Handle exception, in spanish is "un euro" and not "uno euro"
        return result.replace("uno", "un")
