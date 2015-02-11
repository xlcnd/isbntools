"""Define isbntools API and set lib environment."""

__all__ = ('check_version', 'audit', 'messages',
           'ISBNToolsException', 'EAN13',
           'doi', 'editions', 'get_canonical_isbn',
           'info', 'isbn_from_words', 'get_isbnlike',
           'mask', 'meta', 'to_isbn10', 'to_isbn13', 'goom',
           'libversion', 'config', 'registry', 'doi2tex', 'quiet_errors',
           'CONF_PATH', 'CACHE_FILE')


import os as _os

pkg_path = _os.path.dirname(_os.path.abspath(__file__))
defaults_conf = 'DEFAULTS'

# isbnlib hook -- only top level functions
from isbnlib import __version__ as libversion
from isbnlib import (EAN13, canonical, clean, doi, doi2tex, editions,
                     get_canonical_isbn, get_isbnlike, goom, info,
                     isbn_from_words, mask, meta, quiet_errors, to_isbn10,
                     to_isbn13)

# inject isbntools dependencies on isbnlib <-- first import after lib (IMPORTANT)
from ._initapp import config, registry, CONF_PATH, CACHE_FILE

# isbntools
from .contrib.modules.report import check_version, audit, messages
# from .contrib.modules.rename import ren # <-- cannot be imported

from ._exceptions import ISBNToolsException

# ALIAS
