# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-16

from base64 import encodestring
from optparse import OptionParser
from os import path
import re
from urllib2 import Request, urlopen

def calflate(SRC, DST, options):
    items = get_items(get_calendar(*SRC))
    dstmap = uid_seq_map(get_items(get_calendar(*DST)))
    srcuid = set()
    for item in items:
        srcuid.add(item[2])
        try:
            if item[2] not in dstmap or item[3] > dstmap[item[2]]:
                put_item(DST, item, options)
                dstmap[item[2]] = item[3]
        except Exception as ex:
            print('fail to put item: %s [%s] due to Exception: %s' % \
                (item[2], item[1], ex))
    if options.purge:
        uids = set(dstmap.keys()) - srcuid
        for uid in uids:
            try:
                delete_item(DST, uid, options)
            except Exception as ex:
                print('fail to delete item: %s due to Exception: %s' % \
                    (uid, ex))

def delete_item(DST, uid, options):
    print("DELETE item: %s" % uid)
    if options.dryrun:
        return
    r = url_usr_request(path.join(DST[0], "%s.ics" % uid), DST[1], DST[2])
    r.get_method = lambda: 'DELETE'
    is_ok(urlopen(r))

def put_item(DST, item, options):
    print("PUT item: %s [%s]" % (item[2], item[1]))
    if options.dryrun:
        return
    data = new_calendar(item)
    r = url_usr_request(path.join(DST[0], "%s.ics" % item[2]), DST[1], DST[2], data)
    r.add_header('Content-Type', 'text/calendar')
    r.get_method = lambda: 'PUT'
    is_ok(urlopen(r))

def is_ok(response):
    if response.getcode() < 200 or response.getcode() >= 300:
        raise AssertionError(status)

def uid_seq_map(items):
    return {e[2]:e[3] for e in items}

def get_items(calendar):
    r'''yield (data, type, uid, sequence)'''
    reItem = re.compile(r'^(BEGIN:(VEVENT|VTODO|VJOURNAL)$.*?^UID:(.+?)$.*?^END:\2$)', re.S | re.M)
    reSeq = re.compile(r'^SEQUENCE:(\d+?)$', re.M)
    for m in reItem.finditer(calendar):
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

def new_calendar(item):
    c = r'''BEGIN:VCALENDAR
VERSION:2.0
%s
END:VCALENDAR
    ''' % item[0]
    return c.replace('\n', '\r\n')

def run(SRC, DST):
    parser = OptionParser()
    parser.add_option(
        '-n', '--dry-drun', action="store_true", default=False,
        help='dry run', dest='dryrun')
    parser.add_option(
        '-p', '--purge', action="store_true", default=False,
        help='purge orphan items')

    options = parser.parse_args()[0]

    calflate(SRC, DST, options)

if __name__ == '__main__':
    run(SRC, DST)
