#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .helpers import normalize_space
from .exceptions import WPNotValidMetadataError

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
                raise WPNotValidMetadataError()
            self.clean()

    @staticmethod
    def fields():
        """
        Return a list of fields (names/headers/keys) of canonical
        """
        return list(FIELDS)

    def clean(self, broom=normalize_space, filter=()):
        """
        Clean fields of canonical
        """
        self._content.update((k, broom(v)) for k, v
                             in self._content.items()
                             if k != 'Authors' and k not in filter)
        if 'Authors' not in filter:
            self._content['Authors'] = [broom(i) for i in
                                        self._content['Authors']]

    @property
    def canonical(self):
        """
        Get canonical
        """
        return self._content

    @canonical.setter
    def canonical(self, record):
        """
        Sets canonical
        """
        self._content.update((k, v) for k, v in record.items())
        if not self._validate():
            self._set_empty()
            raise WPNotValidMetadataError()
        self.clean()

    @canonical.deleter
    def canonical(self):
        """
        Deletes canonical
        """
        self._set_empty()

    def add_to_authors(self, author):
        """
        Add Author to Authors list
        """
        if not type(author) is unicode:
            author = unicode(author)
        self._content['Authors'].append(author.strip())

    def _validate(self):
        """
        Validates canonical
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
        Sets an empty canonical record
        """
        self._content = dict.fromkeys(list(FIELDS), u'')
        self._content['Authors'] = [u'']

    def __str__(self):   # praga: no cover
        """
        How should metadata be printed
        """
        return '\n'.join((': '.join((f, repr(self._content[f]))) for f
                          in FIELDS)).replace("u''", "").replace("[]", "")


def stdmeta(records):
    """
    Function API to the class
    """
    dt = Metadata(records)
    return dt.canonical
