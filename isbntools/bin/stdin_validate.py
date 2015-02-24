# -*- coding: utf-8 -*-
"""Helper function to validate ISBNs from sys.stdin."""

import re
import sys

from isbntools.app import get_canonical_isbn, get_isbnlike


def stdin_validate():
    """Helper function to validate ISBNs from sys.stdin

    It will output all valid ISBNs that receive from input.

    Usage:
    cat ISBNs| isbn_stdin_validate
    """
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
