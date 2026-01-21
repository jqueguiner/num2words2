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

to_19 = (u'không', u'một', u'hai', u'ba', u'bốn', u'năm', u'sáu',
         u'bảy', u'tám', u'chín', u'mười', u'mười một', u'mười hai',
         u'mười ba', u'mười bốn', u'mười lăm', u'mười sáu', u'mười bảy',
         u'mười tám', u'mười chín')
tens = (u'hai mươi', u'ba mươi', u'bốn mươi', u'năm mươi',
        u'sáu mươi', u'bảy mươi', u'tám mươi', u'chín mươi')
denom = ('',
         u'nghìn', u'triệu', u'tỷ', u'nghìn tỷ', u'trăm nghìn tỷ',
         'Quintillion', 'Sextillion', 'Septillion', 'Octillion', 'Nonillion',
         'Decillion', 'Undecillion', 'Duodecillion', 'Tredecillion',
         'Quattuordecillion', 'Sexdecillion', 'Septendecillion',
         'Octodecillion', 'Novemdecillion', 'Vigintillion')


class Num2Word_VI(object):

    def _convert_nn(self, val):
        if val < 20:
            return to_19[val]
        for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
            if dval + 10 > val:
                if val % 10:
                    a = u'lăm'
                    if to_19[val % 10] == u'một':
                        a = u'mốt'
                    else:
                        a = to_19[val % 10]
                    if to_19[val % 10] == u'năm':
                        a = u'lăm'
                    return dcap + ' ' + a
                return dcap

    def _convert_nnn(self, val):
        word = ''
        (mod, rem) = (val % 100, val // 100)
        if rem > 0:
            word = to_19[rem] + u' trăm'
            if mod > 0:
                word = word + ' '
        if mod > 0 and mod < 10:
            if mod == 5:
                word = word != '' and word + u'lẻ năm' or word + u'năm'
            else:
                word = word != '' and word + u'lẻ ' \
                    + self._convert_nn(mod) or word + self._convert_nn(mod)
        if mod >= 10:
            word = word + self._convert_nn(mod)
        return word

    def vietnam_number(self, val):
        if val < 100:
            return self._convert_nn(val)
        if val < 1000:
            return self._convert_nnn(val)
        for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
            if dval > val:
                mod = 1000 ** didx
                lval = val // mod
                r = val - (lval * mod)

                ret = self._convert_nnn(lval) + u' ' + denom[didx]
                if 99 >= r > 0:
                    ret = self._convert_nnn(lval) + u' ' + denom[didx] + u' lẻ'
                if r > 0:
                    ret = ret + ' ' + self.vietnam_number(r)
                return ret

    def number_to_text(self, number):
        is_negative = number < 0
        number = abs(number)
        number = '%.2f' % number
        the_list = str(number).split('.')
        start_word = self.vietnam_number(int(the_list[0]))
        final_result = start_word
        if len(the_list) > 1 and int(the_list[1]) > 0:
            end_word = self.vietnam_number(int(the_list[1]))
            final_result = final_result + ' phẩy ' + end_word
        if is_negative:
            final_result = 'âm ' + final_result
        return final_result

    def to_cardinal(self, number):
        return self.number_to_text(number)

    def to_ordinal(self, number):
        return self.to_cardinal(number)

    def to_ordinal_num(self, number):
        """Convert to abbreviated ordinal form in Vietnamese"""
        # Vietnamese typically uses "thứ" + number for ordinals
        return "thứ " + str(number)

    def to_year(self, val, longval=True):
        """Convert number to year representation in Vietnamese"""
        if val < 0:
            # BC years (trước Công nguyên)
            return "năm " + self.to_cardinal(-val) + " trước Công nguyên"
        else:
            # AD years (just "năm" + number)
            return "năm " + self.to_cardinal(val)

    def to_currency(self, val, currency='VND', cents=True, separator=',',
                    adjective=False):
        """
        Convert amount to currency format
        """
        from decimal import Decimal

        # Check if value has fractional cents
        decimal_val = Decimal(str(val))
        has_fractional_cents = (decimal_val * 100) % 1 != 0

        # If input is an integer, just return the cardinal number
        if isinstance(val, int):
            return self.to_cardinal(val) + " đồng"

        # For floats with fractional cents
        if has_fractional_cents:
            # Vietnamese doesn't typically use cents, but for consistency
            # we'll handle fractional amounts
            return self.to_cardinal_float(val) + " đồng"

        # For floats, use the full currency format with dong
        return self.to_cardinal(val) + " đồng"
