# -*- coding: utf-8 -*-

"""Rename file using metadata."""

import string
import logging
from ._helpers import last_first
from ..bouth23 import u
from .. import config

LOGGER = logging.getLogger(__name__)

DEFAULT_PATT = '{firstAuthorLastName}{year}_{title}_{isbn}'
PATTERN = config.options.get('REN_FORMAT', DEFAULT_PATT)


def checkpattern(pattern):
    """Check the validity of pattern for renaming a file."""
    placeholders = ('{authorsFullNames}', '{authorsLastNames}',
                    '{firstAuthorLastName}', '{year}', '{publisher}',
                    '{title}', '{isbn}', '{language}')
    tocheck = pattern[:]

    placeholderfound = False
    for placeholder in placeholders:
        if placeholder in tocheck:
            tocheck = tocheck.replace(placeholder, '')
            placeholderfound = True
    if not placeholderfound or '{' in tocheck:
        LOGGER.warning('Not valid pattern %s', pattern)
        return False

    validchars = '-_.,() {0}{1}'.format(string.ascii_letters, string.digits)

    for char in tocheck:
        if char not in validchars:
            LOGGER.warning('Invalid character in pattern (%s)', char)
            return False
    return True


PATTERN = PATTERN if checkpattern(PATTERN) else DEFAULT_PATT


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
    if d['title'] == u('UNKNOWN') or d['isbn'] == u('UNKNOWN'):
        LOGGER.critical('Not enough metadata')
        return

    # cutoff title at 65
    cutoff = min(len(d['title']), 65)
    d['title'] = d['title'][:cutoff]

    try:
        formatted = u(pattern).format(**d)
        return cleannewname(formatted)
    except KeyError as e:
        LOGGER.warning('Error with placeholder: %s', e)
        return


def cleannewname(newname):
    """Strip '.,_' from newname."""
    return newname.strip().strip('.,_')
