#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from isbntools.app import quiet_errors, doi


def usage():
    print('Usage: isbn_doi ISBN')


def main(args=None):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv[1:] if not args else args
        print(doi(args))
    except:
        usage()
