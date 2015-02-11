#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from isbnlib import RDDATE
from isbntools import __version__
from isbntools.contrib.modules.uxcolors import _colors as colors


def main(wait=5):
    NOTICE = """
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

    print((colors.BOLD))
    print(" isbntools - tools for extracting, cleaning and transforming ISBNs")
    print((colors.RESET))
    print((" Copyright (C) 2014  Alexandre Lima Conde, Version %s" % __version__))
    print("")
    print(" License LGPL v3")
    print((NOTICE))

    # make audit
    from isbntools.app import audit
    print((colors.BOLD))
    audit()
    print((colors.RESET))

    # conf file
    from isbntools.conf import conf_file
    if conf_file != 'DEFAULTS':
        print("")
        print(' Your configuration file is at:')
        print("  %s%s%s" % (colors.BOLD, conf_file, colors.RESET))
        print("")

    # lib version
    from isbntools.app import libversion
    print(" And 'isbntools' is using:")
    print("  'isbnlib' version %s%s%s with 'range db' %s%s%s" %
          (colors.BOLD, libversion, colors.RESET, colors.BOLD, RDDATE[0:8], colors.RESET))
    print("")

    # check for updates and messages
    try:
        import threading
        from isbntools.app import check_version, messages
        from isbntools.contrib.modules.report import check_pypi

        threading.Thread(target=check_version).start()
        threading.Thread(target=messages).start()
        threading.Thread(target=check_pypi).start()
    finally:
        time.sleep(wait)
