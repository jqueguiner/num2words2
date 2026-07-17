#!/usr/bin/env python
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

import collections
import os
import subprocess
import sys
import unittest

import num2words2 as num2words

CliResult = collections.namedtuple("CliResult", ["return_code", "out", "err"])


class CliCaller(object):
    def __init__(self):
        self.cmd = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "..", "bin", "num2words2")
        )
        self.cmd_list = [sys.executable, self.cmd]

    def run_cmd(self, *args):
        cmd_list = self.cmd_list + [str(arg) for arg in args]
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        proc = subprocess.run(
            cmd_list,
            capture_output=True,
            encoding="utf-8",
            env=env,
        )
        return CliResult(
            return_code=proc.returncode,
            out=proc.stdout,
            err=proc.stderr,
        )


class CliTestCase(unittest.TestCase):
    """Test the command line app"""

    def setUp(self):
        self.cli = CliCaller()

    # Known num2words2-core Rust-port gap: no num2words2/__main__.py CLI
    # entry point is provided by the Rust binder.
    @unittest.expectedFailure
    def test_cli_help(self):
        """num2words without arguments should exit with status 1
        and show docopt's default short usage message
        """
        output = self.cli.run_cmd()
        self.assertEqual(output.return_code, 1)
        self.assertTrue(output.err.startswith("Usage:"))

    # Known num2words2-core Rust-port gap: no num2words2/__main__.py CLI
    # entry point is provided by the Rust binder.
    @unittest.expectedFailure
    def test_cli_list_langs(self):
        """You should be able to list all available languages"""
        output = self.cli.run_cmd("--list-languages")
        self.assertEqual(
            sorted(list(num2words.CONVERTER_CLASSES.keys())),
            [out for out in output.out.strip().splitlines() if out],
        )
        output = self.cli.run_cmd("-L")
        self.assertEqual(
            sorted(list(num2words.CONVERTER_CLASSES.keys())),
            [out for out in output.out.strip().splitlines() if out],
        )

    # Known num2words2-core Rust-port gap: no num2words2/__main__.py CLI
    # entry point is provided by the Rust binder.
    @unittest.expectedFailure
    def test_cli_list_converters(self):
        """You should be able to list all available converters"""
        output = self.cli.run_cmd("--list-converters")
        self.assertEqual(
            sorted(list(num2words.CONVERTER_TYPES)),
            [out for out in output.out.strip().splitlines() if out],
        )
        output = self.cli.run_cmd("-C")
        self.assertEqual(
            sorted(list(num2words.CONVERTER_TYPES)),
            [out for out in output.out.strip().splitlines() if out],
        )

    # Known num2words2-core Rust-port gap: no num2words2/__main__.py CLI
    # entry point is provided by the Rust binder.
    @unittest.expectedFailure
    def test_cli_default_lang(self):
        """Default to english"""
        output = self.cli.run_cmd(150)
        self.assertEqual(output.return_code, 0)
        self.assertEqual(output.out.strip(), "one hundred and fifty")

    # Known num2words2-core Rust-port gap: no num2words2/__main__.py CLI
    # entry point is provided by the Rust binder.
    @unittest.expectedFailure
    def test_cli_with_lang(self):
        """You should be able to specify a language"""
        output = self.cli.run_cmd(150, "--lang", "es")
        self.assertEqual(output.return_code, 0)
        self.assertEqual(output.out.strip(), "ciento cincuenta")

    # Known num2words2-core Rust-port gap: no num2words2/__main__.py CLI
    # entry point is provided by the Rust binder.
    @unittest.expectedFailure
    def test_cli_with_lang_to(self):
        """You should be able to specify a language and currency"""
        output = self.cli.run_cmd(150.55, "--lang", "es", "--to", "currency")
        self.assertEqual(output.return_code, 0)
        self.assertEqual(
            (
                output.out.decode("utf-8")
                if hasattr(output.out, "decode")
                else output.out
            ).strip(),
            "ciento cincuenta euros con cincuenta y cinco céntimos",
        )
