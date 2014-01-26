#!/usr/bin/env python

from calflate.__main__ import VERSION
from os.path import join, dirname
from setuptools import setup

setup(
    name='calflate',
    version=VERSION,
    description='import external CalDAV and CardDAV entries',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='Christoph Polcin',
    author_email='labs@polcin.de',
    url='https://github.com/chripo/calflate/',
    download_url='https://github.com/chripo/calflate/tarball/%s' % VERSION,
    license='BSD revised',
    platforms='Any',
    packages=['calflate'],
    provides=['calflate'],
    scripts=['bin/calflate'],
    keywords=['calendar', 'addressbook', 'CalDAV', 'CardDAV'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ],
)
