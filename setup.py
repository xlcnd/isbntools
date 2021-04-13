# -*- coding: utf-8 -*-
# flake8: noqa
"""
isbntools - extract, transform and metadata for ISBNs
Copyright (C) 2014-2021  Alexandre Lima Conde
SPDX-License-Identifier: LGPL-3.0-or-later

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

from datetime import datetime as dt

from setuptools import find_packages, setup

from isbntools import __version__

# PROJ
PROJECT_NAME = 'isbntools'
PROJECT_PACKAGE_NAME = 'isbntools'
PROJECT_LICENSE = 'LGPL v3'
PROJECT_LICENSE_URL = 'https://github.com/xlcnd/isbntools/blob/dev/LICENSE-LGPL-3.0.txt'
PROJECT_AUTHOR = 'Alexandre Lima Conde'
PROJECT_COPYRIGHT = ' 2014-{}, {}'.format(dt.now().year, PROJECT_AUTHOR)
PROJECT_URL = 'https://github.com/xlcnd/isbntools'
PROJECT_EMAIL = 'xlcnd@outlook.com'
PROJECT_VERSION = __version__

PROJECT_GITHUB_USERNAME = 'xlcnd'
PROJECT_GITHUB_REPOSITORY = 'isbntools'

GITHUB_PATH = '{}/{}'.format(PROJECT_GITHUB_USERNAME,
                             PROJECT_GITHUB_REPOSITORY)
GITHUB_URL = 'https://github.com/{}'.format(GITHUB_PATH)

DOWNLOAD_URL = '{}/archive/{}.zip'.format(GITHUB_URL, 'v' + PROJECT_VERSION)
PROJECT_URLS = {
    'Bug Reports': '{}/issues'.format(GITHUB_URL),
    'Dev Docs': 'https://isbntools.readthedocs.io/en/latest/devs.html',
    'Forum': 'https://stackoverflow.com/search?tab=newest&q=isbntools',
    'License': PROJECT_LICENSE_URL,
}

PYPI_URL = 'https://pypi.org/project/{}/'.format(PROJECT_PACKAGE_NAME)
PYPI_CLASSIFIERS = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: OS Independent',
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Text Processing :: General',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# SETUP

setup(
    name=PROJECT_PACKAGE_NAME,
    version=PROJECT_VERSION,
    url=PROJECT_URL,
    download_url=DOWNLOAD_URL,
    project_urls=PROJECT_URLS,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    license=PROJECT_LICENSE,
    packages=find_packages(exclude=['*.test', '*.test.*', 'test.*', 'test']),
    entry_points={
        'console_scripts': [
            'isbn_conf=isbntools.bin.confc:main',
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
            'isbn_classify=isbntools.bin.classify:main',
        ]
    },
    data_files=[('isbntools', ['isbntools/isbntools.conf'])],
    install_requires=['isbnlib>=3.10.7,<3.11.0'],
    description=
    "app and framework for 'all things ISBN' (International Standard Book Number) including metadata, descriptions, covers... .",
    long_description=open('README.rst').read(),
    keywords=
    'ISBN metadata Google_Books Open_Library Wikipedia BibTeX EndNote RefWorks MSWord BibJSON ISBN-A doi',
    classifiers=PYPI_CLASSIFIERS,
    tests_require=['nose', 'coverage'],
    test_suite='nose.collector',
)
