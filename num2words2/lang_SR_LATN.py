# -*- coding: utf-8 -*-
# Copyright (c) 2026, num2words2 contributors. All Rights Reserved.
# Licensed under LGPL-2.1 (see COPYING).
"""Serbian Latin (Gaj's alphabet) variant.

Issue #73 ports savoirfairelinux/num2words#332/#336.

Serbian is officially digraphic; both Cyrillic (Ћирилица) and Latin
(latinica) are in use. ``lang_SR`` returns Cyrillic by default. This
module wraps that output and transliterates digraph-by-digraph using
the standard Gaj's-Latin mapping.
"""

from __future__ import unicode_literals

from .lang_SR import Num2Word_SR

# Two-character Cyrillic → Latin mappings must come BEFORE single-character
# entries so they win during the longest-match scan.
_CYRL_TO_LATN = [
    # Digraphs are case-sensitive.
    ("Љ", "Lj"),
    ("Њ", "Nj"),
    ("Џ", "Dž"),
    ("љ", "lj"),
    ("њ", "nj"),
    ("џ", "dž"),
    # Single characters.
    ("А", "A"), ("а", "a"),
    ("Б", "B"), ("б", "b"),
    ("В", "V"), ("в", "v"),
    ("Г", "G"), ("г", "g"),
    ("Д", "D"), ("д", "d"),
    ("Ђ", "Đ"), ("ђ", "đ"),
    ("Е", "E"), ("е", "e"),
    ("Ж", "Ž"), ("ж", "ž"),
    ("З", "Z"), ("з", "z"),
    ("И", "I"), ("и", "i"),
    ("Ј", "J"), ("ј", "j"),
    ("К", "K"), ("к", "k"),
    ("Л", "L"), ("л", "l"),
    ("М", "M"), ("м", "m"),
    ("Н", "N"), ("н", "n"),
    ("О", "O"), ("о", "o"),
    ("П", "P"), ("п", "p"),
    ("Р", "R"), ("р", "r"),
    ("С", "S"), ("с", "s"),
    ("Т", "T"), ("т", "t"),
    ("Ћ", "Ć"), ("ћ", "ć"),
    ("У", "U"), ("у", "u"),
    ("Ф", "F"), ("ф", "f"),
    ("Х", "H"), ("х", "h"),
    ("Ц", "C"), ("ц", "c"),
    ("Ч", "Č"), ("ч", "č"),
    ("Ш", "Š"), ("ш", "š"),
]


def cyrl_to_latn(s):
    """Transliterate a Serbian Cyrillic string to Gaj's Latin."""
    for cyrl, latn in _CYRL_TO_LATN:
        s = s.replace(cyrl, latn)
    return s


class Num2Word_SR_LATN(Num2Word_SR):
    """Serbian (Latin script). Delegates to Num2Word_SR and transliterates."""

    def to_cardinal(self, *args, **kwargs):
        return cyrl_to_latn(super(Num2Word_SR_LATN, self).to_cardinal(*args, **kwargs))

    def to_ordinal(self, *args, **kwargs):
        return cyrl_to_latn(super(Num2Word_SR_LATN, self).to_ordinal(*args, **kwargs))

    def to_ordinal_num(self, *args, **kwargs):
        return cyrl_to_latn(
            super(Num2Word_SR_LATN, self).to_ordinal_num(*args, **kwargs)
        )

    def to_year(self, *args, **kwargs):
        return cyrl_to_latn(super(Num2Word_SR_LATN, self).to_year(*args, **kwargs))

    def to_currency(self, *args, **kwargs):
        return cyrl_to_latn(super(Num2Word_SR_LATN, self).to_currency(*args, **kwargs))
