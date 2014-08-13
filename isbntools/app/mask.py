#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from isbntools import mask


def usage():
    print('Usage: isbn_mask ISBN')


def main():
    try:
        output = mask(sys.argv[1])
        if output:
            print(output)
    except:
        usage()
