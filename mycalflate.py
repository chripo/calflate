#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import calflate

SRC=('https://calendar,source.com/foo.ics/', 'test', 'test')
DST=('https://my.radicale.org/test/test.ics/', 'test', 'test')

calflate.run(SRC, DST)

