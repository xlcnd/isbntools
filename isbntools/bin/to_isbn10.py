# -*- coding: utf-8 -*-

import sys

from ..app import quiet_errors, to_isbn10

PREFIX = ''


def usage(prefix=PREFIX):
    print('Usage: %sto_isbn10 ISBN13' % prefix)
    return 1


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        isbn10 = to_isbn10(isbn)
        if isbn10:
            print(isbn10)
    except:
        return usage(prefix)
