# -*- coding: utf-8 -*-

import sys

from ..app import cover, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %scover ISBN' % prefix)
    return 1


def main(args=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv[1] if not args else args[1]
        lnks = cover(args)
        for k, v in lnks.items():
            print("%s:  %s" % (k, v))
    except:
        usage(prefix)
