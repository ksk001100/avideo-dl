#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'avideo_dl',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.1')

setup(
    name="avideo_dl",
    version=version,
    url='https://github.com/KeisukeToyota/avideo_dl',
    author='KeisukeToyota',
    author_email='hm.pudding0715@gmail.com',
    maintainer='KeisukeToyota',
    maintainer_email='hm.pudding0715@gmail.com',
    description='',
    long_description=readme,
    packages=find_packages(),
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points="""
        # -*- Entry points: -*-
        [console_scripts]
        avideo_dl = avideo_dl.scripts.command:main
    """,
)
