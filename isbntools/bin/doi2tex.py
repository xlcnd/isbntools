# -*- coding: utf-8 -*-
# noqa

import sys

from ..app import doi2tex, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %sdoi2tex DOI' % prefix)
    return 1


def main(doi=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        doi = sys.argv[1] if not doi else doi[1]
        data = doi2tex(doi)
        if data:
            print(data)
    except:
        usage(prefix)
