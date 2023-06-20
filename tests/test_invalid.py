# -*- coding: utf-8 -*-
from datetime import time

import unittest

import tomli

timezone = tomli._re.timezone 

class InvalidDataTests(unittest.TestCase):
    def test_invalid_type_nested(self):
        with self.assertRaises(TypeError):
            tomli.dumps({"bytearr": bytearray()})


    def test_invalid_time(self):
        offset_time = time(23, 59, 59, tzinfo=timezone.utc)
        with self.assertRaises(ValueError):
            tomli.dumps({"offset time": offset_time})
