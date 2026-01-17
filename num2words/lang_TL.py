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

# Tagalog numerals
ONES = {
    0: 'wala',
    1: 'isa',
    2: 'dalawa',
    3: 'tatlo',
    4: 'apat',
    5: 'lima',
    6: 'anim',
    7: 'pito',
    8: 'walo',
    9: 'siyam'
}

TEENS = {
    10: 'sampu',
    11: 'labing-isa',
    12: 'labindalawa',
    13: 'labintatlo',
    14: 'labing-apat',
    15: 'labinlima',
    16: 'labing-anim',
    17: 'labimpito',
    18: 'labinwalo',
    19: 'labinsiyam'
}

TENS = {
    2: 'dalawampu',
    3: 'tatlumpu',
    4: 'apatnapu',
    5: 'limampu',
    6: 'animnapu',
    7: 'pitumpu',
    8: 'walumpu',
    9: 'siyamnapu'
}

HUNDREDS = {
    1: 'isandaan',
    2: 'dalawandaan',
    3: 'tatlondaan',
    4: 'apat na daan',
    5: 'lima na daan',
    6: 'anim na daan',
    7: 'pito na daan',
    8: 'walo na daan',
    9: 'siyam na daan'
}

THOUSANDS = {
    1: 'isanlibo',
    2: 'dalawanlibo',
    3: 'tatlonlibo',
    4: 'apat na libo',
    5: 'lima na libo',
    6: 'anim na libo',
    7: 'pito na libo',
    8: 'walo na libo',
    9: 'siyam na libo'
}

# Ordinal numerals
ORDINAL_ONES = {
    1: 'una',
    2: 'pangalawa',
    3: 'pangatlo',
    4: 'pang-apat',
    5: 'panlima',
    6: 'pang-anim',
    7: 'pampito',
    8: 'panwalo',
    9: 'pansiyam'
}

ORDINAL_TENS = {
    10: 'pansampu',
    20: 'pandalawampu',
    30: 'pantatlumpu',
    40: 'pang-apatnapu',
    50: 'panlimampu',
    60: 'pang-animnapu',
    70: 'panpitumpu',
    80: 'panwalumpu',
    90: 'pansiyamnapu'
}


