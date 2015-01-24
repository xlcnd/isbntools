# -*- coding: utf-8 -*-
"""isbntools helpers file."""

# DON'T USE! in the future this will be in 'isbnlib'

import os
import sys

from isbnlib.dev.bouth23 import b2u3

WINDOWS = os.name == 'nt'


def b2s3(x):
    """For Windows."""
    return x.encode("utf-8") if sys.version < '3' else x.decode("utf-8", 'ignore')


def sprint(content):
    """Smart print function so that redirection works... (see issue 75)."""
    if WINDOWS:  # pragma: no cover
        # print detects the appropriate code
        # (Windows terminal doesn't use UTF-8)
        # print(content.encode("utf-8"))
        s = content + '\n'
        sys.stdout.write(b2s3(s))
    else:
        # stdout gets UTF-8
        s = content + '\n'
        sys.stdout.write(b2u3(s))
