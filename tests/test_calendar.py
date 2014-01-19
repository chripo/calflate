# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-19

import calflate


def test_new_empty_collection():
    data = calflate.new_collection(("", "VEVENT", ))
    assert data == 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nEND:VCALENDAR\r\n'


def test_new_collection():
    data = calflate.new_collection(("UID:12345", "VEVENT", ))
    assert data == 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nUID:12345\r\nEND:VCALENDAR\r\n'


def test_get_items():
    items = calflate.get_items('''BEGIN:VEVENT
SUMMARY:foo
UID:01234-01234-01234-01234
SEQUENCE:2
END:VEVENT
BEGIN:VTODO
SUMMARY:bar
UID:2222
END:VTODO
''')
    item = next(items)
    assert len(item) == 4
    assert item[0] == \
        'BEGIN:VEVENT\nSUMMARY:foo\nUID:01234-01234-01234-01234\nSEQUENCE:2\nEND:VEVENT'
    assert item[1] == 'VEVENT'
    assert item[2] == '01234-01234-01234-01234'
    assert item[3] == 2

    item = next(items)
    assert len(item) == 4
    assert item[0] == 'BEGIN:VTODO\nSUMMARY:bar\nUID:2222\nEND:VTODO'
    assert item[1] == 'VTODO'
    assert item[2] == '2222'
    assert item[3] == 0

    try:
        item = next(items)
        assert 0
    except StopIteration:
        assert 1
