# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""nose tests for rename."""

import os

from isbnlib.dev._bouth23 import b2u3, u
from isbnlib.dev.helpers import cwdfiles
from isbntools.contrib.modules.rename import (
    checkpattern,
    cleannewname,
    get_isbn,
    newfilename,
    rencwdfiles,
    renfile,
)
from nose.tools import assert_equals


WINDOWS = os.name == 'nt'

TESTFILE = './a-deleteme.pdf'
NEW_BASENAME = 'a-deleteme-PLEASE.pdf'

F1 = '9780321534965.pdf'
F2 = '9780743258074.pdf'
# F3 = '9781852330729.pdf'
# F4 = '9787500117018.pdf'

F5 = '9789727576807.pdf'
F6 = u('Campos2011_Emergências obstétricas_9789727576807.pdf')

F7 = u('Knuth2008_The Art Of Computer Programming_9780321534965.pdf')
# F8 = u('Man2001_Genetic Algorithms Concepts And Designs_9781852330729.pdf')
F9 = u('Isaacson2004_Benjamin Franklin_9780743258074.pdf')
# F10 = u('海明威2007_Lao ren yu hai_9787500117018.pdf')

F11 = 'myfile.pdf'

# FISBN = [F1, F2, F3, F4, F5]
# FISBN = [F1, F2, F5]
FISBN = [F1, F2]
# FFT = [F6, F7, F8, F9, F10]
# FFT = [F6, F7, F9]
FFT = [F7, F9]
FILES = FISBN + FFT + [F11]

PATT0 = '{firstAuthorLastName}{year}_{title}_{isbn}'
PATT1 = '{year}_{title}_{isbn}'
PATT2 = '{isbn}'


def create_files(files):
    os.chdir(os.path.dirname(TESTFILE))
    for fn in files:
        f = open(fn, 'w')
        f.write(b2u3('ooo') + b2u3(fn))
        f.close()


def delete_files(fnpatt):
    os.chdir(os.path.dirname(TESTFILE))
    for fn in cwdfiles(fnpatt):
        os.remove(fn)


def setup_module():
    create_files([u(TESTFILE), u('./a-deleteme-PLEASE.pdf')])
    os.chdir(os.path.dirname(TESTFILE))
    create_files(FISBN + [F11])


def teardown_module():
    # os.remove(os.path.join(os.path.dirname(TESTFILE), NEW_BASENAME))
    delete_files('*.pdf')


def test_checkpattern():
    """Test the validation of placeholders"""
    assert_equals(
        checkpattern('{authorsLastNames}_{year}_{title}_{isbn}.pdf'), True)
    assert_equals(checkpattern('mypattern.pdf'), False)
    assert_equals(checkpattern('mypattern{year}'), True)
    assert_equals(
        checkpattern('.{authorsFullNames}_{authorsLastNames} {year}..'
                     '{publisher}({title}){isbn}{language}'),
        True,
    )
    assert_equals(checkpattern('authors:{authorsFullNames}'), False)


def test_newfilename():
    """Test new filename generation"""
    metadata = {
        'Title': 'A Dictionary Of The Internet',
        'Authors': ['Darrel Ince', 'Oxford University Press'],
        'Publisher': 'Oxford University Press',
        'ISBN-13': '9780199571444',
        'Language': 'eng',
        'Year': '2009',
    }
    assert_equals(
        newfilename(metadata, '{authorsLastNames}_{year}_{title}_{isbn}.epub'),
        'Ince,Press_2009_A Dictionary Of '
        'The Internet_9780199571444.epub',
    )
    assert_equals(
        newfilename(metadata, '{authorsFullNames}_{publisher}_{language}'),
        'Darrel Ince,Oxford University Press_Oxford University Press_eng',
    )
    assert_equals(
        newfilename(metadata, 'myfile_{year} {authorsLastNames}.pdf'),
        'myfile_2009 Ince,Press.pdf',
    )

    assert_equals(newfilename(metadata, 'myfile_{nokey}'), None)
    assert_equals(
        newfilename(metadata, '{authorsFullNames}: {title}'),
        'Darrel Ince,Oxford University Press: A '
        'Dictionary Of The Internet',
    )
    assert_equals(newfilename(metadata, 'myfile.pdf'), 'myfile.pdf')

    metadata['Publisher'] = u('')
    assert_equals(
        newfilename(
            metadata, pattern='{authorsFullNames}_{publisher}_{language}'),
        'Darrel Ince,Oxford University Press_UNKNOWN_eng',
    )
    metadata['Title'] = u('')
    assert_equals(newfilename(metadata), None)


def test_cleannewname():
    """Test the cleaning of new filename"""
    assert_equals(
        cleannewname(' this, is a newname., _'), 'this, is a newname')


def test_get_isbn():
    """Test isbn extraction from file names"""
    assert_equals(get_isbn('The Internet_9780199571444.epub'), '9780199571444')
    # assert_equals(
    #    get_isbn('海明威2007_Lao ren yu hai_9787500117018.pdf'), '9787500117018')
    assert_equals(get_isbn('ebook 0826497527 isbn.pdf'), '9780826497529')
    # assert_equals(get_isbn('9780199571445.epub'), None)


def test_renfile():
    """Test the renaming of a file"""
    renfile(F11, '9781593271923', 'default', PATT0)
    assert_equals(
        'Seitz2009_Gray Hat Python_9781593271923.pdf' in cwdfiles('*.pdf'),
        True)
    create_files([F11])
    renfile(F11, '9781593271923', 'default', PATT1)
    assert_equals(
        '2009_Gray Hat Python_9781593271923.pdf' in cwdfiles('*.pdf'), True)
    delete_files('*9781593271923*.pdf')


def test_rencwdfiles():
    """Test the renaming of files in current directory"""
    delete_files('*deleteme*.pdf')
    rencwdfiles('*.pdf', 'default', PATT0)
    pdfs = cwdfiles('*.pdf')
    for f in FISBN:
        assert f not in pdfs
    rencwdfiles('*.pdf', 'default', PATT0)
    rencwdfiles('*.pdf', 'default', PATT2)
    pdfs = cwdfiles('*.pdf')
    for f in FISBN:
        assert f in pdfs
