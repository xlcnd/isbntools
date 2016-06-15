# -*- coding: utf-8 -*-
"""Define isbntools API and set lib environment."""

import os as _os
from shutil import copyfile

# isbnlib hook -- only top level functions
from isbnlib import __version__ as libversion
from isbnlib import (ean13, canonical, clean, doi, doi2tex, editions,
                     get_canonical_isbn, get_isbnlike, goom, info,
                     isbn_from_words, mask, meta, quiet_errors, to_isbn10,
                     to_isbn13, desc, cover)

# inject isbntools dependencies on isbnlib
# <-- first import after lib (IMPORTANT)
from ._initapp import config, registry, CONF_PATH, CACHE_FILE

# isbntools
from .contrib.modules.report import audit
# from .contrib.modules.rename import ren # <-- cannot be imported

from ._exceptions import ISBNToolsException
from ._console import uprint

# ALIAS

# dunders

__all__ = ('audit', 'ISBNToolsException', 'ean13', 'cover', 'desc', 'doi',
           'editions', 'get_canonical_isbn', 'canonical', 'info',
           'isbn_from_words', 'get_isbnlike', 'clean', 'mask', 'meta',
           'to_isbn10', 'to_isbn13', 'goom', 'libversion', 'config',
           'registry', 'doi2tex', 'quiet_errors', 'CONF_PATH', 'CACHE_FILE',
           'uprint')

pkg_path = _os.path.dirname(_os.path.abspath(__file__))
defaults_conf = 'DEFAULTS'
