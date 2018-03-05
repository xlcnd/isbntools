# -*- coding: utf-8 -*-

import sys

from ..app import isbn_from_words, quiet_errors

PREFIX = 'isbn_'
PY2 = sys.version < '3'


def usage(prefix=PREFIX):
    print("Usage: %sfrom_words 'AUTHOR TITLE'" % prefix)
    return 1


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv if not args else args
    except:
        return usage(prefix)
    if len(args) < 2:
        return usage(prefix)

    try:
        if PY2:
            words = args[1].decode(sys.stdin.encoding)
            words = words.encode('UTF-8')
        else:
            # FIXME see: isbnlib.dev.webservice
            words = args[1]
        print(isbn_from_words(words))
        return 0
    except:
        return usage(prefix)
