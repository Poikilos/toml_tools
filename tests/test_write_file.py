# -*- coding: utf-8 -*-

import os
import toml_tools
import unittest
import tempfile

TMP_DIR_PATH = os.path.join(tempfile.gettempdir(), 'toml_tools_write_file_tests')

class FileWriterTests(unittest.TestCase):
    def test_dump(self):
        toml_obj = {"testing": "test\ntest"}
        path = os.path.join(TMP_DIR_PATH, "toml_tools_test_dump.toml")
        with open(path, "wb") as f:
            toml_tools.dump(toml_obj, f)

        with open(path, 'rb') as f:
            actual = f.read().decode()
        self.assertEqual(actual, 'testing = "test\\ntest"\n')
