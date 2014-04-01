#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .helpers import normalize_space
from .exceptions import NotValidMetadataError

# For now you cannot add custom fields!
FIELDS = ('ISBN-13', 'Title', 'Authors', 'Publisher', 'Year', 'Language')


class Metadata(object):
    """
    Class for metadata objects
    """

    def __init__(self, record=None):
        """
        Initializer
        """
        self._set_empty()
        if record:
            self._content.update((k, v) for k, v in record.items())
            if not self._validate():
                self._set_empty()
                raise NotValidMetadataError()
            self.clean()

    @staticmethod
    def fields():
        """
        Return a list of fields (names/headers/keys) of value
        """
        return list(FIELDS)

    def clean(self, broom=normalize_space, filtre=()):
        """
        Clean fields of value
        """
        self._content.update((k, broom(v)) for k, v
                             in self._content.items()
                             if k != 'Authors' and k not in filtre)
        if 'Authors' not in filtre:
            self._content['Authors'] = [broom(i) for i in
                                        self._content['Authors']]

    @property
    def value(self):
        """
        Get value
        """
        return self._content

    @value.setter
    def value(self, record):
        """
        Sets value
        """
        self._content.update((k, v) for k, v in record.items())
        if not self._validate():
            self._set_empty()
            raise NotValidMetadataError()
        self.clean()

    @value.deleter
    def value(self):
        """
        Deletes value
        """
        self._set_empty()

    def add_to_authors(self, author):
        """
        Add Author to Authors list
        """
        if not type(author) is unicode:
            author = unicode(author)
        self._content['Authors'].append(author.strip())

    def merge(self, record, overwrite=(), overrule=lambda x: x == ''):
        """
        Merge the record with value
        """
        # by default do nothing
        self._content.update((k, v) for k, v in record.items()
                             if k in overwrite and not overrule(v))
        if not self._validate():
            self._set_empty()
            raise NotValidMetadataError()
        self.clean()

    def empties(self):
        """
        Returns the names of empty fields
        """
        return [k for k, v in self._content.items() if v == u'' or v == []]

    def metric(self):
        """
        Returns the length of the characters that repr the object
        """
        return len(repr(self._content))

    def _validate(self):
        """
        Validates value
        """
        # 'minimal' check
        for k in self._content:
            if not type(self._content[k]) is unicode:
                if k != 'Authors':
                    return False
        if not type(self._content['Authors']) is list:
            return False
        return True

    def _set_empty(self):
        """
        Sets an empty value record
        """
        self._content = dict.fromkeys(list(FIELDS), u'')
        self._content['Authors'] = [u'']

    def __unicode__(self):  # pragma: no cover
        """
        How should metadata be printed (print unicode(...))
        """
        return '\n'.join((': '.join((k, v)) for k, v in self.__iter__()))

    def __iter__(self):
        """
        Define an iterator for the class (using a generator)
        """
        for k in FIELDS:
            if k == 'Authors':
                for i, a in enumerate(self._content['Authors']):
                    yield 'Author%s' % (i + 1), a
                continue
            yield k, self._content[k]

    def __len__(self):
        """
        Meaningful property for len(metadata object): Sum elements != u''
        """
        lenk = len([v for v in self._content.values() if v != u''])
        lena = len([l for l in self._content.get('Authors') if l != u''])
        return lenk + lena - 1

    def __eq__(self, other):
        """
        When are two of these objects equal?
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.metric() != other.metric():
            return False
        # if self.__len__(self) != self.__len__(other):
        #     return False
        qk = all(v == other._content[k] for k, v in self._content.items()
                 if k != 'Authors')
        if not qk:
            return False
        qa = all(self._content['Authors'][i] == other._content['Authors'][i]
                 for i in range(len(self._content['Authors'])))
        return qa


def stdmeta(records):
    """
    Function API to the class
    """
    dt = Metadata(records)
    return dt.value
