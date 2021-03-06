#!/usr/bin/env python

"""
Call `pip install -e .` to install package locally for testing.
"""

from setuptools import setup

# build command
setup(
    name="records",
    version="0.0.1",
    author="Roí A.k.",
    author_email="ra3040@columbia.edu",
    description="Package to query GBIF",
    packages=["records"],
    license="GPLv3",
    install_requires=["pandas"],
    classifiers = ["Programming Language :: Python :: 3"],
    entry_points={
        'console_scripts': ['records = records.records:Records']
    }
)