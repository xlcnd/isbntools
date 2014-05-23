# -*- coding: utf-8 -*-

"""Format canonical in bibliographic formats."""

import re
import uuid
from string import Template
from ._helpers import last_first


bibtex = r"""@book{$ISBN,
     title = {$Title},
    author = {$AUTHORS},
      isbn = {$ISBN},
      year = {$Year},
 publisher = {$Publisher}
}"""

endnote = r"""%0 Book
%T $Title
%A $AUTHORS
%@ $ISBN
%D $Year
%I $Publisher """

refworks = r"""TY  - BOOK
T1  - $Title
A1  - $AUTHORS
SN  - $ISBN
Y1  - $Year
PB  - $Publisher
ER  - """

msword = r'''<b:Source xmlns:b="http://schemas.microsoft.com/office/'''\
         r'''word/2004/10/bibliography">
<b:Tag>$uid</b:Tag>
<b:SourceType>Book</b:SourceType>
<b:Author>
<b:NameList>$AUTHORS
</b:NameList>
</b:Author>
<b:Title>$Title</b:Title>
<b:Year>$Year</b:Year>
<b:City></b:City>
<b:Publisher>$Publisher</b:Publisher>
</b:Source>'''

json = r'''{"type": "book",
"title": "$Title",
"author": [$AUTHORS],
"year": "$Year",
"identifier": [{"type": "ISBN", "id": "$ISBN"}],
"publisher": "$Publisher"}'''

labels = r"""Type:      BOOK
Title:     $Title
Author:    $AUTHORS
ISBN:      $ISBN
Year:      $Year
Publisher: $Publisher"""

templates = {'labels': labels, 'bibtex': bibtex,
             'endnote': endnote, 'refworks': refworks,
             'msword': msword, 'json': json}

fmts = list(templates.keys())


def _gen_proc(name, canonical):
    if 'ISBN-13' in canonical:
        canonical['ISBN'] = canonical.pop('ISBN-13')
    tpl = templates[name]
    return Template(tpl).safe_substitute(canonical)


def _spec_proc(name, fmtrec, authors):
    """Fix the Authors records."""
    if name not in fmts:
        return
    if name == 'labels':
        AUTHORS = '\nAuthor:    '.join(authors)
    elif name == 'bibtex':
        AUTHORS = ' and '.join(authors)
    elif name == 'refworks':
        AUTHORS = '\nA1  - '.join(authors)
    elif name == 'endnote':
        AUTHORS = '\n%A '.join(authors)
    elif name == 'msword':
        fmtrec = fmtrec.replace('$uid', str(uuid.uuid4()))
        person = r"<b:Person><b:Last>$last</b:Last>"\
                 r"<b:First>$first</b:First></b:Person>"
        AUTHORS = '\n'.join(
            Template(person).safe_substitute(last_first(a))
            for a in authors)
    elif name == 'json':
        AUTHORS = ', '.join('{"name": "$"}'.replace("$", a)
                            for a in authors)
    return re.sub(r'\$AUTHORS', AUTHORS, fmtrec)


def fmtbib(fmtname, canonical):
    """Return a canonical record in the selected format."""
    return _spec_proc(fmtname, _gen_proc(fmtname, canonical),
                      canonical['Authors'])
