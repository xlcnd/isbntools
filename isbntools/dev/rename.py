# -*- coding: utf-8 -*-

"""Rename file using metadata."""

import string
import logging

from ._helpers import last_first
from ..bouth23 import u

LOGGER = logging.getLogger(__name__)
PATTERN = '{firstAuthorLastName}{year}_{title}_{isbn}'


def checkpattern(pattern):
    """Check a pattern for renaming a file for validity."""
    placeholders = ['{authorsFullNames}', '{authorsLastNames}',
                    '{firstAuthorLastName}', '{year}', '{publisher}',
                    '{title}', '{isbn}', '{language}']
    tocheck = pattern[:]

    placeholderfound = False
    for placeholder in placeholders:
        if placeholder in tocheck:
            tocheck = tocheck.replace(placeholder, '')
            placeholderfound = True
    if not placeholderfound:
        LOGGER.warning('no placeholders found in pattern \'' + pattern + '\'')
        return False

    validchars = '-_.,() {0}{1}'.format(string.ascii_letters, string.digits)
    for char in tocheck:
        if char not in validchars:
            LOGGER.warning('invalid character in pattern: \'' + char + '\'')
            return False
    return True


def newfilename(metadata, pattern=PATTERN):
    """Return a new file name created from book metadata."""
    for key in metadata.keys():
        if not metadata[key]:
            metadata[key] = u('UNKNOWN')

    d = {
        'authorsFullNames': ','.join(metadata['Authors']),
        'year': metadata['Year'],
        'publisher': metadata['Publisher'],
        'title': metadata['Title'],
        'language': metadata['Language'],
        'isbn': metadata['ISBN-13']
    }

    authorslastnames = [last_first(authorname)['last']
                        for authorname in metadata['Authors']]
    d['authorsLastNames'] = ','.join(authorslastnames)
    d['firstAuthorLastName'] = authorslastnames[0]

    try:
        formatted = u(pattern).format(**d)
        return cleannewname(formatted)
    except KeyError as e:
        LOGGER.warning('unknown placeholder: ' + str(e))


def cleannewname(newname):
    """Strip '.,_' from newname."""
    newname = newname.strip('.,_')
    return newname.strip()
