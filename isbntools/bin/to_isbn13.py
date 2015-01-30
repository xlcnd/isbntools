#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import to_isbn13


def usage():
    print('Usage: to_isbn13 ISBN10')
    return 1


def main(isbn=None):
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        print(to_isbn13(isbn))
    except:
        return usage()
