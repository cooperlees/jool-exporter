# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run all tests + linting (primary CI workflow):**
```
ptr
```
`ptr` (Facebook's [Python Test Runner](https://github.com/facebookincubator/ptr)) installs dependencies, runs `unittest`, then runs `black`, `mypy`, `flake8`, and `usort`. Config is in `setup.py` under `ptr_params`.

**Run tests only (without linting):**
```
python -m unittest jool_exporter_tests
```

**Run a single test:**
```
python -m unittest jool_exporter_tests.TestJoolExporter.test_handle_debug
```

**Linting tools (run individually):**
```
black jool_exporter.py jool_exporter_tests.py
mypy jool_exporter.py
flake8 jool_exporter.py
usort format jool_exporter.py
```

**Build package:**
```
python -m build
```

## Architecture

This is a single-file prometheus exporter (`jool_exporter.py`) with a corresponding test file (`jool_exporter_tests.py`).

**Flow:** On each prometheus scrape, `JoolCollector.collect()` calls `run_jool()`, which shells out to the `jool` CLI with `stats display --csv --no-headers --explain --all`. The CSV output is parsed row-by-row and each stat becomes a `GaugeMetricFamily` with a `hostname` label. `JSTAT_` prefixes are stripped and replaced with the `jool_` metric prefix.

**Key classes/functions:**
- `JoolCollector(Collector)` — prometheus_client `Collector` subclass; registered with `REGISTRY` at startup
- `run_jool()` — shells out to the jool CLI; returns `str` on success or `CompletedProcess` on failure
- `_handle_counter()` — constructs a single `GaugeMetricFamily` from a CSV row
- `main()` — parses args, starts the HTTP server (`prometheus_client.start_http_server`), registers the collector, then loops forever

**CLI arguments:** `--addr` (bind address), `--port` (default 6971), `--instance` (jool instance name, default `"default"`), `--cli` (binary name, default `"jool"`), `--debug`.

**Versioning:** CalVer (`YY.M.patch`), set in `setup.py`.

**Coverage requirement:** 25% minimum on `jool_exporter.py` (enforced by `ptr`).
