# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-20

import calflate


def test_is_ok():
    class StatusMock:
        def __init__(self, code):
            self.code = code

        def getcode(self):
            return self.code

    assert not calflate.is_ok(None)
    assert not calflate.is_ok(StatusMock(100))
    assert not calflate.is_ok(StatusMock(300))

    assert calflate.is_ok(StatusMock(200))
    assert calflate.is_ok(StatusMock(207))
