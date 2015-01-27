# -*- coding: utf-8 -*-
"""isbntools helpers file."""

# DON'T USE! in the future this will be in 'isbnlib'

import os
import sys


WINDOWS = os.name == 'nt'
PY2 = sys.version < '3'
EOL = '\r\n' if WINDOWS and not PY2 else '\n'


def sprint(content):
    """Smart print function so that redirection works... (see issue 75)."""
    s = content + EOL
    buf = s.encode("utf-8")
    if PY2:
        sys.stdout.write(buf)
    else:
        sys.stdout.buffer.write(buf)
