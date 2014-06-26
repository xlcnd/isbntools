#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from isbntools import to_isbn13


def usage():
    print('Usage: to_isbn13 ISBN10')
    sys.exit(1)


def main():
    try:
        print((to_isbn13(sys.argv[1])))
    except:
        usage()
