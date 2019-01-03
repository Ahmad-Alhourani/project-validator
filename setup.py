#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup

setup(name='ValidatorManager',
      version='1.0',
      description='',
      author='Devyzer Team',
      author_email='hello@xlabtechs.com',
      url='https://gitlab.com/devyzer/project-validator.git',
      packages=find_packages(),
      install_requires=['inflect', 'colander', 'translationstring',
                        '-e git://github.com/Ahmad-Alhourani/project-configuration-manager.git#egg=ProjectConfigurationManager'
                        ],
      )
