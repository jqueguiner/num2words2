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

"""
Module for converting numbers to words in Shona (chiShona).
Shona is a Bantu language spoken in Zimbabwe and Mozambique.
"""

from __future__ import unicode_literals

from .base import Num2Word_Base
from .utils import get_digits, splitbyx

class Num2Word_SN(Num2Word_Base):
    """Convert numbers to Shona words."""
    
    CURRENCY_FORMS = {
        'USD': (
            ('dhora', 'madhora'), ('sendi', 'masendi')
        ),
        'ZWL': (
            ('dhora', 'madhora'), ('sendi', 'masendi')
        ),
        'ZAR': (
            ('randi', 'marandi'), ('sendi', 'masendi')
        ),
    }

    def __init__(self):
        # Basic numbers 0-10
        self.ones = {
            0: 'zero',
            1: 'motsi',
            2: 'piri',
            3: 'tatu',
            4: 'china',
            5: 'shanu',
            6: 'tanhatu',
            7: 'nomwe',
            8: 'sere',
            9: 'pfumbamwe',
            10: 'gumi'
        }
        
        # Numbers for tens when used in compound forms
        self.tens_forms = {
            2: 'maviri',
            3: 'matatu',
            4: 'mana',
            5: 'mashanu',
            6: 'matanhatu',
            7: 'manomwe',
            8: 'masere',
            9: 'mapfumbamwe'
        }
        
        # Ordinal numbers
        self.ordinals = {
            1: 'wekutanga',
            2: 'wechipiri',
            3: 'wechitatu',
            4: 'wechina',
            5: 'wechishanu',
            6: 'wechitanhatu',
            7: 'wechinomwe',
            8: 'wechisere',
            9: 'wechipfumbamwe',
            10: 'wegumi'
        }
        
        # Large number scales
        self.scale = {
            100: 'zana',
            1000: 'churu',
            1000000: 'miriyoni',
            1000000000: 'bhiriyoni',
            1000000000000: 'tiriyoni'
        }
        
        super(Num2Word_SN, self).__init__()

    def setup(self):
        super(Num2Word_SN, self).setup()
        self.negword = "minus"
        self.pointword = "poindi"

    def _int_to_sn_word(self, number):
        """Convert an integer to Shona words."""
        
        if number == 0:
            return self.ones[0]
        
        if number < 0:
            return self.negword + " " + self._int_to_sn_word(-number)
            
        if number <= 10:
            return self.ones[number]
            
        # Numbers 11-19
        if number < 20:
            return "gumi ne" + self.ones[number - 10]
            
        # Numbers 20-99
        if number < 100:
            tens, units = divmod(number, 10)
            if units == 0:
                return "makumi " + self.tens_forms[tens]
            else:
                return "makumi " + self.tens_forms[tens] + " ne" + self.ones[units]
                
        # Numbers 100-999
        if number < 1000:
            hundreds, remainder = divmod(number, 100)
            if hundreds == 1:
                if remainder == 0:
                    return "zana"
                else:
                    return "zana ne" + self._int_to_sn_word(remainder)
            else:
                if remainder == 0:
                    return "mazana " + self.tens_forms[hundreds]
                else:
                    return "mazana " + self.tens_forms[hundreds] + " ne" + self._int_to_sn_word(remainder)
                    
        # Numbers 1000-9999
        if number < 10000:
            thousands, remainder = divmod(number, 1000)
            if thousands == 1:
                if remainder == 0:
                    return "churu"
                else:
                    return "churu ne" + self._int_to_sn_word(remainder)
            else:
                if remainder == 0:
                    if thousands < 10:
                        return "zvuru zvi" + self._get_thousands_form(thousands)
                    else:
                        return "zvuru " + self._int_to_sn_word(thousands)
                else:
                    if thousands < 10:
                        return "zvuru zvi" + self._get_thousands_form(thousands) + " ne" + self._int_to_sn_word(remainder)
                    else:
                        return "zvuru " + self._int_to_sn_word(thousands) + " ne" + self._int_to_sn_word(remainder)
                        
        # Numbers 10000-99999
        if number < 100000:
            ten_thousands, remainder = divmod(number, 1000)
            if remainder == 0:
                return "zvuru " + self._int_to_sn_word(ten_thousands)
            else:
                return "zvuru " + self._int_to_sn_word(ten_thousands) + " ne" + self._int_to_sn_word(remainder)
                
        # Numbers 100000-999999
        if number < 1000000:
            hundred_thousands, remainder = divmod(number, 1000)
            if remainder == 0:
                return "zvuru " + self._int_to_sn_word(hundred_thousands)
            else:
                return "zvuru " + self._int_to_sn_word(hundred_thousands) + " ne" + self._int_to_sn_word(remainder)
                
        # Millions
        if number < 1000000000:
            millions, remainder = divmod(number, 1000000)
            if millions == 1:
                if remainder == 0:
                    return "miriyoni"
                else:
                    return "miriyoni ne" + self._int_to_sn_word(remainder)
            else:
                if remainder == 0:
                    if millions == 2:
                        return "miriyoni mbiri"
                    elif millions < 10:
                        return "miriyoni " + self.ones[millions] if millions in self.ones else "miriyoni " + self._int_to_sn_word(millions)
                    else:
                        return "miriyoni " + self._int_to_sn_word(millions)
                else:
                    if millions == 2:
                        return "miriyoni mbiri ne" + self._int_to_sn_word(remainder)
                    elif millions < 10:
                        return "miriyoni " + (self.ones[millions] if millions in self.ones else self._int_to_sn_word(millions)) + " ne" + self._int_to_sn_word(remainder)
                    else:
                        return "miriyoni " + self._int_to_sn_word(millions) + " ne" + self._int_to_sn_word(remainder)
                        
        # Billions
        if number < 1000000000000:
            billions, remainder = divmod(number, 1000000000)
            if billions == 1:
                if remainder == 0:
                    return "bhiriyoni"
                else:
                    return "bhiriyoni ne" + self._int_to_sn_word(remainder)
            else:
                if remainder == 0:
                    return "bhiriyoni " + ("mbiri" if billions == 2 else self.ones[billions] if billions < 10 else self._int_to_sn_word(billions))
                else:
                    return "bhiriyoni " + ("mbiri" if billions == 2 else self.ones[billions] if billions < 10 else self._int_to_sn_word(billions)) + " ne" + self._int_to_sn_word(remainder)
                    
        # Trillions
        trillions, remainder = divmod(number, 1000000000000)
        if trillions == 1:
            if remainder == 0:
                return "tiriyoni"
            else:
                return "tiriyoni ne" + self._int_to_sn_word(remainder)
        else:
            if remainder == 0:
                return "tiriyoni " + ("mbiri" if trillions == 2 else self.ones[trillions] if trillions < 10 else self._int_to_sn_word(trillions))
            else:
                return "tiriyoni " + ("mbiri" if trillions == 2 else self.ones[trillions] if trillions < 10 else self._int_to_sn_word(trillions)) + " ne" + self._int_to_sn_word(remainder)
    
    def _get_thousands_form(self, number):
        """Get the special form for thousands (zvuru zvi...)"""
        thousands_forms = {
            2: 'viri',
            3: 'tatu',
            4: 'na',
            5: 'shanu',
            6: 'tanhatu',
            7: 'nomwe',
            8: 'sere',
            9: 'pfumbamwe'
        }
        return thousands_forms.get(number, self.ones[number])
    
    def to_cardinal(self, number):
        """Convert a number to its cardinal representation."""
        try:
            if isinstance(number, str):
                number = int(number)
            
            # Handle floats
            if isinstance(number, float):
                return self.to_cardinal_float(number)
                
            return self._int_to_sn_word(number)
            
        except Exception:
            return self._int_to_sn_word(int(number))
    
    def to_cardinal_float(self, number):
        """Convert a float to its cardinal representation."""
        sign = ""
        if number < 0:
            sign = self.negword + " "
            number = abs(number)
            
        integer_part = int(number)
        decimal_part = str(number).split('.')[1] if '.' in str(number) else ''
        
        result = self._int_to_sn_word(integer_part)
        
        if decimal_part:
            result += " " + self.pointword
            for digit in decimal_part:
                result += " " + self.ones[int(digit)]
                
        if sign:
            return sign + result
        return result
    
    def to_ordinal(self, number):
        """Convert a number to its ordinal representation."""
        # For simple ordinals (1-10), use the direct mapping
        if number in self.ordinals:
            return self.ordinals[number]
            
        # For larger numbers, add "we" prefix to the cardinal
        cardinal = self._int_to_sn_word(number)
        
        # Handle special cases for ordinals
        if cardinal.startswith("gumi"):
            return "we" + cardinal
        elif cardinal.startswith("makumi"):
            return "we" + cardinal  # Just add "we" prefix
        elif cardinal.startswith("zana"):
            return "we" + cardinal
        elif cardinal.startswith("mazana"):
            return "we" + cardinal[2:]  # Remove "ma" prefix
        elif cardinal.startswith("churu"):
            return "we" + cardinal
        elif cardinal.startswith("zvuru"):
            return "we" + cardinal[2:]  # Remove "zv" prefix
        else:
            return "we" + cardinal
    
    def to_ordinal_num(self, number):
        """Convert a number to its abbreviated ordinal form."""
        # Shona doesn't typically use abbreviated ordinals like "1st", "2nd"
        # Return the number with a suffix indicator
        return str(number) + "."
    
    def to_currency(self, n, currency='USD', cents=True, separator='ne'):
        """Convert a number to a currency representation."""
        result = []
        value = self.float_to_value(n)
        
        if value < 0:
            result.append(self.negword)
            value = abs(value)
            
        integer_part, decimal_part = self._split_currency(value)
        
        # Get currency forms
        if currency not in self.CURRENCY_FORMS:
            raise NotImplementedError(f"Currency {currency} not implemented for Shona")
            
        currency_forms = self.CURRENCY_FORMS[currency]
        major_singular, major_plural = currency_forms[0]
        minor_singular, minor_plural = currency_forms[1]
        
        # Major currency unit
        if integer_part == 1:
            result.append(major_singular + " rimwe")
        else:
            # Use cardinal form but with "ma" prefix and appropriate forms
            cardinal = self._int_to_sn_word(integer_part)
            # Special handling for smaller numbers
            if integer_part == 2:
                result.append("ma" + major_singular + " maviri")
            elif integer_part < 10 and integer_part in self.ones:
                # Use tens_forms for consistency
                if integer_part in self.tens_forms:
                    result.append("ma" + major_singular + " " + self.tens_forms[integer_part])
                else:
                    result.append("ma" + major_singular + " " + cardinal)
            else:
                result.append("ma" + major_singular + " " + cardinal)
            
        # Minor currency unit (cents)
        if cents and decimal_part:
            if decimal_part == 1:
                result.append(separator + minor_singular + " rimwe")
            else:
                # For cents, just use the minor_singular without "ma" prefix
                result.append(separator + minor_singular + " " + self._int_to_sn_word(decimal_part))
                
        return " ".join(result)
    
    def _split_currency(self, value):
        """Split a currency value into integer and decimal parts."""
        integer_part = int(value)
        decimal_part = int(round((value - integer_part) * 100))
        return integer_part, decimal_part
    
    def to_year(self, number):
        """Convert a number to a year representation."""
        # In Shona, years are typically expressed as regular cardinal numbers
        return self._int_to_sn_word(number)
    
    def float_to_value(self, n):
        """Convert string or float to float value."""
        if isinstance(n, str):
            return float(n)
        return n