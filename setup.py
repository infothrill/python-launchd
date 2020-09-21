#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: Implementation :: CPython
""".splitlines() if len(line) > 0]

install_requires = ["six", "pyobjc-framework-ServiceManagement"]

if sys.version_info < (3, 2):
    install_requires.append("argparse")

if not 'darwin' in sys.platform:
    sys.stderr.write("Warning: The package 'launchd' can only be installed and run on OS X!" + os.linesep)

v = open(os.path.join(os.path.dirname(__file__), 'launchd', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

setup(name="launchd",
      packages=["launchd", "launchd.tests"],
      version=VERSION,
      author="Paul Kremer",
      author_email="@".join(("paul", "spurious.biz")),  # avoid spam,
      license="MIT License",
      description="pythonic interface for OS X launchd",
      long_description=(open('README.rst', 'r').read() + '\n\n' +
                        open('CHANGELOG.rst', 'r').read()),
      url="https://github.com/infothrill/python-launchd",
      install_requires=install_requires,
      classifiers=classifiers,
      test_suite='launchd.tests',
      tests_require=["six"],
      )
