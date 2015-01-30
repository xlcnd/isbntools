#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import get_canonical_isbn


def usage():
    print('Usage: isbn_validate ISBN')
    return 1


def main(isbn=None):
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        print((get_canonical_isbn(isbn)))
    except:
        return usage()
