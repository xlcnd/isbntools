#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from isbntools import quiet_errors, doi


def usage():
    print('Usage: isbn_doi ISBN')


def main():
    sys.excepthook = quiet_errors
    try:
        print(doi(sys.argv[1]))
    except:
        usage()
