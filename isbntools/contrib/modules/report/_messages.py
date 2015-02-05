# -*- coding: utf-8 -*-
"""Get and display messages."""


try:                                                       # pragma: no cover
    from urllib.request import Request
    from urllib.request import urlopen
except ImportError:                                        # pragma: no cover
    from urllib2 import Request
    from urllib2 import urlopen

from ..uxcolors import _colors as colors

from isbnlib.dev.bouth23 import s


def selected(cur, cond, ref):                              # pragma: no cover
    """Evaluate if current version is within the condition."""
    if cond == '>':
        return cur > ref
    if cond == '=':
        return cur == ref
    if cond == '<':
        return cur < ref


def messages():
    """Check online if there are messages from isbntools."""
    try:
        from ....__init__ import __version__

        # Get messages from dev branch
        UA = "isbntools (%s)" % __version__
        headers = {'User-Agent': UA, 'Pragma': 'no-cache'}
        url = "https://raw.githubusercontent.com/xlcnd/"\
              "isbntools/dev/MESSAGES.csv"
        request = Request(url, headers=headers)
        content = s(urlopen(request).read())

        # Parse, select and print messages
        cur = tuple([int(c) for c in __version__.split('.')])
        display = []
        lines = content.split('\n')
        for line in lines:
            if not line.strip().strip('\n'):               # pragma: no cover
                continue
            vrs, cnd, msg = line.split('|')
            ref = tuple([int(c) for c in vrs.split('.') if vrs])
            if selected(cur, cnd, ref):                    # pragma: no cover
                display.append(msg)

        if display:                                        # pragma: no cover
            print("%s%s%s" % (colors.RED, " Important messages:", colors.BOLD))
            for msg in display:
                print(" => %s" % msg)
            print((colors.RESET))
        return 0
    except:                                                # pragma: no cover
        return 1
