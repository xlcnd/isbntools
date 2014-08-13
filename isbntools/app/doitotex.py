#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa

# doi2tex - give me a DOI I will give you the BibTeX :)
# Copyright (C) 2014  Alexandre Lima Conde

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from isbntools import quiet_errors
from isbntools import doi2tex
from isbntools import config


TO = 25


def usage():
    print('Usage: isbn_doi2tex DOI')
    sys.exit(1)

try:
    doi = sys.argv[1]
except:
    usage()


def main():
    sys.excepthook = quiet_errors
    config.setsocketstimeout(TO)
    try:
        data = doi2tex(doi)
        if data:
            print(data)
    except:
        usage()
