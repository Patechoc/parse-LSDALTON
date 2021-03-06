#!/usr/bin/env python

import os, sys
import subprocess as subproc
from setuptools import setup, find_packages
from setuptools.command.install import install

'''
virtualenv and pip: http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/

nice blog post advising on "Developing Reusable Things or How Not to Repeat Yourself":
"abstract dependencies in your setup.py and concrete dependencies in your requirements.txt"
https://caremad.io/2013/07/setup-vs-requirement/
'''

os.system("git submodule init; git submodule update")

setup(
    name="parseLSDALTON",
    version="0.1",
    description='parsing, comparing and exporting LSDALTON inputs and outputs',
    author='Patrick Merlot',
    author_email='patrick.merlot@gmail.com',
    url='https://github.com/Patechoc/parse-LSDALTON',
    keywords = 'LSDALTON parse output topology molecule',
    license = 'MIT',

    packages = find_packages(),

    # install_requires=[
    #     "argparse",
    #     "wsgiref",
    #     "numpy",
    #     "pandas",
    #     "pyparsing",
    #     "pytest",
    #     "plotly",
    # ],

    #dependency_links = [
    #    ""
    #],
    # ...
)
