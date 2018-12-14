#!/usr/bin/env python
"""
A setuptools based setup module generated from the xBrite Sample Package.

See:
* https://github.com/xBrite/sample-python-package
* https://packaging.python.org/en/latest/distributing.html
* https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
import os
import sys
import re

# Package configuration should all be defined here for easy access.
# Update these values as best fits your particular package.

name = "dotscad"

description = "dotscad python tools for OpenSCAD"

author = "Chris Petersen"

# author_email = "sorry@youdontget.this"

url = "https://github.com/dotscad/python-dotscad"

license = "MIT License"

keywords = "dotscad,OpenSCAD"

classifiers = [
    # CHANGEME: Update the classifiers as appropriate
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Build Tools",
    f"License :: {license}",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]

setup_requires = ()

install_requires = setup_requires + ()

tests_require = install_requires  # + ("pytest", "pytest-runner", "tox")

dependency_links = (
    # CHANGEME: Install any private dependency links here.
)

entry_points = {
    # CHANGEME: Set up any appropriate entry points here, e.g. console_scripts
    # 'console_scripts': [
    #     'sample_script = sample_package.example_script:main',
    # ],
}

# Setting this to true will make sure any binaries in MANIFEST.in
# get included with the package when it is distributed.
# See: http://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files
include_package_data = True

# Minimum python version required
min_python_version = (3, 6)

################################################
# Please try not to touch things below this line
################################################

if sys.version_info < min_python_version:
    error = f"ERROR: {name} requires Python Version {min_python_version} or above...exiting."
    print >>sys.stderr, error
    sys.exit(1)

HERE = os.path.abspath(os.path.dirname(__file__))
MODULE_PATH = os.path.join(HERE, name.replace("-", "_"))

# Get the long description from the README file
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Load the version by reading the package directly, so we don't run into
# dependency loops by importing it into setup.py
version = None
with open(os.path.join(MODULE_PATH, "__init__.py")) as file:
    for line in file:
        m = re.search(r"\b(?:__version__|VERSION)\b\s*=\s*(.+?)$", line)
        if m:
            version = eval(m.group(1))
            break
assert version is not None, "Couldn't find version string."


setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    # author_email=author_email,
    url=url,
    license=license,
    classifiers=classifiers,
    keywords=keywords,
    setup_requires=setup_requires,
    # This package only installs its base module, and a bunch of dependencies
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    include_package_data=include_package_data,
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points=entry_points,
    # In order to keep tox *and* setup happy, we need to define the test requirements twice...
    extras_require={"test": tests_require},
    tests_require=tests_require,
    test_suite="py.test",
)
