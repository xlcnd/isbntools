# -*- coding: utf-8 -*-

from isbnlib import RDDATE

from .. import __version__
from ..contrib.modules.uxcolors import _colors as colors

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


def main():
    """Makes an audit report."""
    print((colors.BOLD))
    print(" isbntools - app and framework for 'all things ISBN'")
    print((colors.RESET))
    print((
        " Copyright (C) 2018  Alexandre Lima Conde, Version %s" % __version__))
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
          (colors.BOLD, libversion, colors.RESET, colors.BOLD, RDDATE[0:8],
           colors.RESET))
    print("")

    # check for updates and pypi packages
    print(" Checking %sonline%s services ... %sWAIT%s" %
          (colors.BOLD, colors.RESET, colors.BOLD, colors.RESET))
    try:
        from isbntools.contrib.modules.report import check_pypi
        check_pypi()
    except:
        pass
