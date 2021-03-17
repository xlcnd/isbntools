# -*- coding: utf-8 -*-
"""Persistent shelve cache.

NOTES
1. shelve has different incompatible formats in py2 and py3.
2. If some methods detect that the cache is not consistent
   they delete the cache and create a new one.
3. After purge, the cache keeps the records with more hits
   and the newests.
4. By opening and closing in each operation, the cache performs badly
   for many records (because it doesn't use the 'in memory' part of cache,
   just the 'keys' are kept in memory).
   So don't increase MAXLEN too much.
5. The cache is optimized for low hit frequency (using a simple dict lookup
   not a Bloom filter!).


This file belongs to the project:

isbntools - extract, transform and metadata for ISBNs
Copyright (C) 2014-2021  Alexandre Lima Conde

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

# TODO rewrite using context managers!

import datetime
import shelve
from time import time as timestamp


class ShelveCache(object):
    """Read and write shelve cache."""

    MAXLEN = 2000
    CUTOFF = 0.5

    def __init__(self, filepath, allow_empty=True):
        """Initialize attributes."""
        self._sh = shelve
        self.filepath = filepath
        self._allow_empty = allow_empty
        self._allow_empty_default = allow_empty
        try:
            s = self._sh.open(self.filepath)
            try:
                self._keys = list(s.keys())
                if len(self._keys) > self.MAXLEN:
                    self.purge()
            except Exception:
                pass
        except Exception:
            s = self._sh.open(self.filepath, 'n')
            self._keys = []
        finally:
            s.close()

    def __getitem__(self, key):
        """Read cache e.g. cache[key]."""
        if key not in self._keys:
            return None
        try:
            s = self._sh.open(self.filepath, writeback=True)
            if s[key]:
                s[key]['hits'] += 1
                return s[key]['value']
            return None
        except ValueError:
            s = self._sh.open(self.filepath, 'n')
            self._keys = []
            return None
        finally:
            s.close()

    def get(self, key):
        """Read cache with get."""
        return self.__getitem__(key)

    def __setitem__(self, key, value):
        """Write to cache."""
        try:
            s = self._sh.open(self.filepath)
            if value or self._allow_empty:
                s[key] = {'value': value, 'hits': 0, 'timestamp': timestamp()}
                self._keys.append(key)
                status = True
            else:
                status = False
            self._allow_empty = self._allow_empty_default
        except Exception:
            self._allow_empty = self._allow_empty_default
            status = False
        finally:
            s.close()
        return status

    def set(self, key, value, allow_empty=None):
        """Write to cache with set."""
        if allow_empty is not None:
            self._allow_empty = allow_empty
        return self.__setitem__(key, value)

    def __delitem__(self, key):
        """Delete record with key."""
        if key not in self._keys:
            return
        try:
            s = self._sh.open(self.filepath)
            del s[key]
            self._keys.remove(key)
        except ValueError:
            s = self._sh.open(self.filepath, 'n')
            self._keys = []
            return
        finally:
            s.close()

    def __len__(self):
        """Return the number of keys in cache."""
        return len(self.keys()) if self.keys() else 0

    def __contains__(self, key):
        """Check if key is in keys."""
        return key in self._keys

    def __call__(self, key):
        """Allow an alternative way to access items."""
        return self.__getitem__(key)

    def keys(self):
        """Return list of keys in Cache."""
        if self._keys:
            return self._keys
        try:
            s = self._sh.open(self.filepath)
            self._keys = list(s.keys())
            return self._keys
        finally:
            s.close()

    def ts(self, key):
        """Return the timestamp of the record with key."""
        if key not in self._keys:
            return None
        try:
            s = self._sh.open(self.filepath)
            ts = s[key]['timestamp'] if s[key] else None
            if not ts:
                return None
            fmt = '%Y-%m-%d %H:%M:%S'
            return datetime.datetime.fromtimestamp(ts).strftime(fmt)
        except ValueError:
            s = self._sh.open(self.filepath, 'n')
            self._keys = []
            return None
        finally:
            s.close()

    def hits(self, key):
        """Return the number of hits for the record with key."""
        if key not in self._keys:
            return None
        try:
            s = self._sh.open(self.filepath)
            hts = s[key]['hits'] if s[key] else None
            return hts
        except ValueError:
            s = self._sh.open(self.filepath, 'n')
            self._keys = []
            return None
        finally:
            s.close()

    def new(self):
        """Make new cache."""
        s = self._sh.open(self.filepath, 'n')
        self._keys = []
        s.close()

    def purge(self):
        """Purge the cache."""
        if len(self.keys()) < self.MAXLEN:
            return
        try:
            s = self._sh.open(self.filepath)
            data = [(k, s[k]['timestamp'], s[k]['hits']) for k in s.keys()]
            data.sort(key=lambda tup: (-tup[2], -tup[1]))
            keep = int(self.CUTOFF * self.MAXLEN)
            garbk = [k[0] for k in data[keep:]]
            for k in garbk:
                del s[k]
            self._keys = s.keys()
        finally:
            s.close()
