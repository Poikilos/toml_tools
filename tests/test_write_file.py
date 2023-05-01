# -*- coding: utf-8 -*-

import toml_tools
import unittest

class FileWriterTests(unittest.TestCase):
    def test_dump(self, tmp_path):
        toml_obj = {"testing": "test\ntest"}
        path = tmp_path / "test.toml"
        with open(path, "wb") as f:
            toml_tools.dump(toml_obj, f)
            
        self.assertEqual(path.read_bytes().decode() == 'testing = "test\\ntest"\n')
