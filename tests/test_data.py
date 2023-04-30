# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.

import os
import json
import glob 
import unittest

from . import burntsushi, toml_tools, stem


class MissingFile:
    def __init__(self, path):
        self.path = path


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

VALID_FILES = glob.glob(os.path.join(DATA_DIR, "valid", "**/*.toml"))
assert VALID_FILES, "Valid TOML test files not found"

_expected_files = []
for p in VALID_FILES:
    json_path = os.path.splitext(p)[0] + ".json"
    try:
        with open(json_path, 'rb') as f:
            text = json.loads(f.read().decode())
    except FileNotFoundError:
        text = MissingFile(json_path)
    _expected_files.append(text)
VALID_FILES_EXPECTED = tuple(_expected_files)

INVALID_FILES = glob.glob(os.path.join(DATA_DIR, "invalid", "**/*.toml"))
assert INVALID_FILES, "Invalid TOML test files not found"


class TestData(unittest.TestCase):
    pass

def make_valid_test(t):
    valid = t[0]
    expected = t[1]
    def test_valid(self):

        if isinstance(expected, MissingFile):
            # For a poor man's xfail, assert that this is one of the
            # test cases where expected data is known to be missing.
            assert stem(valid) in {
                "qa-array-inline-nested-1000",
                "qa-table-inline-nested-1000",
            }
            return
        

        with open(valid, 'rb') as f:
            toml_str = f.read().decode()
        actual = toml_tools.loads(toml_str)
        actual = burntsushi.convert(actual)
        expected = burntsushi.normalize(expected)
        self.assertEqual(actual, expected)
    return test_valid

for valid, expected in zip(VALID_FILES, VALID_FILES_EXPECTED):
    setattr(TestData, 
            'test_valid_%s' % stem(valid).replace('-','_'), 
            make_valid_test((valid, expected)))



def make_invalid_test(invalid):
    def test_invalid(self):
        with open(invalid,'rb') as f:
            toml_bytes = f.read()
            try:
                toml_str = toml_bytes.decode('utf8')
            except UnicodeDecodeError:
                # Some BurntSushi tests are not valid UTF-8. Skip those.

                assert True # a poorer man's xfail
                return
            with self.assertRaises(toml_tools.TOMLDecodeError):
                toml_tools.loads(toml_str)
    return test_invalid

for invalid in INVALID_FILES:
    setattr(TestData,
            'test_invalid_%s' % stem(invalid).replace('-','_'), 
            make_invalid_test(invalid))
