#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from calflate import calflate

SRC=('https://calendar,source.com/foo.ics/', 'test', 'test')
DST=('https://my.radicale.org/test/test.ics/', 'test', 'test')

if __name__ == '__main__':
    calflate(SRC, DST)

