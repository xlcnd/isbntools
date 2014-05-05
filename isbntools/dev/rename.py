# -*- coding: utf-8 -*-

import os
import shutil
import string
import logging

from .fmt import _last_first


logger = logging.getLogger(__name__)


def checkfileaccess(filename):
    """
    checks if a file exists and is readable and writeable
    """

    if not os.access(filename, os.F_OK):
        logger.warning('file \'' + filename + '\' not found')
        return False
    if not os.access(filename, os.R_OK):
        logger.warning('no reading rights for file \'' + filename + '\'')
        return False
    if not os.access(filename, os.W_OK):
        logger.warning('no writing rights for file \'' + filename + '\'')
        return False
    return True


def checkpattern(pattern):
    """
    checks a pattern for renaming a file for validity
    """

    placeholders = ['{authorsfull}', '{authorslast}', '{year}',
                    '{publisher}', '{title}', '{isbn}', '{language}']
    tocheck = pattern[:]

    placeholderfound = False
    for placeholder in placeholders:
        if placeholder in tocheck:
            tocheck = tocheck.replace(placeholder, '')
            placeholderfound = True
    if not placeholderfound:
        logger.warning('no placeholders found in pattern \'' + pattern + '\'')
        return False

    validchars = '-_.,() {0}{1}'.format(string.ascii_letters, string.digits)
    for char in tocheck:
        if char not in validchars:
            logger.warning('invalid character in pattern: \'' + char + '\'')
            return False
    return True


def splitname(fullname):
    """
    returns a 3-tuple of path to, name of and extension of a file
    """

    path, filename = os.path.split(fullname)
    if (filename):
        name, extension = os.path.splitext(filename)
        return (path, name, extension)
    return None


def newfilename(metadata, pattern='{authorslast}_{year}_{title}_{isbn}'):
    """
    returns a new file name created from
    book metadata formatted according to pattern
    """

    d = {
        'authorsfull': ','.join(metadata['Authors']),
        'year': metadata['Year'],
        'publisher': metadata['Publisher'],
        'title': metadata['Title'],
        'language': metadata['Language'],
        'isbn':
            metadata['ISBN-13'] if ('ISBN-13' in metadata)
            else metadata['ISBN-10']
    }

    authorslastnames = [_last_first(authorname)['last']
                        for authorname in metadata['Authors']]
    if (len(authorslastnames) >= 3):
        d['authorslast'] = authorslastnames[0] + "_e.a."
    else:
        d['authorslast'] = ','.join(authorslastnames)

    try:
        formatted = pattern.format(**d)
        return formatted
    except KeyError as e:
        logger.warning('unknown placeholder: ' + str(e))


def rename(oldfilename, newfilename):
    """
    rename (move) file from oldfilename to newfilename
    """

    try:
        shutil.move(oldfilename, newfilename)
    except IOError as error:
        logger.warning(
            'An error occurred while trying to rename the file: '
            + str(error))
