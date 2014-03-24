import os
import re
import urllib2


def set_red():
    return '\x1b[38;5;9m' if os.name != 'nt' else ''


def set_blue():
    return '\x1b[38;5;12m' if os.name != 'nt' else ''


def reset():
    return '\x1b[0m' if os.name != 'nt' else ''


def check_version():
    """
    Checks online if there is a new version of isbntools
    """
    try:
        from isbntools import __version__

        UA = "isbntools (%s)" % __version__
        headers = {'User-Agent': UA, 'Pragma': 'no-cache'}

        url = "https://raw.githubusercontent.com/xlcnd/"\
              "isbntools/master/isbntools/__init__.py"
        RE_VERSION = re.compile("__version__\s*=\s*'(.*)'")

        request = urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(request).read()

        newversion = re.search(RE_VERSION, content).group(1)

        if __version__ != newversion:
            print(set_red())
            print((" ** A new version (%s) is available! **" % newversion))
            print(set_blue())
            print((" At command line enter: [sudo] pip install -U isbntools"))
            print("    or")
            print((" Download it from %s"
                  % "https://pypi.python.org/pypi/isbntools"))
            print(reset())
    finally:
        print("")
