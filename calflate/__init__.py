# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-16

from base64 import encodestring
import re
from urllib2 import Request, urlopen

def calflate(SRC, DST):
    events = get_events(get_calendar(*SRC))
    dstset = uid_set(get_events(get_calendar(*DST)))
    for event in events:
        if event[2] not in dstset:
            try:
                put_event(DST, event)
                dstset.add(event[2])
            except Exception as ex:
                print('fail to put event: %s [%s] due to Exception: %s' % \
                    (event[2], event[1], ex))

def put_event(DST, event):
    print("put event: %s [%s]" % (event[2], event[1]))
    data = new_calendar(event)
    r = url_usr_request(DST[0], DST[1], DST[2], data)
    r.add_header('Content-Type', 'text/calendar')
    r.get_method = lambda: 'PUT'
    urlopen(r)

def uid_set(events):
    return set(e[2] for e in events)

def get_events(calendar):
    r'''yield (data, type, uid)'''
    event = re.compile(r'^(BEGIN:(VEVENT|VTODO|VJOURNAL)$.*?^UID:(.+?)$.*?^END:\2$)', re.S | re.M)
    for m in event.finditer(calendar):
        yield m.groups()

def get_calendar(url, usr=None, pw=None, *args):
    r = url_usr_request(url, usr, pw, *args)
    content = urlopen(r).read()
    return content

def url_usr_request(url, usr=None, pw=None, *args):
    r = Request(url, *args)
    if usr and pw:
        base64string = encodestring('%s:%s' % (usr, pw)).replace('\n', '')
        r.add_header("Authorization", "Basic %s" % base64string)
    return r

def new_calendar(event):
    c = r'''BEGIN:VCALENDAR
VERSION:2.0
%s
END:VCALENDAR
    ''' % event[0]
    return c.replace('\n', '\r\n')

