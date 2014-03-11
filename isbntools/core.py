#!/usr/bin/env python
# -*- coding: utf-8 -*-

# isbntools - tools for extracting, cleaning and transforming ISBNs
# Copyright (C) 2014  Alexandre Lima Conde

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


""" isbntools main file

Tools for extracting, cleaning, transforming and validating ISBN ids.
"""

import re
import logging

logger = logging.getLogger(__name__)


RE_ISBN10 = r'ISBN\x20(?=.{13}$)\d{1,5}([- ])\d{1,7}\1\d{1,6}\1(\d|X)$|[- 0-9X]{10,16}'
RE_ISBN13 = r'97[89]{1}(?:-?\d){10,16}|97[89]{1}[- 0-9]{10,16}'
RE_STRICT = r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$'
RE_NORMAL = r'97[89]{1}(?:-?\d){10}|\d{9}[0-9X]{1}|[-0-9X]{10,16}'
RE_LOOSE = r'[- 0-9X]{10,16}'
ISBN13_PREFIX = '978'
LEGAL = '0123456789xXisbnISBN- '


def _check_digit10(firstninedigits):
    """ Checks """
    # minimum checks
    if len(firstninedigits) != 9:
        return None
    try:
        int(firstninedigits)
    except:
        return None
    # checksum
    val = sum((i + 2) * int(x) for
              i, x in enumerate(reversed(firstninedigits)))
    remainder = int(val % 11)
    if remainder == 0:
        tenthdigit = 0
    else:
        tenthdigit = 11 - remainder
    if tenthdigit == 10:
        tenthdigit = 'X'
    return str(tenthdigit)


def _check_digit13(firsttwelvedigits):
    """ Checks """
    # minimum checks
    if len(firsttwelvedigits) != 12:
        return None
    try:
        int(firsttwelvedigits)
    except:
        return None
    # checksum
    val = sum((i % 2 * 2 + 1) * int(x) for
              i, x in enumerate(firsttwelvedigits))
    thirteenthdigit = 10 - int(val % 10)
    if thirteenthdigit == 10:
        thirteenthdigit = '0'
    return str(thirteenthdigit)


def _check_structure10(isbn10like):
    """ Looks like a isbn-10? """
    match = re.match(RE_ISBN10, isbn10like)
    if match:
        return True
    else:
        return False


def _check_structure13(isbn13like):
    """ Looks like an isbn-13? """
    if re.match(RE_ISBN13, isbn13like):
        return True
    else:
        return False


def is_isbn10(isbn10):
    """ Is an isbn-10? """
    isbn10 = canonical(isbn10)
    if len(isbn10) != 10:
        return False
    else:
        if _check_digit10(isbn10[:-1]) != isbn10[-1]:
            return False
        else:
            return True


def is_isbn13(isbn13):
    """ Is an isbn-13? """
    isbn13 = canonical(isbn13)
    if len(isbn13) != 13:
        return False
    else:
        if _check_digit13(isbn13[:-1]) != isbn13[-1]:
            return False
        else:
            return True


def to_isbn10(isbn13):
    """ isbn-13 to isbn-10 """
    # Check prefix
    if isbn13[:3] != ISBN13_PREFIX:
        return None
    isbn10 = isbn13[3:]
    last_digit = _check_digit10(isbn10[:-1])
    # Change check digit
    if last_digit:
        return isbn10[:-1] + last_digit
    else:
        return None


def to_isbn13(isbn10):
    """ isbn-10 to isbn-13 """
    isbn13 = ISBN13_PREFIX + isbn10[:-1]
    last_digit = _check_digit13(isbn13)
    if last_digit:
        return isbn13 + last_digit
    else:
        return None


def canonical(isbnlike):
    """ Only numbers and X """
    numb = [c for c in isbnlike if c in '0123456789X']
    return ''.join(numb)


def clean(isbnlike):
    """ Clean isbn (only legal characters) """
    cisbn = [c for c in isbnlike if c in LEGAL]
    buf = re.sub('\s*-\s*', '-', ''.join(cisbn))
    return re.sub('\s+', ' ', buf).strip()


def notisbn(isbnlike, level='strict'):
    """ Multiple checks with the goal to invalidate isbn-like

    These values are possible for `level`:
       * `strict` for certain they are not ISBNs (default)
       * `loose`  only filters obvious NO ISBNs

    """
    if level not in ('strict', 'loose'):
        logger.error('level as no option %s' % level)
        return
    isbnlike = canonical(isbnlike)
    if len(isbnlike) not in [10, 13]:
        return True
    if level != 'strict':
        return False
    if len(isbnlike) == 10:
        # an isbn-10 starting with 94 is not valid
        if isbnlike[0:2] == '94':
            return True
        return not is_isbn10(isbnlike)
    else:
        if isbnlike[3:5] == '94':
            return True
        return not is_isbn13(isbnlike)


def get_isbnlike(text, level='normal'):
    """ Extracts all substrings that seem like ISBNs

    Three values are possible for `level`:
       * `strict` almost as certain they are ISBNs
       * `normal` (default)
       * `loose`  catch many as possible

    """
    if level == 'normal':
        isbnlike = re.compile(RE_NORMAL, re.I | re.M | re.S)
    elif level == 'strict':
        isbnlike = re.compile(RE_STRICT, re.I | re.M | re.S)
    elif level == 'loose':
        isbnlike = re.compile(RE_LOOSE, re.I | re.M | re.S)
    else:
        logger.error('level as no option %s' % level)
        return
    return isbnlike.findall(text)


def get_canonical_isbn(isbnlike, output='bouth'):
    """ Checks for ISBN-10 or ISBN-13 format
        and returns a ISBN in `canonical` form

    `output` can be:
       * `isbn10`
       * `isbn13`
       * `bouth` (default)

    """
    if output not in ('bouth', 'isbn10', 'isbn13'):
        logger.error('output as no option %s' % output)
        return

    regex = re.compile(RE_STRICT)

    if regex.search(isbnlike):
        # Get only canonical characters and split them into a list
        cisbn = canonical(isbnlike)
        chars = list(cisbn)
        # Remove the last digit from `chars` and assign it to `last`
        last = chars.pop()
        buf = ''.join(chars)

        if len(chars) == 9:
            # Compute the ISBN-10 checksum digit
            check = _check_digit10(buf)
        else:
            # Compute the ISBN-13 checksum digit
            check = _check_digit13(buf)

        # If checksum OK return a `canonical` ISBN
        if (str(check) == last):
            if output == 'bouth':
                return cisbn
            if output == 'isbn10':
                return cisbn if len(cisbn) == 10 else to_isbn10(cisbn)
            return to_isbn13(cisbn) if len(cisbn) == 10 else cisbn
