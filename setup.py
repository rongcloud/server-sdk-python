#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
setup(
    name='rongcloud',
    version='2.0.1',
    packages=find_packages(),
    install_requires = ['requests>=2.10.0'],
    description='Rong Cloud Server SDK in Python.',
    url='https://github.com/rongcloud/server-sdk-python',
    )
