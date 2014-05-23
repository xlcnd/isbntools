#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

from nose.tools import assert_equals
from isbntools.dev.rename import checkpattern, newfilename
from ..bouth23 import u

"""
nose tests
"""


def test_checkpattern():
    assert_equals(checkpattern(
                  '{authorsLastNames}_{year}_{title}_{isbn}.pdf'), True)
    assert_equals(checkpattern('mypattern.pdf'), False)
    assert_equals(checkpattern('mypattern{year}'), True)
    assert_equals(checkpattern(
                  '.{authorsFullNames}_{authorsLastNames} {year}..'
                  '{publisher}({title}){isbn}{language}'), True)
    assert_equals(checkpattern('authors:{authorsFullNames}'), False)


def test_newfilename():
    metadata = {'Title': 'A Dictionary Of The Internet',
                'Authors': ['Darrel Ince', 'Oxford University Press'],
                'Publisher': 'Oxford University Press',
                'ISBN-13': '9780199571444', 'Language': 'eng', 'Year': '2009'}
    assert_equals(newfilename(
                  metadata,
                  '{authorsLastNames}_{year}_{title}_{isbn}.epub'),
                  'Ince,Press_2009_A Dictionary Of '
                  'The Internet_9780199571444.epub')
    assert_equals(
        newfilename(metadata, '{authorsFullNames}_{publisher}_{language}'),
        'Darrel Ince,Oxford University Press_Oxford University Press_eng')
    assert_equals(newfilename(metadata,
                  'myfile_{year} {authorsLastNames}.pdf'),
                  'myfile_2009 Ince,Press.pdf')

    assert_equals(newfilename(metadata, 'myfile_{nokey}'), None)
    assert_equals(newfilename(metadata, '{authorsFullNames}: {title}'),
                  'Darrel Ince,Oxford University Press: A '
                  'Dictionary Of The Internet')
    assert_equals(newfilename(metadata, 'myfile.pdf'), 'myfile.pdf')

    metadata['Publisher'] = u('')
    assert_equals(newfilename(metadata,
                  pattern='{authorsFullNames}_{publisher}_{language}'),
                  'Darrel Ince,Oxford University Press_UNKNOWN_eng')
    metadata['Title'] = u('')
    assert_equals(newfilename(metadata), None)
