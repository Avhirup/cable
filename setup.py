#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='cable',
      version='0.0.3',
      description='This package has components  for preprocessing',
      author='Avhirup',
      author_email='avhirupchakraborty@gmail.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
    )
