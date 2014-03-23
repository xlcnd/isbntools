import re
import urllib2


def check_version():
    """
    Checks if there are available a new version of isbntools
    """
    try:
        from isbntools import __version__
        from random import random

        rid = str(random()).split('.')[1][0:5]
        UA = "isbntools (%s) %s" % (__version__, rid)
        headers = {'User-Agent': UA}

        url = "https://raw.githubusercontent.com/xlcnd/"\
              "isbntools/master/isbntools/__init__.py"
        RE_VERSION = re.compile("__version__\s*=\s*'(.*)'")

        request = urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(request).read()

        newversion = re.search(RE_VERSION, content).group(1)

        if __version__ != newversion:
            print((" **A new version (%s) is available!**" % newversion))
            print(r" At command line enter: [sudo] pip install -U isbntools")
            print(r"    or")
            print(r" Download it from https://pypi.python.org/pypi/isbntools")
    finally:
        pass
