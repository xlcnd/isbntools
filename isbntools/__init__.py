"""Define isbntools API."""

__all__ = ('is_isbn10', 'is_isbn13', 'clean', 'mask', 'info', 'meta',
           'to_isbn10', 'to_isbn13', 'get_isbnlike', 'notisbn', 'EAN13',
           'canonical', 'get_canonical_isbn', 'editions', 'isbn_from_words',
           'quiet_errors', 'config', 'setconf', '__version__', 'doi',
           'check_version', 'ISBN13', 'Cache')

__version__ = '3.2.5'

import os
import logging
from . import config        # <-- first import
from . import setconf       # <-- first import
from ._version import check_version
from .exceptions import quiet_errors
from ._cache import Cache
from ._core import (is_isbn10, is_isbn13, to_isbn10, to_isbn13, clean,
                    canonical, notisbn, get_isbnlike, get_canonical_isbn,
                    EAN13)
from ._ext import (mask, meta, info, editions, isbn_from_words, doi)


pkg_path = os.path.dirname(os.path.abspath(__file__))
defaults_conf = 'DEFAULTS'

# alias
ISBN13 = EAN13

# config logging for lib (NullHandler not available for py26)
try:
    nh = logging.NullHandler()
except:              # pragma: no cover
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

    nh = NullHandler()

logging.getLogger('isbntools').addHandler(nh)
