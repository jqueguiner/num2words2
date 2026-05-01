# -*- coding: utf-8 -*-
# Copyright (c) 2026, num2words2 contributors. All Rights Reserved.
# Licensed under LGPL-2.1 (see COPYING).
"""Number-string grouping helpers.

Some locales group digits in patterns other than the standard ``,###``
Western convention.  This module exposes a single helper, :func:`group_digits`,
that returns the locale-grouped form of an integer.

Currently supported groupings:

- ``"western"``      → ``1,234,567``
- ``"indian"``       → ``12,34,567``        (lakh / crore scale)
- ``"chinese"``      → ``123,4567``         (myriad scale, every 4 digits)

Issue #66; ports the request in savoirfairelinux/num2words#547.
"""

from __future__ import unicode_literals


def group_digits(value, locale="western", separator=","):
    """Format ``value`` as a digit-grouped string.

    Examples
    --------
    >>> group_digits(100000, locale="indian")
    '1,00,000'
    >>> group_digits(12345678, locale="indian")
    '1,23,45,678'
    >>> group_digits(1234567, locale="western")
    '1,234,567'
    >>> group_digits(12345678, locale="chinese")
    '1234,5678'
    """
    if not isinstance(value, int):
        raise TypeError("group_digits requires an int, got %r" % type(value))
    sign = "-" if value < 0 else ""
    s = str(abs(value))

    if locale == "western":
        return sign + _group(s, 3, separator)
    if locale == "indian":
        # Last three digits, then groups of two on the high side.
        if len(s) <= 3:
            return sign + s
        last3, rest = s[-3:], s[:-3]
        return sign + _group(rest, 2, separator) + separator + last3
    if locale == "chinese":
        return sign + _group(s, 4, separator)
    raise ValueError("Unknown locale: %r" % locale)


def _group(s, size, separator):
    out = []
    while s:
        out.append(s[-size:])
        s = s[:-size]
    return separator.join(reversed(out))
