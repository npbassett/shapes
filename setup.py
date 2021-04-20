#!/usr/bin/env python
"""
File: setup.py
Author: Neil Bassett
Date: 19 April 2021

Description: Installs ASHES.
"""
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='ashes', version='0.1',\
    description='Angular Solver for Horizon from Elevation Sets',\
    author='Neil Bassett',\
    author_email='neil.bassett@colorado.edu',\
    packages=['ashes'])

ASHES_env = os.getenv('ASHES')
cwd = os.getcwd()
if not ASHES_env:
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
            print("\n    export ASHES={0}".format(cwd))
        elif re.search('csh', shell):
            print("Looks like you're using csh, so add the following to " +\
                "your .cshrc:")
            print("\n    setenv ASHES {!s}".format(cwd))
    print("\nGood luck!")
    print("#" * 78)
    print("\n")
elif ASHES_env != cwd:
    print("\n")
    print("#" * 78)
    print("It looks like you've already got an ASHES environment variable " +\
        "set but it's \npointing to a different directory:")
    print("\n    ASHES={!s}".format(ASHES_env))
    print("\nHowever, we're currently in {!s}.\n".format(cwd))
    print("Is this a different ashes install (might not cause problems), or " +\
        "perhaps just")
    print("a typo in your environment variable?")
    print("#" * 78)
    print("\n")
