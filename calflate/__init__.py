# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-16

from base64 import encodestring
from icalendar import Calendar, Event
from urllib2 import Request, urlopen

def calflate(SRC, DST):
    src = get_events(get_calendar(*SRC))
    dstset = uid_set(get_events(get_calendar(*DST)))
    for s in src:
        if s.get('UID') not in dstset:
            try:
                put_event(DST, s)
                dstset.add(s.get('UID'))
            except:
                print('fail to put event: %s [%s]' % \
                    (s.get('SUMMARY', ""), s.get('UID')))

def put_event(DST, e):
    print("put event: %s [%s]" % (e.get('SUMMARY', None), e.get('UID')))
    cal = new_calendar()
    cal.add_component(e)
    r = url_usr_request(DST[0], DST[1], DST[2], cal.to_ical())
    r.add_header('Content-Type', 'text/calendar')
    r.get_method = lambda: 'PUT'
    urlopen(r)

def uid_set(events):
    return set(e.get('UID') for e in events)

def get_events(cal):
    for c in cal.walk():
        if c.name == 'VEVENT' and c.get('UID', None):
            yield c

def get_calendar(url, usr=None, pw=None, *args):
    r = url_usr_request(url, usr, pw, *args)
    return Calendar.from_ical(urlopen(r).read())

def url_usr_request(url, usr=None, pw=None, *args):
    r = Request(url, *args)
    if usr and pw:
        base64string = encodestring('%s:%s' % (usr, pw)).replace('\n', '')
        r.add_header("Authorization", "Basic %s" % base64string)
    return r

def new_calendar():
    c = Calendar()
    c.add('PRODID', '-//Radicale//NONSGML Radicale Server//EN')
    c.add('VERSION', '2.0')
    return c

