# -*- coding: utf-8 -*-

import sys

from ..app import quiet_errors, to_isbn13

PREFIX = ''


def usage(prefix=PREFIX):
    print('Usage: %sto_isbn13 ISBN10' % prefix)
    return 1


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        isbn13 = to_isbn13(isbn)
        if isbn13:
            print(isbn13)
    except:
        return usage(prefix)
