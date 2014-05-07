# -*- coding: utf-8 -*-
"""
Private helper functions
"""

import re
import sys


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


def last_first(author):
    """
    Parses an author name into a dict with keys:
      last  (surname),
      first (other names)
    This works in some cases... however is good enough!
    """
    if ',' in author:
        tokens = author.split(',')
        last = tokens[0].strip()
        first = ' '.join(tokens[1:]).strip().replace('  ', ', ')
    else:
        tokens = author.split(' ')
        last = tokens[-1].strip()
        first = ' '.join(tokens[:-1]).strip()
    return {'last': last, 'first': first}


def unicode_to_utf8tex(utex, filtre=()):
    """
    Replaces unicode entities with tex entitites and returns utf8 bytes
    """
    from ..bouth23 import b, s
    from ..data.data4tex import unicode_to_tex
    btex = utex.encode('utf-8')
    table = dict((k.encode('utf-8'), v) for k, v in unicode_to_tex.items()
                 if v not in filtre)
    regex = re.compile(b('|'.join(re.escape(s(k)) for k in table)))
    return regex.sub(lambda m: table[m.group(0)], btex)


def in_virtual():
    """
    Detects if the program is running inside a python virtual environment
    """
    return True if hasattr(sys, 'real_prefix') else False
