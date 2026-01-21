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

# Genders
KK = 0  # Karlkyn (male)
KVK = 1  # Kvenkyn (female)
HK = 2  # Hvorugkyn (neuter)

GENDERS = {
    "einn": ("einn", "ein", "eitt"),
    "tveir": ("tveir", "tvær", "tvö"),
    "þrír": ("þrír", "þrjár", "þrjú"),
    "fjórir": ("fjórir", "fjórar", "fjögur"),
}

PLURALS = {
    "hundrað": ("hundrað", "hundruð"),
}


class Num2Word_IS(lang_EUR.Num2Word_EUR):

    CURRENCY_FORMS = {
        'ISK': (('króna', 'krónur'), ('eyrir', 'aurar')),
        'EUR': (('evra', 'evrur'), ('sent', 'sent')),
        'USD': (('dalur', 'dalir'), ('sent', 'sent')),
    }

    GIGA_SUFFIX = "illjarður"
    MEGA_SUFFIX = "illjón"

    def setup(self):
        lows = ["okt", "sept", "sext", "kvint", "kvaðr", "tr", "b", "m"]
        self.high_numwords = self.gen_high_numwords([], [], lows)

        self.negword = "mínus "
        self.pointword = "komma"

        # All words should be excluded, title case is not used in Icelandic
        self.exclude_title = ["og", "komma", "mínus"]

        self.mid_numwords = [(1000, "þúsund"), (100, "hundrað"),
                             (90, "níutíu"), (80, "áttatíu"), (70, "sjötíu"),
                             (60, "sextíu"), (50, "fimmtíu"), (40, "fjörutíu"),
                             (30, "þrjátíu")]
        self.low_numwords = ["tuttugu", "nítján", "átján", "sautján",
                             "sextán", "fimmtán", "fjórtán", "þrettán",
                             "tólf", "ellefu", "tíu", "níu", "átta",
                             "sjö", "sex", "fimm", "fjórir", "þrír",
                             "tveir", "einn", "núll"]
        self.ords = {"einn": "fyrsti",
                     "tveir": "annar",
                     "þrír": "þriðji",
                     "fjórir": "fjórði",
                     "fimm": "fimmti",
                     "sex": "sjötti",
                     "sjö": "sjöundi",
                     "átta": "áttundi",
                     "níu": "níundi",
                     "tíu": "tíundi",
                     "ellefu": "ellefti",
                     "tólf": "tólfti"}

    def pluralize(self, n, noun):
        form = 0 if (n % 10 == 1 and n % 100 != 11) else 1
        if form == 0:
            return noun
        elif self.GIGA_SUFFIX in noun:
            return noun.replace(self.GIGA_SUFFIX, "illjarðar")
        elif self.MEGA_SUFFIX in noun:
            return noun.replace(self.MEGA_SUFFIX, "illjónir")
        elif noun not in PLURALS:
            return noun
        return PLURALS[noun][form]

    def genderize(self, adj, noun):
        last = adj.split()[-1]
        if last not in GENDERS:
            return adj
        gender = KK
        if "hund" in noun or "þús" in noun:
            gender = HK
        elif "illjarð" in noun:
            gender = KK
        elif "illjón" in noun:
            gender = KVK
        return adj.replace(last, GENDERS[last][gender])

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair

        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
        elif lnum < rnum:
            rtext = self.pluralize(lnum, rtext)
            ltext = self.genderize(ltext, rtext)
            return ("%s %s" % (ltext, rtext), lnum * rnum)
        elif lnum > rnum and rnum in self.cards:
            rtext = self.pluralize(lnum, rtext)
            ltext = self.genderize(ltext, rtext)
            return ("%s og %s" % (ltext, rtext), lnum + rnum)
        return ("%s %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal(self, value):
        # Use the ordinal dictionary defined in setup
        try:
            number = int(value)
        except (ValueError, TypeError):
            return str(value)

        # Get cardinal form first
        cardinal = self.to_cardinal(number)

        # Check if we have a direct mapping
        if cardinal in self.ords:
            return self.ords[cardinal]

        # For numbers beyond our mapping, use generic suffix
        # In Icelandic, ordinals typically end with -asti, -undi, etc.
        if number == 20:
            return "tuttugasti"
        elif 20 < number < 30:
            return "tuttugasti og " + self.ords.get(self.to_cardinal(number % 10), self.to_cardinal(number % 10))
        elif number == 30:
            return "þrítugasti"
        elif number == 40:
            return "fertugasti"
        elif number == 50:
            return "fimmtugasti"
        elif number == 60:
            return "sextugasti"
        elif number == 70:
            return "sjötugasti"
        elif number == 80:
            return "áttugasti"
        elif number == 90:
            return "nítugasti"
        elif number == 100:
            return "hundraðasti"
        elif number == 1000:
            return "þúsundasti"
        else:
            # For composite numbers, just append 'asti' to the cardinal
            # This is a simplified implementation
            return cardinal + "asti"

    def to_ordinal_num(self, value):
        # Just add a period after the number for ordinal numbers in Icelandic
        return str(value) + "."

    def to_year(self, val, suffix=None, longval=True):
        # For Icelandic, years are typically read as cardinal numbers
        # For example: 2024 would be "tvö þúsund tuttugu og fjórir"
        return self.to_cardinal(val)

    def pluralize_currency(self, count, forms):
        """Return the proper plural form for Icelandic currency"""
        if count == 1:
            return forms[0]
        return forms[1] if len(forms) > 1 else forms[0]

    def to_currency(self, val, currency='ISK', cents=True, separator=',',
                    adjective=False):
        # Handle integers specially - just add currency name without cents
        if isinstance(val, int):
            try:
                cr1, cr2 = self.CURRENCY_FORMS[currency]
            except (KeyError, AttributeError):
                # Fallback to base implementation for unknown currency
                return super(Num2Word_IS, self).to_currency(
                    val, currency=currency, cents=cents, separator=separator,
                    adjective=adjective)

            minus_str = self.negword if val < 0 else ""
            abs_val = abs(val)
            money_str = self.to_cardinal(abs_val)

            # Proper pluralization for currency
            if abs_val == 1:
                currency_str = cr1[0] if isinstance(cr1, tuple) else cr1
            else:
                currency_str = cr1[1] if isinstance(cr1, tuple) and len(cr1) > 1 else (cr1[0] if isinstance(cr1, tuple) else cr1)

            return (u'%s %s %s' % (minus_str, money_str, currency_str)).strip()

        # For floats, use the parent class implementation
        return super(Num2Word_IS, self).to_currency(
            val, currency=currency, cents=cents, separator=separator,
            adjective=adjective)
