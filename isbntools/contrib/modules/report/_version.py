# -*- coding: utf-8 -*-
"""Copyright notice and checks updates."""

import re
import sys

from isbnlib.dev.bouth23 import s
try:
    from urllib.request import Request
    from urllib.request import urlopen
except ImportError:
    from urllib2 import Request
    from urllib2 import urlopen
from ..uxcolors import _colors as colors


def check_version():
    """Check online if there is a new version of isbntools."""
    try:
        from ....__init__ import __version__

        # FILTER
        # dont't upgrade if this version of python is not supported anymore
        import platform
        implementation = platform.python_implementation()
        if implementation != "PyPy":
            pyversion = "py{0}{1}".format(sys.version_info.major,
                                          sys.version_info.minor)
        else:
            pyversion = "pypy"

        UA = "isbntools (%s)" % __version__
        headers = {'User-Agent': UA, 'Pragma': 'no-cache'}
        url = "https://raw.githubusercontent.com/xlcnd/"\
              "isbntools/master/isbntools/__init__.py"
        request = Request(url, headers=headers)
        content = s(urlopen(request).read())

        RE_SUPPORT = re.compile(r"__support__\s*=\s*'(.*)'")
        supported = [iden.strip() for iden
                     in re.search(RE_SUPPORT, content).group(1).split(',')]
        if pyversion not in supported:
            raise

        RE_VERSION = re.compile(r"__version__\s*=\s*'(.*)'")
        _newversion = re.search(RE_VERSION, content).group(1)

        has_newversion = False
        try:
            newversion = tuple(map(int, _newversion.split('.')))
            version = tuple(map(int, __version__.split('.')))
            if newversion > version:
                has_newversion = True
        except:
            newversion = None
            has_newversion = __version__ != _newversion

        if has_newversion and newversion:
            print((colors.BOLD + colors.RED))
            print((" ** A new version (%s) is available! **" % _newversion))
            print((colors.BLUE))
            print((" At command line enter: [sudo] pip install -U isbntools"))
            print("    or")
            print((" Download it from %s"
                   % "https://pypi.python.org/pypi/isbntools"))
            print((colors.RESET))
    except:
        pass
    finally:
        sys.exit()
