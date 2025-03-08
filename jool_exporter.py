#!/usr/bin/env python3

# This source code is licensed under the BSD license found in the
# LICENSE file in the root directory of this source tree.
# coding=utf8

import argparse
import csv
import logging
import sys
import time
from io import StringIO
from socket import getfqdn
from subprocess import CompletedProcess, PIPE, run
from typing import Generator, Union

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client.registry import Collector


DEFAULT_ADDR = "0.0.0.0"
DEFAULT_PORT = 6971
HOSTNAME = getfqdn()
LOG = logging.getLogger(__name__)


class JoolCollector(Collector):
    key_prefix = "jool"
    labels = ["hostname"]

    def _handle_counter(
        self, category: str, value: float, explanation: str
    ) -> GaugeMetricFamily:
        desc = "jool metric" if not explanation else explanation
        key = f"{self.key_prefix}_{category}"
        g = GaugeMetricFamily(key, desc, labels=self.labels)
        g.add_metric([HOSTNAME], value)
        return g

    def collect(self) -> Generator[GaugeMetricFamily, None, None]:
        start_time = time.time()
        LOG.info("Collection started")

        jool_data = self.run_jool()
        if isinstance(jool_data, CompletedProcess):
            LOG.error(
                f"jool failed: {jool_data.stderr} (returned {jool_data.returncode})"
            )
            return
        elif not jool_data:
            LOG.error("jool failed: No output returned")
            return

        for row in csv.reader(StringIO(jool_data)):
            yield self._handle_counter(
                row[0].replace("JSTAT_", "").lower(),
                float(row[1]),
                row[2].replace('"', ""),
            )

        run_time = time.time() - start_time
        LOG.info(f"Collection finished in {run_time}s")

    def run_jool(self) -> Union[str, CompletedProcess]:
        cmd = [
            "jool",
            "stats",
            "display",
            "--csv",
            "--no-headers",
            "--explain",
            "--all",
        ]
        cp = run(cmd, stderr=PIPE, stdout=PIPE, encoding="utf8")
        if cp.returncode:
            return cp
        return cp.stdout


def _handle_debug(debug: bool) -> None:
    """Turn on debugging if asked otherwise INFO default"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export `jool stats display` for prometheus"
    )
    parser.add_argument(
        "-a",
        "--addr",
        default=DEFAULT_ADDR,
        help=f"Address to bind socket to [Default = {DEFAULT_ADDR}]",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Verbose debug output"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run webserver on [Default = {DEFAULT_PORT}]",
    )
    args = parser.parse_args()
    _handle_debug(args.debug)

    LOG.info(f"Starting {sys.argv[0]}")
    start_http_server(args.port, args.addr)
    REGISTRY.register(JoolCollector())
    LOG.info(f"jool prometheus exporter - listening on {args.port}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LOG.info("Shutting down ...")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
