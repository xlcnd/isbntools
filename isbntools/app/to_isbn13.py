# -*- coding: utf-8 -*-

import sys
from isbntools import to_isbn13


def usage():
    print('Usage: to_isbn13 ISBN10')
    sys.exit(1)


try:
    ISBN10 = sys.argv[1]
except:
    usage()


def run(isbn10):       # <-- Test this function
    return to_isbn13()


def main():
    try:
        print(run(ISBN10))
    except:
        usage()
