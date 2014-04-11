
# isbntools - tools for extracting, cleaning and transforming ISBNs
# Copyright (C) 2014  Alexandre Lima Conde

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from setuptools import setup
from isbntools import __version__

scripts = ['bin/isbn_validate', 'bin/to_isbn10', 'bin/to_isbn13',
           'bin/isbn_mask', 'bin/isbn_info', 'bin/isbn_meta',
           'bin/isbntools', 'bin/isbn_stdin_validate',
           'bin/isbn_from_words', 'bin/isbn_editions',
           'bin/isbn_goom',
           ]


if "install" in sys.argv and os.name == 'nt':
    scripts = [s + '.py' for s in scripts]
    # rename files to '....py'
    for s in scripts:
        os.rename(s.split('.')[0], s)


def conf_file():
    homepath = os.path.expanduser('~') if os.name != 'nt' else os.getenv('APPDATA')
    confdir = '.isbntools' if os.name != 'nt' else 'isbntools'
    installpath = os.path.join(homepath, confdir)
    # no special needs for internal files!
    conf = 'isbntools/isbntools.conf'
    return (installpath, [conf])

data_files = []
data_files.append(conf_file())

setup(
    name='isbntools',
    version=__version__,
    author='xlcnd',
    author_email='xlcnd@outlook.com',
    url='https://github.com/xlcnd/isbntools',
    download_url='https://github.com/xlcnd/isbntools/archive/master.zip',
    packages=['isbntools', 'isbntools/dev', 'isbntools/data'],
    scripts=scripts,
    data_files=data_files,
    license='LGPL v3',
    description='Extract, clean, transform, hyphenate and metadata for ISBNs (International Standard Book Number).',
    long_description=open('README.rst').read(),
    keywords='ISBN, validate, transform, hyphenate, metadata, World Catalogue, Google Books, Open Library, isbndb.com, BibTeX, EndNote, RefWorks, MSWord, BibJSON',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Topic :: Text Processing :: General',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
