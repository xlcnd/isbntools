#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from isbntools import editions, quiet_errors


def usage():
    print('Usage: isbn_editions ISBN')


def main():
    sys.excepthook = quiet_errors
    try:
        for ib in editions(sys.argv[1]):
            print(ib)
    except:
        usage()
