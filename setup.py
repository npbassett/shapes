#!/usr/bin/env python
"""
File: setup.py
Author: Neil Bassett
Date: 19 April 2021

Description: Installs SHAPES.
"""
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='shapes', version='0.1',\
    description='Simulating Horizon Angle Profile from Elevation Sets',\
    author='Neil Bassett',\
    author_email='neil.bassett@colorado.edu',\
    packages=['shapes'])

SHAPES_env = os.getenv('SHAPES')
cwd = os.getcwd()
if not SHAPES_env:
    import re
    shell = os.getenv('SHELL')
    print("\n")
    print("#" * 78)
    print("It would be in your best interest to set an environment variable")
    print("pointing to this directory.\n")
    if shell:
        if re.search('bash', shell):
            print("Looks like you're using bash, so add the following to " +\
                "your .bashrc:")
            print("\n    export SHAPES={0}".format(cwd))
        elif re.search('csh', shell):
            print("Looks like you're using csh, so add the following to " +\
                "your .cshrc:")
            print("\n    setenv SHAPES {!s}".format(cwd))
    print("\nGood luck!")
    print("#" * 78)
    print("\n")
elif SHAPES_env != cwd:
    print("\n")
    print("#" * 78)
    print("It looks like you've already got an shapes environment variable " +\
        "set but it's \npointing to a different directory:")
    print("\n    SHAPES={!s}".format(shapes_env))
    print("\nHowever, we're currently in {!s}.\n".format(cwd))
    print("Is this a different shapes install (might not cause problems), or " +\
        "perhaps just")
    print("a typo in your environment variable?")
    print("#" * 78)
    print("\n")
