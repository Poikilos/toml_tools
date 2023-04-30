# -*- coding: utf-8 -*-

import os
import glob
from decimal import Decimal
from math import isnan

import pytest
from . import toml_tools, stem


PARENT_DIR = os.path.dirname(__file__)
COMPLIANCE_DIR = os.path.join(PARENT_DIR, "data", "toml-lang-compliance", "valid")
EXTRAS_DIR = os.path.join(PARENT_DIR, "data", "extras", "valid")

VALID_FILES = (glob.glob(os.path.join(COMPLIANCE_DIR,"**/*.toml")) + 
               glob.glob(os.path.join(EXTRAS_DIR, "**/*.toml")))


@pytest.mark.parametrize(
    "valid",
    VALID_FILES#),
    #ids=[os.path.splitext(p)[0] for p in VALID_FILES],
    # ids=[stem(p) for p in VALID_FILES],
)
def test_valid(valid):
    if stem(valid) in {"qa-array-inline-nested-1000", "qa-table-inline-nested-1000"}:
        pytest.xfail("This much recursion is not supported")
    with open(valid,'rb') as f:
        original_str = f.read().decode()
    # original_str = valid.read_bytes().decode()
    original_data = toml_tools.loads(original_str)
    dump_str = toml_tools.dumps(original_data)
    after_dump_data = toml_tools.loads(dump_str)
    assert replace_nans(after_dump_data) == replace_nans(original_data)


NAN = object()


def replace_nans(cont):
    #type(Union[dict, list] -> Union[dict, list])
    """Replace NaNs with a sentinel object to fix the problem that NaN is not
    equal to another NaN."""
    for k, v in cont.items() if isinstance(cont, dict) else enumerate(cont):
        if isinstance(v, (float, Decimal)) and isnan(v):
            cont[k] = NAN
        elif isinstance(v, dict) or isinstance(v, list):
            cont[k] = replace_nans(cont[k])
    return cont


@pytest.mark.parametrize(
    "obj,expected_str,multiline_strings",
    [
        ({"cr-newline": "foo\rbar"}, 'cr-newline = "foo\\rbar"\n', True),
        ({"crlf-newline": "foo\r\nbar"}, 'crlf-newline = """\nfoo\nbar"""\n', True),
    ],
)
def test_obj_to_str_mapping(obj, expected_str, multiline_strings):
    assert toml_tools.dumps(obj, multiline_strings=multiline_strings) == expected_str
