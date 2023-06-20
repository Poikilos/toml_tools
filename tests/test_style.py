# -*- coding: utf-8 -*-

import tomli
import unittest
from collections import OrderedDict

class TableWritingTests(unittest.TestCase):
    def test_table_with_empty_array(self):
        # Empty arrays should never be AoTs
        example = {"table": {"array": []}}
        expected = """\
[table]
array = []
"""
        actual = tomli.dumps(example)
        self.assertEqual(actual, expected)
        self.assertEqual(tomli.loads(actual), example)


    def test_newline_before_table(self):
        actual = tomli.dumps({"table": {}})
        expected = "[table]\n"
        self.assertEqual(actual, expected)

        example = OrderedDict([("table", {"nested": {}, "val3": 3}), 
                               ("val2", 2), 
                               ("val1", 1)])
        
        actual = tomli.dumps(example)
        expected = """\
val2 = 2
val1 = 1

[table]
val3 = 3

[table.nested]
"""
        self.assertEqual(actual, expected)


    def test_empty_doc(self):
        self.assertEqual(tomli.dumps({}), "")


    def test_dont_write_redundant_tables(self):
        actual = tomli.dumps({"tab1": {"tab2": {"tab3": {}}}})
        expected = "[tab1.tab2.tab3]\n"
        self.assertEqual(actual, expected)


    def test_multiline(self):
        multiline_string = (
            "This is longer than threshold!\n"
            "Should be formatted as a multiline basic string"
        )
        actual = tomli.dumps({"ml_string": multiline_string}, multiline_strings=True)
        expected = '''\
ml_string = """
This is longer than threshold!
Should be formatted as a multiline basic string"""
'''
        self.assertEqual(actual, expected)


    def test_only_tables(self):
        actual = tomli.dumps(OrderedDict([("tab1", {}), 
                                               ("tab2", {})]))
        expected = """\
[tab1]

[tab2]
"""
        self.assertEqual(actual, expected)



class KeysTests(unittest.TestCase):

    def test_tricky_keys(self):
        example = OrderedDict([("f", 1), 
                               ("tab1", {}), 
                               ("", {"f": 2, "": {"": 1}}), 
                               ("tab3", {})])
        actual = tomli.dumps(example)
        expected = """\
f = 1

[tab1]

[""]
f = 2

["".""]
"" = 1

[tab3]
"""
        self.assertEqual(actual, expected)


    def test_nested_keys(self):
        actual = tomli.dumps(
            {
                "k": 1,
                "a": {"b": {"c": {"d": {"e": {"f": {}}, "e2": {"f2": {}}}, "d_key1": 1}}},
            }
        )
        expected = """\
k = 1

[a.b.c]
d_key1 = 1

[a.b.c.d.e.f]

[a.b.c.d.e2.f2]
"""
        self.assertEqual(actual, expected)
    


class ArrayOfTablesTests(unittest.TestCase):

    def test_example_issue_12(self):
        example = {
            "table": {
                "nested_table": [
                    {"array_options": [1, 2, 3]},
                    {"another_array": [1, 2]},
                    {"c": 3},
                ]
            }
        }
        expected = """\
[[table.nested_table]]
array_options = [
    1,
    2,
    3,
]

[[table.nested_table]]
another_array = [
    1,
    2,
]

[[table.nested_table]]
c = 3
"""
        actual = tomli.dumps(example)
        self.assertEqual(actual, expected)
        self.assertEqual(tomli.loads(actual), example)


    def test_non_trivial_nesting(self):

        # Use OrderedDict for dicts with more than one key, if the
        # test requires equality to a string literal.
        long = OrderedDict([
            ("long-value", "Lorem ipsum dolor sit amet"),
            ("another-long-value", "consectetur adipiscing elit"),
            ("a-third-one", "sed do eiusmod tempor incididunt ut labore et dolore magna"),
            ("simple-value", 3)
        ])
        example = {
            "table": {
                "aot": [
                    {"nested-table": {"nested_aot": [{"a": [0, 1]}, {"b": 2}, {"c": 3}]}},
                    {"other-nested-table": OrderedDict([("d", 4), 
                                                        ("e", 5), 
                                                        ("f", [{"g": 6}]), 
                                                        ("h", [long])])},
                ]
            }
        }

        expected = """\
[[table.aot]]

[[table.aot.nested-table.nested_aot]]
a = [
    0,
    1,
]

[[table.aot.nested-table.nested_aot]]
b = 2

[[table.aot.nested-table.nested_aot]]
c = 3

[[table.aot]]

[table.aot.other-nested-table]
d = 4
e = 5
f = [
    { g = 6 },
]

[[table.aot.other-nested-table.h]]
long-value = "Lorem ipsum dolor sit amet"
another-long-value = "consectetur adipiscing elit"
a-third-one = "sed do eiusmod tempor incididunt ut labore et dolore magna"
simple-value = 3
"""
        actual = tomli.dumps(example)
        self.assertEqual(actual, expected)
        self.assertEqual(tomli.loads(actual), example)




    def test_array_of_tables_containing_lists(self):
        example = {"aot": [{"a": [0, 1, 2, 3]}]}
        expected = """\
[[aot]]
a = [
    0,
    1,
    2,
    3,
]
"""
        actual = tomli.dumps(example)
        self.assertEqual(actual, expected)
        self.assertEqual(tomli.loads(actual), example)

        example = {"a": {"nested": example}}
        expected = """\
[[a.nested.aot]]
a = [
    0,
    1,
    2,
    3,
]
"""
        actual = tomli.dumps(example)
        self.assertEqual(actual, expected)
        self.assertEqual(tomli.loads(actual), example)


    def test_array_of_long_tables(self):

        long_dict = OrderedDict([
            ("long-value", "Lorem ipsum sith"),
            ("another-long-value", "consectetur adipis"),
            ("simple-value", 3)
        ])
        example = {"table": {"nested-array": [{"a": 42}, long_dict]}}
        expected = """\
[[table.nested-array]]
a = 42

[[table.nested-array]]
long-value = "Lorem ipsum sith"
another-long-value = "consectetur adipis"
simple-value = 3
"""
        actual = tomli.dumps(example)
        self.assertEqual(actual, expected)
        self.assertEqual(tomli.loads(actual), example)


    def test_array_of_short_tables(self):
        long_name = "a" * 87
        example = {"table": {"nested-array": [{long_name: 0}, {"b": 1}, {"c": 2}]}}
        expected = """\
[table]
nested-array = [
    { %s = 0 },
    { b = 1 },
    { c = 2 },
]
""" % long_name
        
        actual = tomli.dumps(example)
        self.assertEqual(actual, expected)
        self.assertEqual(tomli.loads(actual), example)




    def test_multiline_in_aot(self):
        data = {"aot": [{"multiline_string": "line1\nline2"}]}
        self.assertEqual(
            tomli.dumps(data, multiline_strings=True),
            '''\
[[aot]]
multiline_string = """
line1
line2"""
'''
        )
        self.assertEqual(
            tomli.dumps(data, multiline_strings=False),
            """\
aot = [
    { multiline_string = "line1\\nline2" },
]
"""
        )

