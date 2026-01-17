# -*- encoding: utf-8 -*-
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

from num2words.base import Num2Word_Base


class Num2Word_ML(Num2Word_Base):
    """
    Malayalam (ML) Num2Word class
    """

    def setup(self):
        # Numbers 0-99 in reverse order (99 down to 0)
        self.low_numwords = [
            "തൊണ്ണൂറ്റൊമ്പത്",      # 99
            "തൊണ്ണൂറ്റിയെട്ട്",       # 98
            "തൊണ്ണൂറ്റിയേഴ്",        # 97
            "തൊണ്ണൂറ്റിയാറ്",        # 96
            "തൊണ്ണൂറ്റിയഞ്ച്",       # 95
            "തൊണ്ണൂറ്റിനാല്",        # 94
            "തൊണ്ണൂറ്റിയമൂന്ന്",      # 93
            "തൊണ്ണൂറ്റിരണ്ട്",        # 92
            "തൊണ്ണൂറ്റൊന്ന്",         # 91
            "തൊണ്ണൂറ്",              # 90
            "എണ്പത്തൊമ്പത്",         # 89
            "എണ്പത്തിയെട്ട്",        # 88
            "എണ്പത്തിയേഴ്",         # 87
            "എണ്പത്തിയാറ്",         # 86
            "എണ്പത്തിയഞ്ച്",        # 85
            "എണ്പത്തിനാല്",         # 84
            "എണ്പത്തിയമൂന്ന്",       # 83
            "എണ്പത്തിരണ്ട്",         # 82
            "എണ്പത്തിയൊന്ന്",        # 81
            "എണ്പത്",               # 80
            "എഴുപത്തൊമ്പത്",         # 79
            "എഴുപത്തിയെട്ട്",        # 78
            "എഴുപത്തിയേഴ്",         # 77
            "എഴുപത്തിയാറ്",         # 76
            "എഴുപത്തിയഞ്ച്",        # 75
            "എഴുപത്തിനാല്",         # 74
            "എഴുപത്തിയമൂന്ന്",       # 73
            "എഴുപത്തിരണ്ട്",         # 72
            "എഴുപത്തിയൊന്ന്",        # 71
            "എഴുപത്",               # 70
            "അറുപത്തൊമ്പത്",         # 69
            "അറുപത്തിയെട്ട്",        # 68
            "അറുപത്തിയേഴ്",         # 67
            "അറുപത്തിയാറ്",         # 66
            "അറുപത്തിയഞ്ച്",        # 65
            "അറുപത്തിനാല്",         # 64
            "അറുപത്തിയമൂന്ന്",       # 63
            "അറുപത്തിരണ്ട്",         # 62
            "അറുപത്തിയൊന്ന്",        # 61
            "അറുപത്",               # 60
            "അന്പത്തൊമ്പത്",         # 59
            "അന്പത്തിയെട്ട്",        # 58
            "അന്പത്തിയേഴ്",         # 57
            "അന്പത്തിയാറ്",         # 56
            "അന്പത്തിയഞ്ച്",        # 55
            "അന്പത്തിനാല്",         # 54
            "അന്പത്തിയമൂന്ന്",       # 53
            "അന്പത്തിരണ്ട്",         # 52
            "അന്പത്തിയൊന്ന്",        # 51
            "അന്പത്",               # 50
            "നാല്പത്തൊമ്പത്",        # 49
            "നാല്പത്തിയെട്ട്",       # 48
            "നാല്പത്തിയേഴ്",        # 47
            "നാല്പത്തിയാറ്",        # 46
            "നാല്പത്തിയഞ്ച്",       # 45
            "നാല്പത്തിനാല്",        # 44
            "നാല്പത്തിയമൂന്ന്",      # 43
            "നാല്പത്തിരണ്ട്",        # 42
            "നാല്പത്തിയൊന്ന്",       # 41
            "നാല്പത്",              # 40
            "മുപ്പത്തൊമ്പത്",        # 39
            "മുപ്പത്തിയെട്ട്",       # 38
            "മുപ്പത്തിയേഴ്",        # 37
            "മുപ്പത്തിയാറ്",        # 36
            "മുപ്പത്തിയഞ്ച്",       # 35
            "മുപ്പത്തിനാല്",        # 34
            "മുപ്പത്തിയമൂന്ന്",      # 33
            "മുപ്പത്തിരണ്ട്",        # 32
            "മുപ്പത്തിയൊന്ന്",       # 31
            "മുപ്പത്",              # 30
            "ഇരുപത്തൊമ്പത്",        # 29
            "ഇരുപത്തിയെട്ട്",       # 28
            "ഇരുപത്തിയേഴ്",        # 27
            "ഇരുപത്തിയാറ്",        # 26
            "ഇരുപത്തിയഞ്ച്",       # 25
            "ഇരുപത്തിനാല്",        # 24
            "ഇരുപത്തിയമൂന്ന്",      # 23
            "ഇരുപത്തിരണ്ട്",        # 22
            "ഇരുപത്തിയൊന്ന്",       # 21
            "ഇരുപത്",              # 20
            "പത്തൊമ്പത്",           # 19
            "പതിനെട്ട്",            # 18
            "പതിനേഴ്",             # 17
            "പതിനാറ്",             # 16
            "പതിനഞ്ച്",            # 15
            "പതിനാല്",             # 14
            "പതിമൂന്ന്",            # 13
            "പന്ത്രണ്ട്",           # 12
            "പതിനൊന്ന്",           # 11
            "പത്ത്",               # 10
            "ഒമ്പത്",              # 9
            "എട്ട്",               # 8
            "ഏഴ്",                # 7
            "ആറ്",                # 6
            "അഞ്ച്",              # 5
            "നാല്",               # 4
            "മൂന്ന്",              # 3
            "രണ്ട്",              # 2
            "ഒന്ന്",              # 1
            "പൂജ്യം",             # 0
        ]

        # Hundreds
        self.mid_numwords = [(100, "നൂറ്")]

        # Thousands, lakhs, crores (Indian numbering system)
        self.high_numwords = [
            (7, "കോടി"),      # 10,000,000 (crore)
            (5, "ലക്ഷം"),     # 100,000 (lakh)
            (3, "ആയിരം"),    # 1,000 (thousand)
        ]

        self.pointword = "പോയിന്റ്"
        self.negword = "മൈനസ് "

        # Special hundreds forms (2-9 * 100)
        self.hundreds_forms = {
            200: "ഇരുനൂറ്",
            300: "മുന്നൂറ്",
            400: "നാന്നൂറ്",
            500: "അഞ്ഞൂറ്",
            600: "ആറുനൂറ്",
            700: "ഏഴുനൂറ്",
            800: "എട്ടുനൂറ്",
            900: "ഒമ്പതുനൂറ്",
        }

    def set_high_numwords(self, high):
        for n, word in self.high_numwords:
            self.cards[10**n] = word

    def merge(self, lpair, rpair):
        ltext, lnum = lpair
        rtext, rnum = rpair
        
        # Handle special case of 1 + anything less than 100
        if lnum == 1 and rnum < 100:
            return (rtext, rnum)
            
        # Handle hundreds with addition (e.g., 100 + 1 = 101) 
        elif lnum >= 100 and lnum < 1000 and rnum < 100:
            # Special handling for hundreds + units (only for actual hundreds)
            if ltext.endswith("നൂറ്"):
                # Transform "നൂറ്" to "നൂറ്റി" pattern for connection
                base = ltext.replace("നൂറ്", "നൂറ്റി")
                if rtext.startswith("ഒ"):  # If number starts with "ഒ" use "യൊ" connector
                    combined_text = base + "യൊ" + rtext[1:]
                elif rtext.startswith("അ"):  # If number starts with "അ" use "യ" connector 
                    combined_text = base + "യ" + rtext[1:]
                else:
                    combined_text = base + rtext
            else:
                combined_text = "%s %s" % (ltext, rtext)
            return (combined_text, lnum + rnum)
            
        # Handle multiplication (e.g., 2 * 100 = 200)
        elif rnum > lnum:
            # Handle special hundreds forms (200, 300, etc.)
            if rnum == 100 and (lnum * rnum) in self.hundreds_forms:
                return (self.hundreds_forms[lnum * rnum], lnum * rnum)
            
            # Handle thousands, lakhs, crores
            if rnum == 1000:  # thousands
                if lnum == 1:
                    return ("ഒരായിരം", lnum * rnum)  # Fixed form for "one thousand"
                else:
                    # Handle connection between number and "ആയിരം"
                    if ltext.endswith("്"):
                        combined_text = ltext[:-1] + "ായിരം"
                    else:
                        combined_text = ltext + "ആയിരം"
                    return (combined_text, lnum * rnum)
            elif rnum == 100000:  # lakhs
                if lnum == 1:
                    return ("ഒരു%s" % rtext, lnum * rnum)
                else:
                    return ("%sു%s" % (ltext, rtext), lnum * rnum)
            elif rnum == 10000000:  # crores
                if lnum == 1:
                    return ("ഒരു%s" % rtext, lnum * rnum)
                else:
                    return ("%sു%s" % (ltext, rtext), lnum * rnum)
            elif rnum == 100:
                if lnum == 1:
                    return ("ഒരു %s" % rtext, lnum * rnum)
                else:
                    return ("%s %s" % (ltext, rtext), lnum * rnum)
            else:
                return ("%s %s" % (ltext, rtext), lnum * rnum)
        
        # Handle addition for larger numbers 
        elif lnum >= 10000000:  # crores
            return ("%s%s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 100000:  # lakhs  
            return ("%sത്തി%s" % (ltext, rtext), lnum + rnum)
        elif lnum >= 1000:  # thousands
            # Special connector logic for thousands + units
            if ltext.endswith("ം"):  # If thousands end with "ം", replace with "ത്തി"
                base = ltext[:-1] + "ത്തി"
                if rtext.startswith("ഒ") and " " not in rtext:  # For simple numbers starting with "ഒ"
                    return ("%sയൊ%s" % (base, rtext[1:]), lnum + rnum)
                else:
                    return ("%s%s" % (base, rtext), lnum + rnum)
            else:
                if rtext.startswith("ഒ"):  # For numbers starting with "ഒ"
                    return ("%sത്തിയൊ%s" % (ltext, rtext[1:]), lnum + rnum)
                else:
                    return ("%sത്തി%s" % (ltext, rtext), lnum + rnum)
        elif lnum > rnum:  # For cases like 20 + 2
            # Use special connectors for compound numbers below 100
            if lnum >= 20 and rnum < 10:
                return ("%sതി%s" % (ltext, rtext), lnum + rnum)
            else:
                return ("%s %s" % (ltext, rtext), lnum + rnum)
        else:
            return ("%s %s" % (ltext, rtext), lnum + rnum)

    def to_ordinal(self, value):
        # For ordinals, we typically add "ആം" suffix to cardinals
        cardinal = self.to_cardinal(value)
        
        # Special transformations for common patterns
        if cardinal.endswith("ആയിരം"):
            return cardinal.replace("ആയിരം", "ായിരാം")
        elif cardinal.endswith("ലക്ഷം"):
            return cardinal.replace("ലക്ഷം", "ലക്ഷാം")  
        elif cardinal.endswith("കോടി"):
            return cardinal.replace("കോടി", "കോടിയാം")
        elif cardinal.endswith("നൂറ്"):
            return cardinal.replace("നൂറ്", "നൂറാം")
        
        # Remove trailing letters that conflict with ordinal suffix
        if cardinal.endswith('്'):
            cardinal = cardinal[:-1]
        
        # Add ordinal suffix
        return cardinal + "ാം"