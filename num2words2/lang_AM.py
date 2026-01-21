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

from __future__ import division, print_function, unicode_literals

from . import lang_EUR


class Num2Word_AM(lang_EUR.Num2Word_EUR):
    CURRENCY_FORMS = {'ETB': (('ብር', 'ብር'), ('ሳንቲም', 'ሳንቲም'), ' ከ'),
                      'USD': (('ዶላር', 'ዶላር'), ('ሳንቲም', 'ሳንቲም'), ' ከ'),
                      'JPY': (('የን', 'የን'), ('ሴን', 'ሴን'), ' ከ')}

    GIGA_SUFFIX = 'ቢሊዮን'
    MEGA_SUFFIX = 'ሚሊዮን'

    def set_high_numwords(self, high):
        cap = 3 * (len(high) + 1)

        for word, n in zip(high, range(cap, 5, -3)):
            if n == 9:
                self.cards[10 ** n] = word + self.GIGA_SUFFIX
            else:
                self.cards[10 ** n] = word + self.MEGA_SUFFIX

    def setup(self):
        super(Num2Word_AM, self).setup()

        self.negword = 'ሰልቢ '
        self.pointword = 'ነጥብ'
        self.exclude_title = ['እና', 'ነጥብ', 'አሉታዊ']

        self.mid_numwords = [(1000, 'ሺህ'), (100, 'መቶ'), (90, 'ዘጠና'),
                             (80, 'ሰማንያ'), (70, 'ሰባ'), (60, 'ስድሳ'),
                             (50, 'አምሳ'), (40, 'አርባ'), (30, 'ሠላሳ')]
        self.low_numwords = ['ሃያ', 'አሥራ ዘጠኝ', 'አሥራ ስምንት', 'አሥራ ሰባት',
                             'አስራ ስድስት', 'አሥራ አምስት', 'አሥራ አራት', 'አሥራ ሦስት',
                             'አሥራ ሁለት', 'አሥራ አንድ', 'አሥር', 'ዘጠኝ', 'ስምንት',
                             'ሰባት', 'ስድስት', 'አምስት', 'አራት', 'ሦስት', 'ሁለት',
                             'አንድ', 'ዜሮ']
        self.ords = {'አንድ': 'አንደኛ',
                     'ሁለት': 'ሁለተኛ',
                     'ሦስት': 'ሦስተኛ',
                     'አራት': 'አራተኛ',
                     'አምስት': 'አምስተኛ',
                     'ስድስት': 'ስድስተኛ',
                     'ሰባት': 'ሰባተኛ',
                     'ስምንት': 'ስምንተኛ',
                     'ዘጠኝ': 'ዘጠነኛ',
                     'አሥር': 'አሥረኛ',
                     'አሥራ አንድ': 'አሥራ አንደኛ',
                     'አሥራ ሁለት': 'አሥራ ሁለተኛ',
                     'አሥራ ሦስት': 'አሥራ ሦስተኛ',
                     'አሥራ አራት': 'አሥራ አራተኛ',
                     'አሥራ አምስት': 'አሥራ አምስተኛ',
                     'አሥራ ስድስት': 'አሥራ ስድስተኛ',
                     'አሥራ ሰባት': 'አሥራ ሰባተኛ',
                     'አሥራ ስምንት': 'አሥራ ስምንተኛ',
                     'አሥራ ዘጠኝ': 'አሥራ ዘጠነኛ'}

    def to_cardinal(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)

        # Handle negative integers
        if value < 0:
            return self.negword + self.to_cardinal(-value)

        out = ''
        if value >= self.MAXVAL:
            raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))

        if value == 100:
            return self.title(out + 'መቶ')
        else:
            val = self.splitnum(value)
            words, num = self.clean(val)
            return self.title(out + words)

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return rtext, rnum
        elif 100 > lnum > rnum:
            return '%s %s' % (ltext, rtext), lnum + rnum
        elif lnum >= 100 > rnum:
            return '%s %s' % (ltext, rtext), lnum + rnum
        elif rnum > lnum:
            return '%s %s' % (ltext, rtext), lnum * rnum
        else:
            # Default case: lnum > rnum, both could be >= 100
            return '%s %s' % (ltext, rtext), lnum + rnum

    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(' ')
        lastwords = outwords[-1].split('-')
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            lastword += 'ኛ'
        lastwords[-1] = self.title(lastword)
        outwords[-1] = ' '.join(lastwords)
        return ' '.join(outwords)

    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return '%s%s' % (value, self.to_ordinal(value)[-1:])

    def to_currency(self, val, currency='ETB', cents=True, separator=',',
                    adjective=False):
        # Track if input was originally an integer
        is_integer_input = isinstance(val, int)

        if is_integer_input:
            left = abs(val)
            right = 0
            is_negative = val < 0
        else:
            from decimal import Decimal

            from .currency import parse_currency_parts

            # Check if value has fractional cents
            decimal_val = Decimal(str(val))
            has_fractional_cents = (decimal_val * 100) % 1 != 0

            left, right, is_negative = parse_currency_parts(val, is_int_with_cents=False,
                                                            keep_precision=has_fractional_cents)

        try:
            cr1, cr2, default_separator = self.CURRENCY_FORMS[currency]
            if separator == ',':  # Use default separator if not overridden
                separator = default_separator
        except KeyError:
            raise NotImplementedError(
                'Currency code "%s" not implemented for "%s"' %
                (currency, self.__class__.__name__))

        minus_str = "%s " % self.negword.strip() if is_negative else ""
        money_str = self.to_cardinal(left)

        # For floats, always show cents (even if zero)
        # For integers, don't show cents at all
        if not is_integer_input:
            if cents:
                # Handle fractional cents
                from decimal import Decimal
                if isinstance(right, Decimal):
                    # Convert fractional cents (e.g., 65.3 cents)
                    cents_str = self.to_cardinal_float(float(right)) if right > 0 else 'ዜሮ'
                else:
                    cents_str = self.to_cardinal(right) if right > 0 else 'ዜሮ'
            else:
                cents_str = str(float(right) if isinstance(right, Decimal) else right)
            return u'%s%s %s%s %s %s' % (
                minus_str,
                money_str,
                self.pluralize(left, cr1),
                separator,
                cents_str,
                self.pluralize(right, cr2)
            )
        else:
            # Integer: no cents
            return u'%s%s %s' % (
                minus_str,
                money_str,
                self.pluralize(left, cr1)
            )

    def to_year(self, val, longval=True):
        if not (val // 100) % 10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt='መቶ', longval=longval)
