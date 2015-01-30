#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import quiet_errors, doi


def usage():
    print('Usage: isbn_doi ISBN')
    return 1


def main(args=None):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv[1] if not args else args[1]
        print(doi(args))
    except:
        usage()
