#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
from .data.data4mask import ranges
from .core import canonical, to_isbn13


def mask(isbn, separator='-'):
    """ Transforms a canonical ISBN to a `masked` one

    `Mask` the ISBN, separating by identifier
    ISBN-10 identifiers: country-publisher-title-check
    """
    ib = canonical(isbn)

    isbn10 = False
    if len(ib) == 10:
        check10 = ib[-1:]
        ib = to_isbn13(ib)
        isbn10 = True

    idx = None
    check = ib[-1:]
    cur = 3
    igi = cur
    buf = ib[igi:cur + 1]
    group = ib[0:cur] + '-' + buf

    for i in range(6):
        if group in ranges:
            sevens = ib[cur + 1:cur + 8].ljust(7, '0')
            for l in ranges[group]:
                if l[0] <= int(sevens) <= l[1]:
                    idx = l[2]
                    break
            break
        cur += 1
        buf = ib[igi:cur + 1]
        group = group + buf[-1:]

    if idx:
        if isbn10:
            group = group[4:]
            check = check10
        return separator.join([group, ib[cur + 1:cur + idx + 1],
                              ib[cur + idx + 1:-1], check])
    logging.warning('identifier not found! Please, update the program.')
    return