class Num2Word_TL(Num2Word_Base):
    CURRENCY_FORMS = {
        'PHP': (('piso', 'piso'), ('sentimo', 'sentimo')),
        'USD': (('dolyar', 'dolyar'), ('sentimo', 'sentimo')),
        'EUR': (('euro', 'euro'), ('sentimo', 'sentimo')),
        'JPY': (('yen', 'yen'), ('sen', 'sen')),
        'GBP': (('pound', 'pound'), ('pence', 'pence')),
        'CNY': (('yuan', 'yuan'), ('fen', 'fen')),
    }

    def set_high_numwords(self, high):
        max = 3 + 3 * len(high)
        for word, n in zip(high, range(max, 3, -3)):
            self.cards[10 ** n] = word

    def setup(self):
        self.negword = "negatibong "
        self.pointword = "punto"
        self.exclude_title = ["at", "punto", "negatibong"]

        # Define high numwords for large numbers
        self.high_numwords = ["trilyon", "bilyon"]
        self.mid_numwords = [(1000, "libo"), (100, "daan")]
        self.low_numwords = ["labinsiyam", "labinwalo", "labimpito", "labing-anim",
                             "labinlima", "labing-apat", "labintatlo", "labindalawa",
                             "labing-isa", "sampu", "siyam", "walo", "pito", "anim",
                             "lima", "apat", "tatlo", "dalawa", "isa", "wala"]

    def merge(self, curr, next):
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            # Special handling for "isa" + large numbers
            if nnum == 1000000:
                return ("isang milyon", cnum * nnum)
            elif nnum == 1000000000:
                return ("isang bilyon", cnum * nnum)
            elif nnum == 1000:
                return ("isanlibo", cnum * nnum)
            elif nnum == 100:
                return ("isandaan", cnum * nnum)
            elif nnum < 100:
                return next

        if nnum < cnum:
            if cnum < 100:
                # For compound numbers within 99
                if cnum >= 20 and nnum < 10:
                    return (ctext + "'t " + ntext, cnum + nnum)
                else:
                    return (ctext + " " + ntext, cnum + nnum)
            else:
                # For hundreds, thousands, etc. with smaller numbers
                return (ctext + " at " + ntext, cnum + nnum)
        else:
            # For larger multipliers
            if nnum == 1000000:
                if ctext in ["dalawa", "tatlo", "apat", "lima", "anim", "pito", "walo", "siyam"]:
                    return (ctext + "ng milyon", cnum * nnum)
                elif ctext == "sampu":
                    return ("sampung milyon", cnum * nnum)
                elif ctext == "isandaan":
                    return ("isandaang milyon", cnum * nnum)
                elif ctext in ["dalawandaan", "tatlondaan"]:
                    return (ctext.replace("daan", "daang") + " milyon", cnum * nnum)
                elif "na daan" in ctext:
                    return (ctext + " milyon", cnum * nnum)
                elif "libo" in ctext:
                    return (ctext.replace("libo", "libong") + " milyon", cnum * nnum)
                else:
                    return (ctext + " milyon", cnum * nnum)
            elif nnum == 1000000000:
                if ctext in ["dalawa", "tatlo", "apat", "lima", "anim", "pito", "walo", "siyam"]:
                    return (ctext + "ng bilyon", cnum * nnum)
                else:
                    return (ctext + " bilyon", cnum * nnum)
            elif nnum == 1000:
                if ctext in ["dalawa", "tatlo", "apat", "lima", "anim", "pito", "walo", "siyam"]:
                    return (ctext + "ng libo", cnum * nnum)
                elif ctext == "sampu":
                    return ("sampung libo", cnum * nnum)
                elif ctext == "labing-isa":
                    return ("labing-isang libo", cnum * nnum)
                elif "daan" in ctext:
                    return (ctext.replace("daan", "daang") + " libo", cnum * nnum)
                else:
                    return (ctext + " libo", cnum * nnum)
            elif nnum == 100:
                if ctext in ["dalawa", "tatlo"]:
                    return (ctext + "ndaan", cnum * nnum)
                elif ctext in ["apat", "lima", "anim", "pito", "walo", "siyam"]:
                    return (ctext + " na daan", cnum * nnum)
                elif ctext == "sampu":
                    return ("sampung daan", cnum * nnum)
                else:
                    return (ctext + "daan", cnum * nnum)
            else:
                return (ctext + " " + ntext, cnum * nnum)

    def to_cardinal(self, value):
        # Handle decimal numbers first
        if isinstance(value, float) or (isinstance(value, str) and '.' in str(value)):
            return self.to_cardinal_float(value)
            
        if value == 0:
            return 'wala'

        # Handle negative numbers
        if value < 0:
            return self.negword + self.to_cardinal(abs(value))

        # Handle special cases for ones
        if 1 <= value <= 9:
            return ONES[value]

        # Handle teens
        if 10 <= value <= 19:
            return TEENS[value]

        # Handle tens
        if 20 <= value <= 99:
            tens_digit = value // 10
            ones_digit = value % 10
            if ones_digit == 0:
                return TENS[tens_digit]
            else:
                return TENS[tens_digit] + "'t " + ONES[ones_digit]

        # Handle hundreds
        if 100 <= value <= 999:
            hundreds_digit = value // 100
            remainder = value % 100
            hundreds_text = HUNDREDS[hundreds_digit]
            if remainder == 0:
                return hundreds_text
            else:
                return hundreds_text + " at " + self.to_cardinal(remainder)

        # Handle thousands
        if 1000 <= value <= 999999:
            thousands = value // 1000
            remainder = value % 1000

            if thousands == 1:
                thousands_text = "isanlibo"
            elif thousands <= 9:
                thousands_text = THOUSANDS[thousands]
            elif thousands == 10:
                thousands_text = "sampung libo"
            elif 11 <= thousands <= 19:
                if thousands == 11:
                    thousands_text = "labing-isang libo"
                else:
                    thousands_text = TEENS[thousands] + " libo"
            elif 20 <= thousands <= 99:
                thousands_cardinal = self.to_cardinal(thousands)
                if thousands_cardinal.endswith("mpu"):
                    # Handle special case like "dalawampu" -> "dalawampung libo"
                    thousands_text = thousands_cardinal + "ng libo"
                elif (thousands_cardinal.endswith("'t apat") or thousands_cardinal.endswith("apat") or 
                      "'t siyam" in thousands_cardinal or thousands_cardinal.endswith("siyam") or
                      thousands_cardinal.endswith("'t lima") or thousands_cardinal.endswith("lima") or
                      thousands_cardinal.endswith("'t tatlo") or thousands_cardinal.endswith("tatlo")):
                    # Handle special case for numbers ending with certain digits that need "na libo"
                    if thousands_cardinal.endswith("'t lima"):
                        thousands_text = thousands_cardinal.replace("'t lima", "'t limang") + " libo"
                    elif thousands_cardinal == "lima":
                        thousands_text = "limang libo"
                    elif thousands_cardinal.endswith("'t tatlo"):
                        thousands_text = thousands_cardinal.replace("'t tatlo", "'t tatlong") + " libo"
                    elif thousands_cardinal == "tatlo":
                        thousands_text = "tatlong libo"
                    else:
                        thousands_text = thousands_cardinal + " na libo"
                else:
                    thousands_text = thousands_cardinal + " libo"
            else:
                # 100-999 thousands
                hundreds_part = thousands // 100
                tens_units_part = thousands % 100
                if tens_units_part == 0:
                    if hundreds_part <= 3:
                        thousands_text = HUNDREDS[hundreds_part].replace("daan", "daang") + " libo"
                    else:
                        thousands_text = HUNDREDS[hundreds_part] + " libo"
                else:
                    thousands_cardinal = self.to_cardinal(thousands)
                    # Apply same logic for compound thousands
                    if (thousands_cardinal.endswith("'t apat") or 
                        "'t siyam" in thousands_cardinal or
                        thousands_cardinal.endswith("'t lima") or
                        thousands_cardinal.endswith("'t tatlo")):
                        if thousands_cardinal.endswith("'t lima"):
                            thousands_text = thousands_cardinal + " na libo"
                        elif thousands_cardinal.endswith("'t tatlo"):
                            thousands_text = thousands_cardinal.replace("'t tatlo", "'t tatlong") + " libo"
                        else:
                            thousands_text = thousands_cardinal + " na libo"
                    else:
                        thousands_text = thousands_cardinal + " libo"

            if remainder == 0:
                return thousands_text
            else:
                return thousands_text + " at " + self.to_cardinal(remainder)

        # Handle millions
        if 1000000 <= value <= 999999999:
            millions = value // 1000000
            remainder = value % 1000000

            if millions == 1:
                millions_text = "isang milyon"
            elif millions in [2, 3, 4, 5, 6, 7, 8, 9]:
                millions_text = ONES[millions] + "ng milyon"
            elif millions == 10:
                millions_text = "sampung milyon"
            elif millions == 100:
                millions_text = "isandaang milyon"
            else:
                millions_cardinal = self.to_cardinal(millions)
                if millions_cardinal in ["dalawa", "tatlo", "apat", "lima", "anim", "pito", "walo", "siyam"]:
                    millions_text = millions_cardinal + "ng milyon"
                elif millions_cardinal == "sampu":
                    millions_text = "sampung milyon"
                elif millions_cardinal == "isandaan":
                    millions_text = "isandaang milyon"
                elif millions_cardinal == "labindalawa":
                    millions_text = "labindalawang milyon"
                elif "na daan" in millions_cardinal or "'t siyam" in millions_cardinal:
                    millions_text = millions_cardinal + " na milyon"
                else:
                    millions_text = millions_cardinal + " milyon"

            if remainder == 0:
                return millions_text
            else:
                return millions_text + " at " + self.to_cardinal(remainder)

        # Handle billions
        if 1000000000 <= value <= 999999999999:
            billions = value // 1000000000
            remainder = value % 1000000000

            if billions == 1:
                billions_text = "isang bilyon"
            else:
                billions_text = self.to_cardinal(billions) + "ng bilyon"

            if remainder == 0:
                return billions_text
            else:
                return billions_text + " at " + self.to_cardinal(remainder)

        # For larger numbers, use the standard implementation
        return super(Num2Word_TL, self).to_cardinal(value)

    def to_ordinal(self, value):
        if value <= 0:
            raise ValueError("Ordinal numbers must be positive")

        # Handle special cases for small ordinals
        if 1 <= value <= 9:
            return ORDINAL_ONES[value]

        if value == 10:
            return "pansampu"
        elif 11 <= value <= 19:
            return "pang-" + TEENS[value]
        elif value in ORDINAL_TENS:
            return ORDINAL_TENS[value]
        elif 20 <= value <= 99:
            tens_digit = value // 10
            ones_digit = value % 10
            if ones_digit == 0:
                return ORDINAL_TENS[tens_digit * 10]
            else:
                return "pang-" + self.to_cardinal(value)

        # For larger numbers, add "pang-" prefix
        return "pang-" + self.to_cardinal(value)

    def to_ordinal_num(self, value):
        if value <= 0:
            raise ValueError("Ordinal numbers must be positive")

        # English-style ordinal suffixes for numerical representation
        if value % 100 in [11, 12, 13]:
            suffix = "th"
        elif value % 10 == 1:
            suffix = "st"
        elif value % 10 == 2:
            suffix = "nd"
        elif value % 10 == 3:
            suffix = "rd"
        else:
            suffix = "th"

        return str(value) + suffix

    def pluralize(self, n, forms):
        # Tagalog doesn't have complex plural rules like other languages
        # Generally, the same form is used for both singular and plural
        if forms:
            return forms[0]
        return ''

    def to_currency(self, val, currency='PHP', cents=True, separator=','):
        """
        Convert a value to Tagalog currency.
        """
        result = []
        is_negative = val < 0
        val = abs(val)

        if currency in self.CURRENCY_FORMS:
            if cents:
                # Convert to cents and split
                cents_total = int(round(val * 100))
                whole, cents_part = divmod(cents_total, 100)
            else:
                whole, cents_part = int(val), 0

            # Main currency part
            if whole:
                if whole == 1:
                    if currency == 'PHP':
                        result.append("isang piso")
                    elif currency == 'USD':
                        result.append("isang dolyar")
                    else:
                        result.append("isang " + self.CURRENCY_FORMS[currency][0][0])
                else:
                    cardinal_whole = self.to_cardinal(whole)
                    # Handle the Tagalog linker "ng" for currency
                    if currency == 'PHP':
                        if cardinal_whole in ['dalawa', 'tatlo', 'apat', 'lima', 'anim', 'pito', 'walo', 'siyam']:
                            result.append(cardinal_whole + "ng piso")
                        elif cardinal_whole == 'sampu':
                            result.append("sampung piso")
                        elif cardinal_whole == 'isandaan':
                            result.append("isandaang piso")
                        else:
                            result.append(cardinal_whole + " piso")
                    elif currency == 'USD':
                        if cardinal_whole in ['dalawa', 'tatlo', 'apat', 'lima', 'anim', 'pito', 'walo', 'siyam']:
                            result.append(cardinal_whole + "ng dolyar")
                        elif cardinal_whole == 'sampu':
                            result.append("sampung dolyar")
                        elif cardinal_whole == 'isandaan':
                            result.append("isandaang dolyar")
                        else:
                            result.append(cardinal_whole + " dolyar")
                    else:
                        result.append(cardinal_whole + " " + self.CURRENCY_FORMS[currency][0][0])

            # Cents part
            if cents_part:
                if whole:
                    result.append("at")
                if cents_part == 1:
                    result.append("isang sentimo")
                else:
                    cardinal_cents = self.to_cardinal(cents_part)
                    # Handle Tagalog linker for cents
                    if cardinal_cents in ['dalawa', 'tatlo', 'apat', 'lima', 'anim', 'pito', 'walo', 'siyam']:
                        result.append(cardinal_cents + "ng sentimo")
                    elif cardinal_cents == 'limampu':
                        result.append("limampung sentimo")
                    elif cardinal_cents == 'sampu':
                        result.append("sampung sentimo")
                    elif cardinal_cents.endswith("'t lima"):
                        result.append(cardinal_cents.replace("'t lima", "'t limang") + " sentimo")
                    else:
                        result.append(cardinal_cents + " sentimo")

            if is_negative:
                result.insert(0, self.negword.strip())

            return ' '.join(result)
        else:
            return self.to_cardinal(val)

    def to_year(self, val, longval=True):
        """Convert number to year in Tagalog."""
        return self.to_cardinal(val)

    def float2tuple(self, value):
        """Override to handle decimal conversion for Tagalog."""
        pre = int(value)
        
        # Get decimal places
        decimal_str = str(value).split('.')
        if len(decimal_str) > 1:
            post_str = decimal_str[1]
            self.precision = len(post_str)
            post = int(post_str)
        else:
            self.precision = 0
            post = 0

        return pre, post

    def to_cardinal_float(self, value):
        """Handle decimal numbers in Tagalog."""
        try:
            float(value) == value
        except (ValueError, TypeError, AssertionError, AttributeError):
            raise TypeError("Invalid number type")

        pre, post = self.float2tuple(float(value))

        # Handle negative numbers
        is_negative = value < 0
        if is_negative:
            pre = abs(pre)
            value = abs(value)

        out = []
        
        if is_negative:
            out.append(self.negword.strip())

        # Add the whole part
        out.append(self.to_cardinal(pre))
        
        # Add decimal point
        out.append(self.pointword)
        
        # Add decimal digits
        if self.precision > 0:
            out.append(self.to_cardinal(post))

        return " ".join(out)