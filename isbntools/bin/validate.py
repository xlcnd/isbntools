#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import get_canonical_isbn, quiet_errors

PREFIX = ''

def usage(prefix=PREFIX):
    print('Usage: %svalidate ISBN' % prefix)
    return 1


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        out = get_canonical_isbn(isbn)
        if out:
            print(out)
    except:
        return usage(prefix)
