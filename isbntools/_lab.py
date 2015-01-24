# -*- coding: utf-8 -*-
"""isbntools helpers file."""

# DON'T USE! in the future this will be in 'isbnlib'

import os
import sys

from isbnlib.dev.bouth23 import b2u3

WINDOWS = os.name == 'nt'


def sprint(content):
    """Smart print function so that redirection works... (see issue 75)."""
    if WINDOWS:  # pragma: no cover
        # the `print` function detects the appropriate codec
        # (Windows terminal doesn't use UTF-8)
        s = content + '\n'
        # s = content.encode("utf-8")
        if sys.version < '3':
            sys.stdout.write(s.encode('utf-8'))
        else:
            # sys.stdout.write(s)
            # print(s.encode(ecode))
            # sys.stdout.write(s.encode(ecode))
            # IS almost impossible to write non-ascii characters
            # in a Windows terminal with python 3!!!
            # try:
            #     print(content)
            # except:
            # ecode = sys.stdout.encoding
            # ecode = 'utf-8' if ecode is None else ecode
            # sys.stdout.write(s)
            print(content)
    else:
        # stdout gets UTF-8
        s = content + '\n'
        sys.stdout.write(b2u3(s))
