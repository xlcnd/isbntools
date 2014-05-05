#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nose.tools import assert_equals

#  functions to test:
from isbntools.dev.rename import checkfileaccess, checkpattern, \
    splitname, newfilename, rename

"""
nose tests
"""


def test_rename_dev():
    assert_equals(checkpattern('{authorslast}_{year}_{title}_{isbn}.pdf'),
                  True)
    assert_equals(checkpattern('mypattern.pdf'), False)
    assert_equals(checkpattern('mypattern{year}'), True)
    assert_equals(checkpattern('.{authorsfull}_{authorslast} {year}..'
                               '{publisher}({title}){isbn}{language}'), True)
    assert_equals(checkpattern('authors:{authorsfull}'), False)

    assert_equals(splitname('/home/me/myfile.pdf'),
                           ('/home/me', 'myfile', '.pdf'))
    assert_equals(splitname('myfile.pdf'), ('', 'myfile', '.pdf'))
    assert_equals(splitname('/home/me/myfile'), ('/home/me', 'myfile', ''))

    metadata = {'Title': 'A Dictionary Of The Internet',
                'Authors': ['Darrel Ince', 'Oxford University Press'],
                'Publisher': 'Oxford University Press',
                'ISBN-13': '9780199571444', 'Language': 'eng', 'Year': '2009'}
    assert_equals(newfilename(
                  metadata,
                  '{authorslast}_{year}_{title}_{isbn}.epub'),
                  'Ince,Press_2009_A Dictionary Of '
                  'The Internet_9780199571444.epub')
    assert_equals(
        newfilename(metadata, '{authorsfull}_{publisher}_{language}'),
        'Darrel Ince,Oxford University Press_Oxford University Press_eng')
    assert_equals(newfilename(metadata, 'myfile_{year} {authorslast}.pdf'),
                  'myfile_2009 Ince,Press.pdf')
    assert_equals(newfilename(metadata, 'myfile_{nokey}'), None)
    assert_equals(newfilename(metadata, '{authorsfull}: {title}'),
                  'Darrel Ince,Oxford University Press: A '
                  'Dictionary Of The Internet')
    assert_equals(newfilename(metadata, 'myfile.pdf'), 'myfile.pdf')

    f = open('torename_testfile.pdf', 'w')
    f.close()
    assert_equals(checkfileaccess('torename_testfile.pdf'), True)
    rename(os.path.join(os.getcwd(), 'torename_testfile.pdf'),
           os.path.join(os.getcwd(), 'renamed_testfile.pdf'))
    assert ('renamed_testfile.pdf' in os.listdir('.'))
    assert ('torename_testfile.pdf' not in os.listdir('.'))
    assert_equals(checkfileaccess('torename_testfile.pdf'), False)
    os.remove('renamed_testfile.pdf')
