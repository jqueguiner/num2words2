# -*- coding: utf-8 -*-
# Copyright (c) 2026, num2words2 contributors. All Rights Reserved.
# Licensed under LGPL-2.1 (see COPYING).
"""Allow ``python -m num2words2`` invocation. Issue #348."""
from __future__ import print_function, unicode_literals

import argparse
import sys

import num2words2


def main():
    p = argparse.ArgumentParser(prog="num2words2", description="Convert numbers to words.")
    p.add_argument("number", nargs="?", help="number to convert")
    p.add_argument("-l", "--lang", default="en", help="language code (default: en)")
    p.add_argument("--to", default="cardinal", help="cardinal/ordinal/year/currency")
    p.add_argument("--list-languages", action="store_true")
    p.add_argument("--list-converters", action="store_true")
    args = p.parse_args()
    if args.list_languages:
        for lang in sorted(num2words2.CONVERTER_CLASSES):
            print(lang)
        return 0
    if args.list_converters:
        for cvt in sorted(num2words2.CONVERTES_TYPES):
            print(cvt)
        return 0
    if args.number is None:
        p.print_help()
        return 1
    try:
        print(num2words2.num2words(args.number, lang=args.lang, to=args.to))
        return 0
    except Exception as err:
        print("{}: {}".format(args.number, err), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
