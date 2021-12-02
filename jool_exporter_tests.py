#!/usr/bin/env python3

# This source code is licensed under the BSD license found in the
# LICENSE file in the root directory of this source tree.
# coding=utf8

import unittest
from unittest.mock import Mock

import jool_exporter


# Turn off logging for unit tests - Comment out to enable
jool_exporter.LOG = Mock()


class TestJoolExporter(unittest.TestCase):
    def setUp(self) -> None:
        self.je = jool_exporter.JoolCollector()
        self.je_ns = jool_exporter.JoolCollector('some_namespace')

    def test_handle_debug(self) -> None:
        self.assertFalse(jool_exporter._handle_debug(False))


if __name__ == "__main__":
    unittest.main()
