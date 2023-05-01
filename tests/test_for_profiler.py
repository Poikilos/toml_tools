# -*- coding: utf-8 -*-
"""Test for profiling.

This test can be useful for profiling, as most of the execution time
will be spent writing TOML instead of managing pytest execution
environment. To get and read profiler results:
  - `tox -e profile`
  - `firefox .tox/prof/combined.svg`
"""
import os
import unittest
import toml_tools


path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "benchmark", "data.toml")
with open(path, 'rb') as f:
    benchmark_toml = f.read().decode('utf8')
data = toml_tools.loads(benchmark_toml)

class ProfilerTests(unittest.TestCase):
    def test_for_profiler(self):
        # increase the count here to reduce the impact of
        # setting up pytest execution environment. Let's keep
        # the count low by default because this is part of the
        # standard test suite.
        iterations = int(os.environ.get("PROFILER_ITERATIONS", 1))
        for _ in range(iterations):
            toml_tools.dumps(data)
            
        self.assertTrue(True)
