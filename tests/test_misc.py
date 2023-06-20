# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Taneli Hukkinen
# Licensed to PSF under a Contributor Agreement.

import os
import copy
import datetime
from decimal import Decimal as D
import tempfile
import unittest

import tomli

timezone = tomli._re.timezone

TMP_DIR_PATH = os.path.join(tempfile.gettempdir(), 'tomli_file_loading_tests')

if not os.path.isdir(TMP_DIR_PATH):
    os.mkdir(TMP_DIR_PATH)

class TestMiscellaneous(unittest.TestCase):


    def test_load(self):
        content = "one=1 \n two='two' \n arr=[]"
        expected = {"one": 1, "two": "two", "arr": []}


        
        file_path = os.path.join(TMP_DIR_PATH, "tomli_test_correct_load.toml")
        with open(file_path, 'wt') as f:
            f.write(content)

        with open(file_path, "rb") as bin_f:
            actual = tomli.load(bin_f)
        self.assertEqual(actual, expected)

        os.unlink(file_path)

    @unittest.skipIf(hasattr(str, 'decode'), reason = "str can be decoded, so won't trip error (Python 2 or Iron Python 2)")
    def test_incorrect_load(self):

        content = "one=1"


        file_path = os.path.join(TMP_DIR_PATH, "tomli_test_incorrect_load.toml")
        with open(file_path, 'wt') as f:
            f.write(content)

        with open(file_path, "rt") as txt_f:
            with self.assertRaises(TypeError):
                tomli.load(txt_f)  # type: ignore[arg-type]

        os.unlink(file_path)

    def test_parse_float(self):
        doc = """
              val=0.1
              biggest1=inf
              biggest2=+inf
              smallest=-inf
              notnum1=nan
              notnum2=-nan
              notnum3=+nan
              """
        obj = tomli.loads(doc, parse_float=D)
        expected = {
            "val": D("0.1"),
            "biggest1": D("inf"),
            "biggest2": D("inf"),
            "smallest": D("-inf"),
            "notnum1": D("nan"),
            "notnum2": D("-nan"),
            "notnum3": D("nan"),
        }
        for k, expected_val in expected.items():
            actual_val = obj[k]
            self.assertIsInstance(actual_val, D)
            if actual_val.is_nan():
                self.assertTrue(expected_val.is_nan())
            else:
                self.assertEqual(actual_val, expected_val)

    def test_deepcopy(self):
        doc = """
              [bliibaa.diibaa]
              offsettime=[1979-05-27T00:32:00.999999-07:00]
              """
        obj = tomli.loads(doc)
        obj_copy = copy.deepcopy(obj)
        self.assertEqual(obj_copy, obj)
        expected_obj = {
            "bliibaa": {
                "diibaa": {
                    "offsettime": [
                        datetime.datetime(
                            1979,
                            5,
                            27,
                            0,
                            32,
                            0,
                            999999,
                            tzinfo=timezone(datetime.timedelta(hours=-7)),
                        )
                    ]
                }
            }
        }
        self.assertEqual(obj_copy, expected_obj)

    def test_inline_array_recursion_limit(self):
        nest_count = 470
        recursive_array_toml = "arr = " + nest_count * "[" + nest_count * "]"
        dict_ = tomli.loads(recursive_array_toml)

        list_ = dict_['arr']

        i = 1
        while len(list_) >= 1:
            list_ = list_[0]
            i += 1

        self.assertEqual(i, nest_count)

    def test_inline_table_recursion_limit(self):
        nest_count = 310
        recursive_table_toml = nest_count * "key = {" + nest_count * "}"
        dict_ = tomli.loads(recursive_table_toml)

        i = 0
        while 'key' in dict_:
            dict_ = dict_['key']
            i += 1

        self.assertEqual(i, nest_count)
