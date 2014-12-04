# coding:utf-8

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 6):
    error = 'ERROR: rongcloud-sdk requires Python Version 2.6 or above.'
    print >> sys.stderr, error
    sys.exit(1)

long_description="""
    The RongCloud Server Python SDK provides Python APIs .

    1. http://docs.rongcloud.cn/server.html
  """

setup(
    name='rongcloud',
    version='0.0.1',
    description='Software Development Kit for RongCloud Server.',
    long_description=long_description,
    install_requires=['requests'],
    keywords='rongcloud sdk',
    author='rongcloud',
    author_email = 'fengyadong@feinno.com',
    url='http://docs.rongcloud.cn/server.html',
    packages=['rongcloud'],
    package_dir={'rongcloud': 'rongcloud'},
    namespace_packages=['rongcloud'],
    include_package_data=True,
)
