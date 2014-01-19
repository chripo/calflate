#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import calflate.__main__

SRC=('https://calendar,source.com/foo.ics/', 'test', 'test')
DST=('https://my.radicale.org/test/test.ics/', 'test', 'test')

calflate.__main__.run(SRC, DST)

