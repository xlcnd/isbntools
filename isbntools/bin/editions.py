# -*- coding: utf-8 -*-

import sys

from ..app import editions, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %seditions ISBN' % prefix)
    return 1


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        for ib in editions(isbn, service='any'):
            print(ib)
    except:
        return usage(prefix)
