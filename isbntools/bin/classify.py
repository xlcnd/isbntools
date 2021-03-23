# -*- coding: utf-8 -*-

import sys
from json import dumps

from ..app import classify, quiet_errors

PREFIX = 'isbn_'


def usage(prefix=PREFIX):
    print('Usage: %sclassify ISBN' % prefix)
    return 1


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isbn = sys.argv[1] if not isbn else isbn[1]
        data = classify(isbn)
        if data:
            print(dumps(data, indent=4))
        else:
            raise Exception('No data')
    except:
        usage(prefix)
