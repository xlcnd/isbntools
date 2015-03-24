# -*- coding: utf-8 -*-

import re
import sys

from ..app import get_canonical_isbn, get_isbnlike, quiet_errors

PREFIX = ''


def usage(prefix=PREFIX):
    print('Usage: %svalidate ISBN' % prefix)
    if PREFIX:
        print('OR')
        print('       cat ISBNs| isbn_validate')
    return 1


def do_pipe():
    """Validate ISBNs from sys.stdin."""
    # check if pipe
    if sys.stdin.isatty():
        print('Usage:\n   cat ISBNs | isbn_validate')
        return 1
    for line in sys.stdin:
        line = line.strip()
        buf = re.sub(r"\[|\]|'|-", "", repr(get_isbnlike(line)))
        buf = buf.strip()
        if ',' in buf:
            for b in buf.split(','):
                b = get_canonical_isbn(b.strip())
                if b:
                    print(b)
        else:
            buf = get_canonical_isbn(buf)
            if buf:
                print(buf)
    return 0


def main(isbn=None, prefix=PREFIX):
    sys.excepthook = quiet_errors
    try:
        isterminal = sys.stdin.isatty()
        if not isterminal:
            return do_pipe()
        isbn = sys.argv[1] if not isbn else isbn[1]
        out = get_canonical_isbn(isbn)
        if out:
            print(out)
    except:
        return usage(prefix)
