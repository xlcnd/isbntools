# -*- coding: utf-8 -*-


import sys

from ..app import isbn_from_words, quiet_errors

PREFIX = 'isbn_'


def usage(args, prefix=PREFIX):
    print(("Usage: %s%s 'AUTHOR TITLE'" % (prefix, args[0])))
    return 1


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv if not args else args
    except:
        return usage(args, prefix)
    if len(args) < 2:
        return usage(args, prefix)
    print((isbn_from_words(args[1])))
