# -*- coding: utf-8 -*-

import os
import tomli
import unittest
import tempfile

TMP_DIR_PATH = os.path.join(tempfile.gettempdir(), 'tomli_write_file_tests')

if not os.path.isdir(TMP_DIR_PATH):
    os.mkdir(TMP_DIR_PATH)

class FileWriterTests(unittest.TestCase):
    def test_dump(self):
        toml_obj = {"testing": "test\ntest"}
        path = os.path.join(TMP_DIR_PATH, "tomli_test_dump.toml")
        with open(path, "wb") as f:
            tomli.dump(toml_obj, f)

        with open(path, 'rb') as f:
            actual = f.read().decode(encoding = 'utf8')
        self.assertEqual(actual, 'testing = "test\\ntest"\n')
