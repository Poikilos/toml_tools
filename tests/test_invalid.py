# -*- coding: utf-8 -*-
from datetime import time

import unittest

import toml_tools

timezone = toml_tools._re.timezone 

class InvalidDataTests(unittest.TestCase):
    def test_invalid_type_nested(self):
        with self.assertRaises(TypeError):
            toml_tools.dumps({"bytearr": bytearray()})


    def test_invalid_time(self):
        offset_time = time(23, 59, 59, tzinfo=timezone.utc)
        with self.assertRaises(ValueError):
            toml_tools.dumps({"offset time": offset_time})
