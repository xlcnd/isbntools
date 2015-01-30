#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa

import sys

from isbntools.app import config, doi2tex, quiet_errors


TO = 25


def usage():
    print('Usage: isbn_doi2tex DOI')
    return 1


def main(doi=None):
    sys.excepthook = quiet_errors
    config.setsocketstimeout(TO)
    try:
        doi = sys.argv[1] if not doi else doi[1]
        data = doi2tex(doi)
        if data:
            print(data)
    except:
        usage()
