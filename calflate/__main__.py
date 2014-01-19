# -*- encoding: utf-8 -*-

# AUTHOR: http://www.christoph-polcin.com
# LICENSE: FreeBSD License
# CREATED: 2014-01-16

from optparse import OptionParser
from . import calflate

def run(SRC, DST):
    parser = OptionParser()
    parser.add_option(
        '-p', '--purge', action="store_true", default=False,
        help='purge orphan items')

    options = parser.parse_args()[0]

    calflate(SRC, DST, options)

if __name__ == '__main__':
    run(SRC, DST)
