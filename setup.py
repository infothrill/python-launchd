#!/usr/bin/env python

import sys
import re
import os

from setuptools import setup

classifiers = [line.strip() for line in """
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: DFSG approved
License :: OSI Approved
License :: OSI Approved :: MIT License
Topic :: Software Development :: Libraries :: Python Modules
Environment :: MacOS X
Natural Language :: English
Operating System :: MacOS :: MacOS X
Programming Language :: Python
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
Programming Language :: Python :: Implementation :: CPython
""".splitlines() if len(line) > 0]

install_requires = ["pyobjc-framework-ServiceManagement"]

if "darwin" not in sys.platform:
    sys.stderr.write("Warning: The package 'launchd' can only be installed and run on macOS!" + os.linesep)

v = open(os.path.join(os.path.dirname(__file__), "launchd", "__init__.py"))
VERSION = re.compile(r".*__version__ = \"(.*?)\"", re.S).match(v.read()).group(1)
v.close()
LONG_DESCRIPTION = open("README.rst").read() + "\n\n" + open("CHANGELOG.rst").read()
setup(name="launchd",
      packages=["launchd", "launchd.tests"],
      version=VERSION,
      author="Paul Kremer",
      author_email="@".join(("paul", "spurious.biz")),  # avoid spam,
      license="MIT License",
      description="pythonic interface for macOS launchd",
      long_description=LONG_DESCRIPTION,
      url="https://github.com/infothrill/python-launchd",
      install_requires=install_requires,
      classifiers=classifiers,
      test_suite="launchd.tests",
      tests_require=[],
      )
