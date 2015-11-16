#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='rongcloud-server-sdk-python',
    author='Rong Cloud',
    author_email='support@rongcloud.cn',
    version='0.0.1',
    description='Rong Cloud Server SDK in Python.',
    url='https://github.com/rongcloud/server-sdk-python',
    package=['rong'],
    zip_safe=False,
    install_requires=[
        'requests'
    ]
)
