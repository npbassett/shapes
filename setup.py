#!/usr/bin/env python
"""
File: setup.py
Author: Neil Bassett
Date: 19 April 2021

Description: Installs ashes.
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='ashes', version='0.1',\
    description='Angular Solver for Horizon from Elevation Sets',\
    author='Neil Bassett',\
    author_email='neil.bassett@colorado.edu',\
    packages=['ashes'])
