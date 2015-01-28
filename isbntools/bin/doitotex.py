#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa

import sys

from isbntools.app import config, doi2tex, quiet_errors


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
