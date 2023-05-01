# -*- coding: utf-8 -*-

from decimal import Decimal
import unittest

import toml_tools

class TypeWriterTests(unittest.TestCase):
    def test_decimal(self):
        obj = {
            "decimal-0": Decimal(0),
            "decimal-pi": Decimal("3.14159"),
            "decimal-inf": Decimal("inf"),
            "decimal-minus-inf": Decimal("-inf"),
            "decimal-nan": Decimal("nan"),
        }
        self.assertEqual(
            toml_tools.dumps(obj),
            """\
decimal-0 = 0
decimal-pi = 3.14159
decimal-inf = inf
decimal-minus-inf = -inf
decimal-nan = nan
"""
        )


    def test_tuple(self):
        obj = {"empty-tuple": (), "non-empty-tuple": (1, (2, 3))}
        self.assertEqual(
            toml_tools.dumps(obj),
            """\
empty-tuple = []
non-empty-tuple = [
    1,
    [
        2,
        3,
    ],
]
"""
        )
