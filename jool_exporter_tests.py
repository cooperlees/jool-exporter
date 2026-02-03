#!/usr/bin/env python3

# This source code is licensed under the BSD license found in the
# LICENSE file in the root directory of this source tree.
# coding=utf8

import argparse
import unittest
from unittest.mock import Mock

import jool_exporter

# Turn off logging for unit tests - Comment out to enable
jool_exporter.LOG = Mock()


class TestJoolExporter(unittest.TestCase):
    def setUp(self) -> None:
        args = argparse.Namespace(
            cli=jool_exporter.DEFAULT_CLI, instance=jool_exporter.DEFAULT_INSTANCE
        )
        self.je = jool_exporter.JoolCollector(args)

    def test_handle_debug(self) -> None:
        self.assertFalse(jool_exporter._handle_debug(False))


if __name__ == "__main__":
    unittest.main()
