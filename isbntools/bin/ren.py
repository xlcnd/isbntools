# -*- coding: utf-8 -*-
"""Rename files using metadata."""

import logging
import sys
from difflib import get_close_matches

from ..app import (canonical, clean, config, get_canonical_isbn,
                   quiet_errors, registry)
from ..contrib.modules.rename import (checkpattern, get_isbn,
                                      rencwdfiles, renfile)

FORMAT = '%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


def usage(wservs="wcat|goob|..."):
    """Write usage message."""
    sys.stderr.write('Usage: \n\nisbn_ren [ISBN] [%s] '
                     '[apikey] [pattern] filename\n  ' % (wservs))
    sys.stderr.write(
        '\n  - If no ISBN is provided, the file name will \n'
        '    be searched for a valid ISBN and in this case you \n'
        '    can enter a glob pattern like "*.pdf". \n'
        '  - [pattern] must be a string in quotes containing\n  '
        '    only ASCII letters, digits and \'#\'-_.,() \'\n  '
        '    and one or more of the following placeholders:\n  '
        '    - {authorsFullNames}    (full names of the author(s))\n  '
        '    - {authorsLastNames}    (last names of the author(s))\n  '
        '    - {firstAuthorLastName} (only last name of first author)\n  '
        '    - {year}\n  '
        '    - {publisher}\n  '
        '    - {title}\n  '
        '    - {isbn}(ISBN-13) \n  '
        '    - {language}\n  '
        '    Author names are separated with commas, (\',\').\n  '
        '    Default pattern is \"'
        '{firstAuthorLastName}{year}_{title}_{isbn}\".\n\n')
    return 1


def parse_args(args):
    """Parse and return a tuple of the command line arguments."""
    fn = args[-1]
    service = None
    key = None
    isbn = None
    pattern = None
    if len(args) == 1:
        return (isbn, service, key, pattern, fn)
    isbn = get_canonical_isbn(canonical(clean(args[0])))
    providers = list(registry.services.keys())
    if isbn:
        args.pop(0)
    if args[0] != fn:
        service = args[0]
        match = get_close_matches(service, providers)
        if len(match) == 1 and '{' not in args[0]:  # <- rule out placeholders
            service = match[0]
        else:
            service = None
            pattern = args[0]
        key = None if args[1] == fn else args[1]
        if key and '{' in key:
            pattern = key
            key = None
        if not args[1] == fn:
            pattern = pattern if args[2] == fn else args[2]
    return (isbn, service, key, pattern, fn)


def is_fnpatt(filename):
    """Check if filename is a fnpattern."""
    return True if '*' in filename or '?' in filename else False


def reg_apikey(service, apikey):
    """Register API-KEY."""
    try:
        config.add_apikey(service, apikey)
    except:
        pass


def ren(args):
    """Rename files."""
    isbn, service, apikey, pattern, filename = parse_args(args)

    if pattern and not checkpattern(pattern):
        return

    if apikey:
        reg_apikey(service, apikey)

    if not isbn:
        if is_fnpatt(filename):
            return rencwdfiles(filename, service, pattern)
        isbn = get_isbn(filename)
        if not isbn:
            return
    return renfile(filename, isbn, service, pattern)


def main():
    sys.excepthook = quiet_errors
    success = ren(sys.argv[1:]) if len(sys.argv) > 1 else False
    if success:
        return
    providers = list(registry.services.keys())
    if 'default' in providers:
        providers.remove('default')
    available = '|'.join(providers)
    usage(available)
