#!/usr/bin/env python

from setuptools import setup

setup(name='calflate',
    version='0.1',
    description='Simple script to merge calendar events into online a calendar.',
    author='Christoph Polcin',
    author_email='labs@polcin.de',
    url='https://github.com/chripo/calflate',
    license = "BSD",
    packages=['calflate'],
    install_requires=[
        'icalendar'
    ],
    classifiers=[
        'Development Status :: 1 - Planning'
    ],
)
