# -*- encoding: utf-8 -*-

# LICENSE: FreeBSD License
# CREATED: 2014-01-16

__author__ = 'Christoph Polcin <labs@polcin.de>'
__url__ = 'https://github.com/chripo/calflate/'

from base64 import encodestring
from os import path
import re
from urllib2 import Request, urlopen


def calflate(SRC, DST, options):
    srcCollection, srcType = get_collection(*SRC)
    dstCollection, dstType = get_collection(*DST)
    if srcType != dstType or not srcType:
        print('collection types dosen\'t match %s != %s' % (srcType, dstType))
        return
    items = get_items(srcCollection, srcType)
    if hasattr(options, 'uid_from') and hasattr(options, 'uid_to'):
        items = replace_uid(items, options.uid_from, options.uid_to)
    dstmap = uid_seq_map(get_items(dstCollection, srcType))
    srcuid = set()
    for item in items:
        srcuid.add(item[2])
        try:
            if item[2] not in dstmap or item[3] > dstmap[item[2]]:
                put_item(DST, item, options)
                dstmap[item[2]] = item[3]
            elif options.verbose:
                print('skip item %s [%s]' % (item[2], item[1]))
        except Exception as ex:
            print('fail to put item: %s [%s] due to Exception: %s' %
                  (item[2], item[1], ex))
    if options.purge:
        uids = set(dstmap.keys()) - srcuid
        for uid in uids:
            try:
                delete_item(DST, uid, srcType, options)
            except Exception as ex:
                print('fail to delete item: %s due to Exception: %s' %
                      (uid, ex))


def delete_item(DST, uid, ctype, options):
    p = '%s.%s' % (uid, 'vcf' if ctype == 'VCARD' else 'ics')
    print('DELETE item: %s' % p)
    if options.dryrun:
        return
    r = url_usr_request(path.join(DST[0], p), DST[1], DST[2])
    r.get_method = lambda: 'DELETE'
    if not is_ok(urlopen(r)):
        raise IOError


def put_item(DST, item, options):
    print('PUT item: %s [%s]' % (item[2], item[1]))
    if options.dryrun:
        return
    data = new_collection(item)
    if item[1] == 'VCARD':
        p = '%s.vcf' % item[2]
        ctype = 'text/vcard'
    else:
        p = '%s.ics' % item[2]
        ctype = 'text/calendar'
    r = url_usr_request(path.join(DST[0], p), DST[1], DST[2], data)
    r.add_header('Content-Type', ctype)
    r.get_method = lambda: 'PUT'
    if not is_ok(urlopen(r)):
        raise IOError


def is_ok(response):
    if not response or response.getcode() < 200 or response.getcode() >= 300:
        return False
    return True


def uid_seq_map(items):
    return {e[2]: e[3] for e in items}


def get_items(collection, filter_ctype=None):
    '''yield (data, type, uid, sequence)'''

    reItem = re.compile(
        r'^(BEGIN:(VEVENT|VTODO|VJOURNAL|VCARD)$.*?^UID:(.+?)$.*?^END:\2$)', re.S | re.M)
    reSeq = re.compile(r'^SEQUENCE:(\d+?)$', re.M)
    reRev = re.compile(r'^REV:(.+?)$', re.M)
    for m in reItem.finditer(collection):
        data, ctype, uid = m.groups()
        if ctype == 'VCARD':
            rev = reRev.search(data)
            # TODO: check if all date values are sortable
            rev = rev.group(1) if rev else '0'
        else:
            rev = reSeq.search(data)
            rev = int(rev.group(1)) if rev else 0
        yield (data, ctype, uid, rev, )


def replace_uid(items, uidfrom, uidto):
    '''relaces all occurrences of UID based on a regular expression.
     yield (data, type, uid, sequence)'''

    print('UID replace pattern: %s -> %s' % (uidfrom, uidto))
    reUid = re.compile(uidfrom)
    for data, ctype, ouid, rev in items:
        uid = reUid.sub(uidto, ouid)
        if uid != ouid:
            data = data.replace(ouid, uid)
        print('UID %s -> %s' % (ouid, uid))
        yield data, ctype, uid, rev


def collection_with_ctype(collection):
    reType = re.compile(r'BEGIN:(VCALENDAR|VCARD)')
    m = reType.search(collection)
    return collection, m.group(1) if m else None


def get_collection(url, usr=None, pw=None, *args):
    '''return data, type'''
    def r_fac():
        return url_usr_request(url, usr, pw, *args)

    try:
        return collection_with_ctype(get_collection_from_file(url))
    except:
        pass

    try:
        return collection_with_ctype(get_collection_by_GET(r_fac))
    except:
        pass

    raise IOError('fail read collection from: \'%s\'' % url)


def get_collection_from_file(url):
    if url.startswith('~'):
        url = path.expanduser(url)
    if path.isfile(url):
        with open(url, 'r') as f:
            c = f.read(20)
            if c.find('BEGIN:', 0, min(len(c), 20)) != -1:
                f.seek(0)
                return f.read()
            else:
                print('faulty input: %s' % url)
                return ''
    raise IOError('file not found')


def get_collection_by_GET(r_fac):
    res = urlopen(r_fac())
    if res.getcode() == 200:
        c = res.read()
        if c.find('BEGIN:', 0, min(len(c), 20)) != -1:
            return c
    raise Exception('fail to find BEGIN block')


def url_usr_request(url, usr=None, pw=None, *args):
    r = Request(url, *args)
    if usr and pw:
        base64string = encodestring('%s:%s' % (usr, pw)).replace('\n', '')
        r.add_header('Authorization', 'Basic %s' % base64string)
    return r


def new_collection(item):
    if item[1] == 'VCARD':
        c = item[0]
    else:
        c = r'''BEGIN:VCALENDAR
VERSION:2.0
%s
END:VCALENDAR
''' % item[0]
    return c.replace('\n', '\r\n').replace('\r\n\r\n', '\r\n')
