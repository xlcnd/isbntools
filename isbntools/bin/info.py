#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import info


def usage():
    print('Usage: isbn_info ISBN')
    return 1


def main(isbn=None):
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        print((info(isbn)))
    except:
        return usage()
