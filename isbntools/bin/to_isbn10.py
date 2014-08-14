#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from isbntools import to_isbn10


def usage():
    print('Usage: to_isbn10 ISBN13')
    sys.exit(1)


def main():
    try:
        print((to_isbn10(sys.argv[1])))
    except:
        usage()
