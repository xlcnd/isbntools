# -*- coding: utf-8 -*-
"""
Private helper functions
"""

import re


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


def unicode_to_utf8tex(ustream, filtre=None):       # pragma: no cover
    """
    Replaces unicode entities by tex entitites and returns utf8 bytes
    """
    from ..bouth23 import b, s
    from ..data.data4tex import unicode_to_tex
    filtre = filtre if filtre else []
    bstream = ustream.encode('utf-8')
    table = dict((k.encode('utf-8'), v) for k, v in unicode_to_tex.items()
                 if v not in filtre)
    regex = re.compile(b('|'.join(re.escape(s(k)) for k in table)))
    return regex.sub(lambda m: b(table[m.group(0)]), bstream)
