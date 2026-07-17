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
"""num2words2 — a thin Python binder over the Rust conversion core.

Every conversion is served by the compiled `_rust` extension: this module
normalises the language code, maps the public keyword arguments onto the
core's entry points, and applies the two string-level post-processing steps
(`style=`, `cents=`) that are presentation, not conversion. There is no
pure-Python conversion fallback — the core is authoritative, and an input it
declines raises rather than silently diverging.
"""
from __future__ import unicode_literals

import decimal

from .grouping import group_digits  # noqa: E402

# Version information
try:
    from ._version import __version__, __version_tuple__
except ImportError:
    # Package is not installed, provide defaults
    __version__ = "unknown"
    __version_tuple__ = (0, 0, 0, "unknown", 0)


# The compiled core is mandatory: this package is a binder over it.
from . import _rust as _RUST  # noqa: E402

_RUST_LANGS = frozenset(_RUST.supported_langs())
_RUST_TYPES = frozenset(["cardinal", "ordinal", "ordinal_num", "year"])
# The core's "declined" signal (see rust/num2words2-py/src/lib.rs). It is
# distinct from NotImplementedError so a genuine NotImplementedError raise
# propagates natively; here, with no Python conversion path behind it, a
# decline is surfaced as NotImplementedError to the caller.
_RUST_FALLBACK = _RUST.RustFallback

# bn raises NumberTooLargeError past its MAX_NUMBER. The class used to live in
# lang_BN.py; the pure binder defines it in the core and re-exports it here so
# `from num2words2 import NumberTooLargeError` (and `except`) keep working.
NumberTooLargeError = _RUST.NumberTooLargeError


__all__ = [
    "num2words",
    "num2words_sentence",
    "convert_sentence",
    "sentence_to_words",
    "group_digits",
    "maxval",
    "NumberTooLargeError",
]

CONVERTES_TYPES = [
    "cardinal", "ordinal", "ordinal_num", "year", "currency", "cheque",
    "fraction",
]
CONVERTER_TYPES = CONVERTES_TYPES  # Alias for compatibility


def maxval(lang="en"):
    """Return the maximum integer ``num2words(..., lang=lang)`` can convert.

    Issue #582 ports savoirfairelinux/num2words#582.
    """
    return _RUST.maxval(lang)


def _normalize_lang(lang):
    """Resolve a caller's language code to a core key, mirroring the historic
    dispatcher: exact match, then hyphen->underscore, then ``xx_YY`` casing,
    then the bare two-letter prefix. Raises NotImplementedError if none match.
    """
    if lang in _RUST_LANGS:
        return lang
    nl = lang.replace("-", "_")
    if nl in _RUST_LANGS:
        return nl
    parts = nl.split("_")
    if len(parts) >= 2:
        candidate = "%s_%s" % (parts[0].lower(), parts[1].upper())
        if candidate in _RUST_LANGS:
            return candidate
        if parts[0] in _RUST_LANGS:
            return parts[0]
    if nl[:2] in _RUST_LANGS:
        return nl[:2]
    raise NotImplementedError()


def _rust_kw_items(kwargs):
    """kwargs -> [(k, v)] for the core boundary, or None when a value has a
    type the boundary cannot carry (then the call is out of the core's
    envelope and must raise)."""
    items = []
    for k, v in kwargs.items():
        if v is None or isinstance(v, (bool, int, str)):
            items.append((k, v))
        elif isinstance(v, (list, tuple)) and all(
                isinstance(x, str) for x in v):
            items.append((k, list(v)))
        else:
            return None
    return items


def _apply_style(result, style, to, lang):
    """`style=` presentation post-processing (issues #535, #562). Operates on
    the rendered string, so it is conversion-independent."""
    if style == "terse" and to == "ordinal" and isinstance(result, str):
        for prefix in ("one ", "un ", "uno "):
            if result.startswith(prefix) and len(result) > len(prefix):
                result = result[len(prefix):]
                break
    if style == "us" and lang.startswith("en") and isinstance(result, str):
        result = result.replace(" and ", " ")
    return result


def _normalize_cents(kwargs):
    """`cents='omit'|'verbose'|'terse'` -> the legacy bool the core expects
    (issue #554). Returns (cents_bool, drop_cents) where drop_cents means the
    float value should be truncated to an int so no cents segment appears."""
    cents_kw = kwargs.get("cents", True)
    if cents_kw == "omit":
        return True, True
    if cents_kw == "verbose":
        return True, False
    if cents_kw == "terse":
        return False, False
    return cents_kw, False


