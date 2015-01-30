#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import mask


def usage():
    print('Usage: isbn_mask ISBN')
    return 1


def main(isbn=None):
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        output = mask(isbn)
        if output:
            print(output)
    except:
        return usage()
