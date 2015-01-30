#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import quiet_errors, EAN13


def usage():
    print('Usage: isbn_EAN13 ISBN')
    return 1


def main(isbn=None):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        print(EAN13(isbn))
    except:
        usage()