def num2words(number, ordinal=False, lang="en", to="cardinal", **kwargs):
    # Captured before any normalisation: the core keys off the *arrival* type
    # (a plain int vs a float/Decimal vs a str), not a post-parse value.
    _plain_int = type(number) is int
    _plain_num = isinstance(number, (float, decimal.Decimal))

    lang = _normalize_lang(lang)
    _style = kwargs.get("style")

    # ---- string input: the core's from_string owns the whole pipeline
    # (fraction strings, str_to_number incl. the ES "1ro" / pt_BR "ponto"
    # handshakes, mixed text -> sentence, then the mode dispatch).
    if isinstance(number, str):
        _to_final = "ordinal" if ordinal else to
        if _to_final not in CONVERTES_TYPES:
            raise NotImplementedError()
        _cents, _ = _normalize_cents(kwargs)
        _extras = {k: v for k, v in kwargs.items()
                   if k not in ("currency", "cents", "separator",
                                "adjective", "style", "precision")}
        _items = _rust_kw_items(_extras)
        if _cents not in (True, False) or _items is None:
            raise NotImplementedError()
        try:
            _kind, _out = _RUST.from_string(
                lang, number, _to_final, kwargs.get("currency"), _cents,
                kwargs.get("separator"), kwargs.get("adjective"), _items)
        except _RUST_FALLBACK:
            raise NotImplementedError()
        if _kind != 0:
            raise NotImplementedError()
        return _apply_style(_out, _style, _to_final, lang)

    # backwards compatible
    if ordinal:
        to = "ordinal"
    if to not in CONVERTES_TYPES:
        raise NotImplementedError()

    _precision = kwargs.get("precision")
    _extras = {k: v for k, v in kwargs.items()
               if k not in ("style", "precision")}

    # ---- integer modes with a plain int
    if _plain_int and to in _RUST_TYPES:
        _items = _rust_kw_items(_extras)
        if _items is not None:
            try:
                if _items:
                    result = getattr(_RUST, "to_%s_kw" % to)(
                        lang, number, _items)
                else:
                    result = getattr(_RUST, "to_%s" % to)(lang, number)
            except _RUST_FALLBACK:
                raise NotImplementedError()
            return _apply_style(result, _style, to, lang)

    # ---- float / Decimal, all four integer modes
    if _plain_num and to in _RUST_TYPES:
        try:
            _finite = float(number) == float(number) and float(
                number) not in (float("inf"), float("-inf"))
        except (OverflowError, ValueError):
            _finite = False
        _fitems = {k: v for k, v in _extras.items()
                   if k not in ("currency", "cents", "separator", "adjective")}
        _items = _rust_kw_items(_fitems)
        if _finite and _items is not None:
            _prec = abs(decimal.Decimal(str(number)).as_tuple().exponent)
            _dec = str(number) if isinstance(number, decimal.Decimal) else ""
            try:
                result = _RUST.to_float(
                    lang, to, float(number), _prec, _dec, str(number),
                    _precision, _items)
            except _RUST_FALLBACK:
                raise NotImplementedError()
            return _apply_style(result, _style, to, lang)

    # ---- currency
    if to == "currency" and isinstance(number, (int, float, decimal.Decimal)):
        _cents, _drop = _normalize_cents(kwargs)
        if _drop and isinstance(number, float):
            number = int(number)  # int path drops cents naturally
        if _cents in (True, False):
            _citems = {k: v for k, v in _extras.items()
                       if k not in ("currency", "cents", "separator",
                                    "adjective")}
            _items = _rust_kw_items(_citems)
            if _items is not None:
                _args = (
                    lang, str(number), type(number) is int,
                    isinstance(number, float) or "." in str(number),
                    isinstance(number, float),
                    kwargs.get("currency"), _cents,
                    kwargs.get("separator"), kwargs.get("adjective"),
                )
                try:
                    if _items:
                        return _RUST.to_currency_kw(*_args, _items)
                    return _RUST.to_currency(*_args)
                except _RUST_FALLBACK:
                    raise NotImplementedError()

    if to == "cheque" and isinstance(number, (int, float, decimal.Decimal)):
        try:
            return _RUST.to_cheque(lang, str(number), kwargs.get("currency"))
        except _RUST_FALLBACK:
            raise NotImplementedError()

    # to='fraction' with a non-string number: the historic dispatcher fed the
    # value straight to converter.to_fraction(value). A single positional (the
    # tuple ``(1, 2)``) raised TypeError where the method exists, or
    # AttributeError where it does not (bn/dv/id have no to_fraction). Probe
    # the core to tell them apart; genuine "n/d" fractions arrive as strings
    # and are served by from_string above.
    if to == "fraction":
        try:
            _RUST.to_fraction(lang, 1, 1)
        except AttributeError:
            raise
        except Exception:  # noqa: BLE001 - probing for the method's existence
            pass
        raise TypeError(
            "to_fraction() missing 1 required positional argument: "
            "'denominator'")

    raise NotImplementedError()


def num2words_sentence(sentence, lang="en", to="cardinal", **kwargs):
    """Convert every number in a sentence to words.

    `lang=None` auto-detects (lingua-rs in the full build). Handles ordinals,
    currency, dates, temperatures and plain numbers, splicing each conversion
    back in place.

    >>> num2words_sentence("I bought 6 apples")
    'I bought six apples'
    >>> num2words_sentence("The 1st place winner got $100")
    'The first place winner got one hundred dollars, zero cents'
    """
    if lang is None:
        return _RUST.sentence_auto(sentence, to)
    # The core's sentence converter does its own lang validation (and the
    # same two-letter-prefix fallback), raising NotImplementedError for an
    # unsupported language exactly as the historic dispatcher did.
    return _RUST.sentence(sentence, lang, to)


# Aliases for num2words_sentence
convert_sentence = num2words_sentence
sentence_to_words = num2words_sentence
