# -*- coding: utf-8 -*-
# flake8: noqa
"""Install file for isbntools."""

"""
isbntools - extract, transform and metadata for ISBNs
Copyright (C) 2014-2018  Alexandre Lima Conde

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

import os
import sys

from shutil import copy2 as copyfile

from isbntools import __version__

#import pkg_resources

from setuptools import find_packages, setup


# ENV

ARGVS = sys.argv
FIRSTRUN = 'egg_info' in ARGVS
PIP = '-c' in ARGVS
INSTALL = any((m in ARGVS for m in ('install', 'develop'))) or PIP
WINDOWS = os.name == 'nt'
PY2 = sys.version < '3'
PY3 = not PY2
VIRTUAL = getattr(sys, 'base_prefix', sys.prefix) != sys.prefix or hasattr(sys, 'real_prefix')
SECONDRUN = INSTALL and not FIRSTRUN


# CHECK SUPPORT
if INSTALL and FIRSTRUN:
    SUPPORTED = ((2, 7), (3, 4), (3, 5), (3, 6))
    if tuple(int(x) for x in sys.version[:3].split('.')) not in SUPPORTED:
        raise Exception('isbntools %s  requires Python 2.7+ or 3.4+.' %
                        __version__)


# DEFS

CONFDIR = '.isbntools' if not WINDOWS and not VIRTUAL else 'isbntools'
CONFFILE = 'isbntools.conf'
#CONFRES = pkg_resources.resource_filename('isbntools', CONFFILE)
CONFRES = 'isbntools/' + CONFFILE


# HELPERS

def uxchown(fp):
    if WINDOWS:
        return
    from pwd import getpwnam, getpwuid
    from grp import getgrnam, getgrgid
    uid = getpwnam(os.getenv("SUDO_USER", getpwuid(os.getuid()).pw_name)).pw_uid
    gid = getgrnam(os.getenv("SUDO_USER", getgrgid(os.getgid()).gr_name)).gr_gid
    os.chown(fp, uid, gid)


def data_path():
    if VIRTUAL:
        installpath = CONFDIR
    else:
        user = '~%s' % os.getenv("SUDO_USER", '')
        homepath = os.path.expanduser(user) if not WINDOWS else os.getenv('APPDATA')
        installpath = os.path.join(homepath, CONFDIR)
        if not os.path.exists(installpath) and INSTALL:
            print('making data dir %s' % installpath)
            try:
                os.mkdir(installpath)
                uxchown(installpath)
            except:
                print("Warning: %s not properly setuped!" % installpath)
                return
    return installpath


def backup_file(fp):
    """Append _ORIGINAL or _BACKUP to the file name."""
    if os.path.isfile(fp):
        name, ext = os.path.splitext(fp)
        newfp = name + '_ORIGINAL' + ext
        if os.path.isfile(newfp):
            newfp = name + '_BACKUP' + ext
        return copyfile(fp, newfp)
    return


def backup():
    if VIRTUAL:
        places = [os.path.join(sys.prefix, CONFDIR + '/isbntools.conf')]
    else:
        if WINDOWS:
            places = [os.path.join(os.getenv('APPDATA'), 'isbntools/isbntools.conf')]
        else:
            places = [
                '/etc/.isbntools/isbntools.conf',
                '/usr/local/bin/isbntools.conf',
                '/usr/local/isbntools.conf',
                os.path.expanduser('~/.isbntools.conf'),
                os.path.expanduser('~/.local/.isbntools/isbntools.conf'),
                os.path.expanduser('~/.isbntools/isbntools.conf'),
                os.path.expanduser('~/isbntools/isbntools.conf'),
            ]
    for place in reversed(places):
        if os.path.isfile(place):
            print('Backup isbntools.conf ...')
            backup_file(place)


def protect(datapath):
    """Recovers 'protected' datafiles."""
    fn = 'isbntools.conf'
    fbase, ext = os.path.splitext(fn)
    backf = fbase + '_BACKUP' + ext
    backfp = os.path.join(datapath, backf)
    if os.path.isfile(backfp):
        fnp = os.path.join(datapath, fn)
        copyfile(backfp, fnp)
        print('file %s restored' % fn)
        return True
    orif = fbase + '_ORIGINAL' + ext
    orifp = os.path.join(datapath, orif)
    if os.path.isfile(orifp):
        fnp = os.path.join(datapath, fn)
        copyfile(orifp, fnp)
        print('file %s restored' % fn)
        return True
    return False


# PRE-SETUP

# pip deletes the original files on FIRSTRUN (even if they have been customized!)
# so, before that, do a backup ...
if FIRSTRUN:
    try:
        backup()
    except:
        print("Warning: previous 'isbntools.conf' found but backup wasn't done!")

# define data_files
DATAPATH = data_path()
data_files = [(DATAPATH, [CONFRES])] if DATAPATH else []


# SETUP

setup(
    name='isbntools',
    version='4.3.14',
    author='xlcnd',
    author_email='xlcnd@outlook.com',
    url='https://github.com/xlcnd/isbntools',
    download_url='https://github.com/xlcnd/isbntools/archive/v4.3.14.zip',
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    entry_points={
        'console_scripts': ['isbn_conf=isbntools.bin.confc:main',
                            'isbn_doi=isbntools.bin.doi:main',
                            'isbn_doi2tex=isbntools.bin.doi2tex:main',
                            'isbn_ean13=isbntools.bin.ean13:main',
                            'isbn_editions=isbntools.bin.editions:main',
                            'isbn_from_words=isbntools.bin.from_words:main',
                            'isbn_goom=isbntools.bin.goom:main',
                            'isbn_info=isbntools.bin.info:main',
                            'isbn_mask=isbntools.bin.mask:main',
                            'isbn_meta=isbntools.bin.meta:main',
                            'isbn_ren=isbntools.bin.ren:main',
                            'to_isbn10=isbntools.bin.to_isbn10:main',
                            'to_isbn13=isbntools.bin.to_isbn13:main',
                            'isbn_validate=isbntools.bin.validate:main',
                            'isbn_stdin_validate=isbntools.bin.validate:do_pipe',
                            'isbntools=isbntools.bin.version:main',
                            'isbn_repl=isbntools.bin.repl:main',
                            'isbn_cover=isbntools.bin.cover:main',
                            'isbn_desc=isbntools.bin.desc:main',
                            ]},
    data_files=data_files,
    install_requires=['isbnlib>=3.8.4,<3.9.0'],
    license='LGPL v3',
    description="app and framework for 'all things ISBN' (International Standard Book Number) including metadata, descriptions, covers... .",
    long_description=open('README.rst').read(),
    keywords='ISBN metadata World_Catalogue Google_Books Open_Library BibTeX EndNote RefWorks MSWord BibJSON ISBN-A doi',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Topic :: Text Processing :: General',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=['nose', 'coverage'],
    test_suite='nose.collector',
)


# POS-SETUP

if not VIRTUAL and not WINDOWS and SECONDRUN:
    conffile = os.path.join(DATAPATH, CONFFILE)
    if not os.path.exists(conffile):
        print("Warning: file %s doesn't exist! Use 'isbn_conf make'" % conffile)
        sys.exit()
    try:
        uxchown(conffile)
        print('changing mode of %s to 666' % conffile)
    except:
        print('Warning: permissions not set for file %s' % conffile)

if SECONDRUN:
    try:
        datapath = os.path.join(sys.prefix, CONFDIR) if VIRTUAL else DATAPATH
        protect(datapath)
    except:
        print("Warning: isbntools.conf wasn't restored.")
