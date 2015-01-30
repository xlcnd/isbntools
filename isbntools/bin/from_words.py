#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

from isbntools.app import isbn_from_words, quiet_errors


def usage(args):
    print(("Usage: %s 'AUTHOR TITLE'" % args[0]))
    return 1


def main(args=None):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv if not args else args
    except:
        return usage(args)
    if len(args) < 2:
        return usage(args)
    print((isbn_from_words(args[1])))
