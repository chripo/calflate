#!/usr/bin/env python

from setuptools import setup

setup(
    name='calflate',
    version='0.3',
    description='copy / import icalendar events',
    author='Christoph Polcin',
    author_email='labs@polcin.de',
    url='https://github.com/chripo/calflate',
    license='BSD',
    platforms='Any',
    packages=['calflate'],
    provides=['calflate'],
    scripts=['bin/calflate'],
    keywords=['calendar', 'addressbook', 'CalDAV', 'CardDAV'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent'
    ],
)
