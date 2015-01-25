# -*- coding: utf-8 -*-
"""isbntools helpers file."""

# DON'T USE! in the future this will be in 'isbnlib'

import os
import sys

from isbnlib.dev.bouth23 import u

WINDOWS = os.name == 'nt'
EOL = u('\r\n') if WINDOWS else u('\n')
PY2 = sys.version < '3'


def sprint(content):
    """Smart print function so that redirection works... (see issue 75)."""
    # FIXME adopt the same solution for both ops
    s = content + EOL
    # the print function doesn't work well with redirection
    # is best to work with bytes (unicode encoded as UTF-8)
    buf = s.encode("utf-8")
    if PY2:
        sys.stdout.write(buf)
    else:
        sys.stdout.buffer.write(buf)
