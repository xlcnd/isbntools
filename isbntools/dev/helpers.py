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


def titlecase(s):
    """
    Title case function suitable to normalize book's title in metadata

    Only changes the first character of each word.
    """
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:], s)
