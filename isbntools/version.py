"""
Copyright notice and checks updates
"""

import re
import urllib2
from . import colors


def check_version():
    """
    Checks online if there is a new version of isbntools
    """
    try:
        from .__init__ import __version__

        UA = "isbntools (%s)" % __version__
        headers = {'User-Agent': UA, 'Pragma': 'no-cache'}

        url = "https://raw.githubusercontent.com/xlcnd/"\
              "isbntools/master/isbntools/__init__.py"
        RE_VERSION = re.compile(r"__version__\s*=\s*'(.*)'")

        request = urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(request).read()

        newversion = re.search(RE_VERSION, content).group(1)

        if __version__ != newversion:
            print(colors.BOLD + colors.RED)
            print((" ** A new version (%s) is available! **" % newversion))
            print(colors.BLUE)
            print((" At command line enter: [sudo] pip install -U isbntools"))
            print("    or")
            print((" Download it from %s"
                  % "https://pypi.python.org/pypi/isbntools"))
            print(colors.RESET)
    except:
        pass
    finally:
        print("")
