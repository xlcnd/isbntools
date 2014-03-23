import re
import urllib2


def check_version():
    try:
        from isbntools import __version__

        UA = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Firefox/17.0"
        headers = {'User-Agent': UA}

        url = "https://raw.githubusercontent.com/xlcnd/"\
              "isbntools/master/isbntools/__init__.py"
        RE_VERSION = re.compile("__version__\s*=\s*'(.*)'")

        request = urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(request).read()

        newversion = re.search(RE_VERSION, content).group(1)

        if __version__ != newversion:
            print((" **A new version (%s) is available!**" % newversion))
            print(r" Enter at command line: [sudo] pip install -U isbntools")
            print(r"    or")
            print(r" Download it from https://pypi.python.org/pypi/isbntools")
    finally:
        pass
