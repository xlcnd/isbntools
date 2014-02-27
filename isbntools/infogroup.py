#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .data.data4info import d, identifiers, dnew, newidentifiers


def infogroup(isbn):
    """ Language/Country of this ISBN """
    dtxt = d.copy()
    idents = identifiers
    ixi, ixf = 0, 1
    if len(isbn) == 13:
        ixi, ixf = 3, 4
        if isbn[0:3] == '979':
            ixf = 5  # <-- 979 id start with a group of 2 elements
            dtxt = dnew.copy()
            idents = newidentifiers
    for ident in idents:
        iid = isbn[ixi:ixf]
        ixf += 1
        if iid in ident:
            return dtxt[iid]
