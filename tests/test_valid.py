# -*- coding: utf-8 -*-

import os
import glob
from decimal import Decimal
from math import isnan
import unittest

import toml_tools

stem = toml_tools.stem


PARENT_DIR = os.path.dirname(__file__)
COMPLIANCE_DIR = os.path.join(PARENT_DIR, "data", "toml-lang-compliance", "valid")
EXTRAS_DIR = os.path.join(PARENT_DIR, "data", "extras", "valid")

VALID_FILES = (glob.glob(os.path.join(COMPLIANCE_DIR,"**/*.toml")) + 
               glob.glob(os.path.join(EXTRAS_DIR, "**/*.toml")))




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



class ValidTests(unittest.TestCase):
    pass


def make_test_valid_method(valid):
    def test_valid(self, valid = valid):
        with open(valid,'rb') as f:
            original_str = f.read().decode()
        # original_str = valid.read_bytes().decode()
        original_data = toml_tools.loads(original_str)
        dump_str = toml_tools.dumps(original_data)
        after_dump_data = toml_tools.loads(dump_str)
        self.assertEqual(replace_nans(after_dump_data), 
                         replace_nans(original_data))
    
    return test_valid


for valid_file, id in zip(VALID_FILES,
                          (os.path.splitext(p)[0] for p in VALID_FILES)):
                        # ids=[stem(p) for p in VALID_FILES],
    
    method_name = 'test_%s' % id.replace(os.sep,'_').replace('-','_')
    names.add(method_name)

    method = make_test_valid_method(valid_file)
    if stem(valid_file) in ("qa-array-inline-nested-1000"
                           ,"qa-table-inline-nested-1000"):
        method = unittest.expectedFailure(method)# pytest.xfail("This much recursion is not supported")

    setattr(ValidTests, method_name, method)


def make_test_obj_to_str_mapping_test(obj,
                                      expected_str, 
                                      multiline_strings):
    def test_obj_to_str_mapping(self,
                                obj = obj,
                                expected_str = expected_str,
                                multiline_strings = multiline_strings):
        self.assertEqual(toml_tools.dumps(obj, multiline_strings=multiline_strings),
                         expected_str)
    return test_obj_to_str_mapping

for name, obj, expected, multiline_strings in [
        ('test_1', {"cr-newline": "foo\rbar"}, 'cr-newline = "foo\\rbar"\n', True),
        ('test_2', {"crlf-newline": "foo\r\nbar"}, 'crlf-newline = """\nfoo\nbar"""\n', True)]:
    setattr(ValidTests, name, make_test_obj_to_str_mapping_test(obj, expected, multiline_strings))



