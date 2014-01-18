# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-16

from base64 import encodestring
from os import path
import re
from urllib2 import Request, urlopen

def calflate(SRC, DST):
    events = get_events(get_calendar(*SRC))
    dstmap = uid_seq_map(get_events(get_calendar(*DST)))
    for event in events:
        try:
            if event[2] not in dstmap or event[3] > dstmap[event[2]]:
                put_event(DST, event)
                dstmap[event[2]] = event[3]
        except Exception as ex:
            print('fail to put event: %s [%s] due to Exception: %s' % \
                (event[2], event[1], ex))

def put_event(DST, event):
    print("PUT event: %s [%s]" % (event[2], event[1]))
    data = new_calendar(event)
    r = url_usr_request(path.join(DST[0], "%s.ics" % event[2]), DST[1], DST[2], data)
    r.add_header('Content-Type', 'text/calendar')
    r.get_method = lambda: 'PUT'
    urlopen(r)

def uid_seq_map(events):
    return {e[2]:e[3] for e in events}

def get_events(calendar):
    r'''yield (data, type, uid, sequence)'''
    reEvent = re.compile(r'^(BEGIN:(VEVENT|VTODO|VJOURNAL)$.*?^UID:(.+?)$.*?^END:\2$)', re.S | re.M)
    reSeq = re.compile(r'^SEQUENCE:(\d+?)$', re.M)
    for m in reEvent.finditer(calendar):
        sq = reSeq.search(m.group(0))
        yield m.groups() + (int(sq.group(1)) if sq else 0, )

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

