# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

"""Describe the distribution to distutils."""

# Import third-party modules
import os
from setuptools import find_packages
from setuptools import setup

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
README_PATH = os.path.join(ROOT_PATH, 'README.md')

requires = [
    'dayu_widgets >= 0.0.1',
    'strack-api >=1.0.0',
    'PyYAML >= 5.0'
]

setup(
    name='strack-connect',
    author='weijer',
    url='https://github.com/cgpipline/strack-connect',
    license='Apache License (2.0)',
    version='0.0.1',
    author_email='weiwei163@foxmail.com',
    description=('Connect for strack.'),
    long_description=open(README_PATH, 'r', encoding='UTF-8').read(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
