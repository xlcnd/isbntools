# -*- coding: utf-8 -*-

import sys

from ..app import ean13, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %sEAN13 ISBN' % prefix)
    return 1


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        print(ean13(isbn))
    except:
        usage(prefix)
