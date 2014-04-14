# -*- coding: utf-8 -*-
"""
Private helper functions
"""

import re
import functools


def normalize_space(item):
    """
    Normalizes space

    Strips leading and trailing white space and replaces sequences of
    white space characters with a single space.
    """
    item = re.sub(r'\s\s+', ' ', item)
    return item.strip()


def titlecase(s):
    """
    Title case function suitable to normalize book's title in metadata

    Only changes the first character of each word.
    """
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda m: m.group(0)[0].upper() + m.group(0)[1:], s)


def compose1arg(*functions):
    """
    Composes one-argument functions

    Very handy for functional techniques!
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)
