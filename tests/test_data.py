# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.

import os
import sys
import datetime
import json
import glob 
import unittest

import toml_tools


stem = toml_tools.stem

#################################################################


"""Utilities for tests that are in the "burntsushi" format."""

try:
    basestring #type: ignore
except NameError:
    basestring = str

# Aliases for converting TOML compliance format [1] to BurntSushi format [2]
# [1] https://github.com/toml-lang/compliance/blob/db7c3211fda30ff9ddb10292f4aeda7e2e10abc4/docs/json-encoding.md  # noqa: E501
# [2] https://github.com/BurntSushi/toml-test/blob/4634fdf3a6ecd6aaea5f4cdcd98b2733c2694993/README.md  # noqa: E501
_aliases = {
    "boolean": "bool",
    "offset datetime": "datetime",
    "local datetime": "datetime-local",
    "local date": "date-local",
    "local time": "time-local",
}


def convert(obj):  # noqa: C901
    if isinstance(obj, basestring):
        return {"type": "string", "value": obj}
    elif isinstance(obj, bool):
        return {"type": "bool", "value": str(obj).lower()}
    elif isinstance(obj, int):
        return {"type": "integer", "value": str(obj)}
    elif isinstance(obj, float):
        return {"type": "float", "value": _normalize_float_str(str(obj))}
    elif isinstance(obj, datetime.datetime):
        val = _normalize_datetime_str(obj.isoformat())
        if obj.tzinfo:
            return {"type": "datetime", "value": val}
        return {"type": "datetime-local", "value": val}
    elif isinstance(obj, datetime.time):
        return {
            "type": "time-local",
            "value": _normalize_localtime_str(str(obj)),
        }
    elif isinstance(obj, datetime.date):
        return {
            "type": "date-local",
            "value": str(obj),
        }
    elif isinstance(obj, list):
        return [convert(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    raise Exception("unsupported type: %s, %s" % (obj, type(obj)) )


def normalize(obj):
    """Normalize test objects.

    This normalizes primitive values (e.g. floats), and also converts from
    TOML compliance format [1] to BurntSushi format [2].

    [1] https://github.com/toml-lang/compliance/blob/db7c3211fda30ff9ddb10292f4aeda7e2e10abc4/docs/json-encoding.md  # noqa: E501
    [2] https://github.com/BurntSushi/toml-test/blob/4634fdf3a6ecd6aaea5f4cdcd98b2733c2694993/README.md  # noqa: E501
    """
    if isinstance(obj, list):
        return [normalize(item) for item in obj]
    if isinstance(obj, dict):
        if "type" in obj and "value" in obj:
            type_ = obj["type"]
            norm_type = _aliases.get(type_, type_)
            value = obj["value"]
            if norm_type == "float":
                norm_value = _normalize_float_str(value)
            elif norm_type in {"datetime", "datetime-local"}:
                norm_value = _normalize_datetime_str(value)
            elif norm_type == "time-local":
                norm_value = _normalize_localtime_str(value)
            else:
                norm_value = value

            if norm_type == "array":
                return [normalize(item) for item in value]
            return {"type": norm_type, "value": norm_value}
        return {k: normalize(v) for k, v in obj.items()}
    raise AssertionError("Burntsushi fixtures should be dicts/lists only")


def _normalize_datetime_str(dt_str):
    #type(str) -> str
    if dt_str[-1].lower() == "z":
        dt_str = dt_str[:-1] + "+00:00"

    date = dt_str[:10]
    rest = dt_str[11:]

    if "+" in rest:
        sign = "+"
    elif "-" in rest:
        sign = "-"
    else:
        sign = ""

    if sign:
        time, _, offset = rest.partition(sign)
    else:
        time = rest
        offset = ""

    time = time.rstrip("0") if "." in time else time
    return date + "T" + time + sign + offset


def _normalize_localtime_str(lt_str):
    #type(str) -> str
    return lt_str.rstrip("0") if "." in lt_str else lt_str


def _normalize_float_str(float_str):
    #type(str) -> str
    as_float = float(float_str)

    # Normalize "-0.0" and "+0.0"
    if as_float == 0:
        return "0"

    return str(as_float)



#################################################################

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

def make_valid_test(valid, expected):
    def test_valid(self, valid = valid, expected  = expected):

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
        actual = convert(actual)
        expected = normalize(expected)
        self.assertEqual(actual, expected)
    return test_valid

for valid, expected in zip(VALID_FILES, VALID_FILES_EXPECTED):
    setattr(TestData, 
            'test_valid_%s' % stem(valid).replace('-','_'), 
            make_valid_test(valid, expected))



def make_invalid_test(invalid):
    def test_invalid(self, invalid = invalid):
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
