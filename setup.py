#!/usr/bin/env python3

# This source code is licensed under the BSD license found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path

from setuptools import setup


def get_long_desc() -> str:
    repo_base = Path(__file__).parent
    long_desc = ""
    for info_file in (repo_base / "README.md",):
        with info_file.open("r", encoding="utf8") as ifp:
            long_desc += ifp.read()
        long_desc += "\n\n"

    return long_desc


setup(
    name="jool-exporter",
    version="26.2.27",
    description="Export `jool stats display` for prometheus",
    long_description=get_long_desc(),
    long_description_content_type="text/markdown",
    py_modules=["jool_exporter"],
    url="http://github.com/cooperlees/jool-exporter",
    author="Cooper Lees",
    author_email="me@cooperlees.com",
    license="BSD-2-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["jool-exporter = jool_exporter:main"]},
    install_requires=["prometheus_client"],
    test_suite="jool_exporter_tests",
)
