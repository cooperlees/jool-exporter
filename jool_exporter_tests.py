#!/usr/bin/env python3

# This source code is licensed under the BSD license found in the
# LICENSE file in the root directory of this source tree.
# coding=utf8

import argparse
import unittest
from subprocess import CompletedProcess
from unittest.mock import Mock, patch

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

    @patch("jool_exporter.run")
    def test_run_jool_success(self, mock_run: Mock) -> None:
        mock_run.return_value = CompletedProcess(
            args=[], returncode=0, stdout="JSTAT_SUCCESS,1,Successful translations\n"
        )
        result = self.je.run_jool()
        self.assertEqual(result, "JSTAT_SUCCESS,1,Successful translations\n")
        cmd = mock_run.call_args[0][0]
        self.assertIn("-i", cmd)
        self.assertEqual(cmd[cmd.index("-i") + 1], jool_exporter.DEFAULT_INSTANCE)

    @patch("jool_exporter.run")
    def test_run_jool_failure(self, mock_run: Mock) -> None:
        failed_cp = CompletedProcess(args=[], returncode=1, stderr="error", stdout="")
        mock_run.return_value = failed_cp
        result = self.je.run_jool()
        self.assertIsInstance(result, CompletedProcess)
        self.assertEqual(result.returncode, 1)

    @patch("jool_exporter.run")
    def test_run_jool_instance_whitespace_stripped(self, mock_run: Mock) -> None:
        mock_run.return_value = CompletedProcess(
            args=[], returncode=0, stdout="JSTAT_SUCCESS,1,Successful translations\n"
        )
        args = argparse.Namespace(cli=jool_exporter.DEFAULT_CLI, instance="  myinst  ")
        je = jool_exporter.JoolCollector(args)
        je.run_jool()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd[cmd.index("-i") + 1], "myinst")


if __name__ == "__main__":
    unittest.main()
