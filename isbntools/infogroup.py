#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .data.data4info import d, identifiers


def infogroup(isbn):
    """ Language/Country of this ISBN """
    ixi, ixf = 0, 1
    if len(isbn) == 13:
        ixi, ixf = 3, 4
    for identifier in identifiers:
        iid = isbn[ixi:ixf]
        ixf += 1
        if iid in identifier:
            return d[iid]
