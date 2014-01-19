# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-19

import calflate


def test_new_empty_collection():
    data = calflate.new_collection(("", "VCARD", ))
    assert data == ''


def test_new_collection():
    data = calflate.new_collection(("UID:12345", "VCARD", ))
    assert data == 'UID:12345'
    data = calflate.new_collection(("UID:12345\nREV:2011-01-02", "VCARD", ))
    assert data == 'UID:12345\r\nREV:2011-01-02'
    data = calflate.new_collection(("UID:12345\n\nREV:2011-01-02", "VCARD", ))
    assert data == 'UID:12345\r\nREV:2011-01-02'


def test_get_items():
    items = calflate.get_items('''BEGIN:VCARD
VERSION:3.0
N:Gump;Forrest;Mr.
UID:01234-01234-01234-01234
REV:2008-04-24T19:52:43Z
END:VCARD
BEGIN:VCARD
VERSION:4.0
N:Gump;Forrest;Mr.
UID:3333-3444-55
END:VCARD
''')
    item = next(items)
    assert len(item) == 4
    assert item[0] == '''BEGIN:VCARD\nVERSION:3.0\nN:Gump;Forrest;Mr.\n\
UID:01234-01234-01234-01234\nREV:2008-04-24T19:52:43Z\nEND:VCARD'''
    assert item[1] == 'VCARD'
    assert item[2] == '01234-01234-01234-01234'
    assert item[3] == '2008-04-24T19:52:43Z'

    item = next(items)
    assert len(item) == 4
    assert item[0] == 'BEGIN:VCARD\nVERSION:4.0\nN:Gump;Forrest;Mr.\nUID:3333-3444-55\nEND:VCARD'
    assert item[1] == 'VCARD'
    assert item[2] == '3333-3444-55'
    assert item[3] == '0'

    try:
        item = next(items)
        assert 0
    except StopIteration:
        assert 1
