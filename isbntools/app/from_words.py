#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from isbntools import isbn_from_words, quiet_errors


def main():
    sys.excepthook = quiet_errors

    if len(sys.argv) != 2:
        print(("Usage: %s 'AUTHOR TITLE'" % sys.argv[0]))
        sys.exit(1)

    print((isbn_from_words(sys.argv[1])))
