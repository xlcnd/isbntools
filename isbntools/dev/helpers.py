#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re


def normalize_space(item):
    """
    Normalizes space

    Strips leading and trailing white space and replaces sequences of
    white space characters with a single space
    """
    item = re.sub('\s\s+', ' ', item)
    return item.strip()
