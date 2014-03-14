# -*- coding: utf-8 -*-

import sortedcontainers
from setuptools import setup, find_packages

with open('README.rst') as fptr:
    readme = fptr.read()

with open('LICENSE') as fptr:
    license = fptr.read()

setup(
    name=sortedcontainers.__title__,
    version=sortedcontainers.__version__,
    description='Sorted container data types.',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='https://github.com/grantjenks/sortedcontainers',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
