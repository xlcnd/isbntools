# -*- coding: utf-8 -*-
"""isbntools helpers file."""

import os
import sys

from isbnlib.dev.bouth23 import b2u3

WINDOWS = os.name == 'nt'


def sprint(content):
    """Smart print function so that redirection works... (see issue 75)"""
    if WINDOWS:
        # print detects the appropriate code
        # (Windows terminal doesn't use UTF-8)
        print(content)
    else:
        # stdout gets UTF-8
        s = content + '\n'
        sys.stdout.write(b2u3(s))   
