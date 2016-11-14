# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name = 'email-parser',
    version = '1.0.0',
    packages = (['email_parser']),
    package_data={
      '': ['*.json'],
    },
    entry_points = {
        'console_scripts': [
            'email_parser = email_parser.process:main',
        ],
    },
    author = 'Myagkikh Konstantin',
    author_email = 'k.myagkikh@gmail.com',
)
