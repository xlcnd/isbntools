#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from isbntools import get_canonical_isbn


def usage():
    print('Usage: isbn_validate ISBN')
    sys.exit(1)


def main():
    try:
        print((get_canonical_isbn(sys.argv[1])))
    except:
        usage()
