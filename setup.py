import os

from setuptools import find_packages
from setuptools import setup


setup(
    name='commander',
    version='1.0.0',
    description='Parallel command exectution framework',
    author='Igor Shishkin',
    author_email='ishishkin@mirantis.com',
    zip_safe=False,
    include_package_data=True,
    packages=['commander'],
    scripts=['bin/cmd.py'],
    install_requires=[
        'pyzabbix',
        'readline',
        'termcolor',
    ]
)
