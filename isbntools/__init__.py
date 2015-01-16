"""Define isbntools API and set lib environment."""

__all__ = ('__version__', '__support__', 'check_version', 'audit',
           'ISBNToolsException', 'canonical', 'clean', 'EAN13',
           'doi', 'editions', 'get_canonical_isbn', 'get_isbnlike',
           'info', 'is_isbn10', 'is_isbn13', 'isbn_from_words',
           'mask', 'meta', 'notisbn', 'to_isbn10', 'to_isbn13', 'goom',
           'libversion', 'config', 'registry', 'doi2tex', 'quiet_errors')

__version__ = '4.0.1'                               # <-- literal IDs
__support__ = 'py26, py27, py33, py34, pypy'        # <-- literal IDs


import os as _os

pkg_path = _os.path.dirname(_os.path.abspath(__file__))
defaults_conf = 'DEFAULTS'


# isbnlib hook
from isbnlib import (canonical, clean, doi, editions, get_canonical_isbn,
                     get_isbnlike, info, is_isbn10, is_isbn13,
                     isbn_from_words, mask, meta, notisbn,
                     to_isbn10, to_isbn13, EAN13, goom, doi2tex, quiet_errors)
from isbnlib import __version__ as libversion

# inject isbntools dependencies on isbnlib
from . import _setconf         # <-- first import after lib (IMPORTANT)
# from isbnlib import config
# from isbnlib import registry
from ._setconf import config
from ._setconf import registry

# isbntools
from .contrib.modules.report import check_version, audit
# from .contrib.modules.rename import ren # <-- cannot be imported

from ._exceptions import ISBNToolsException

# ALIAS
