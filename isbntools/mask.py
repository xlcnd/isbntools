# -*- coding: utf-8 -*-


import logging
from .data.data4mask import ranges
from .core import canonical, to_isbn13

LOGGER = logging.getLogger(__name__)


def mask(isbn, separator='-'):
    """ Transforms a canonical ISBN to a `masked` one

    `Mask` the ISBN, separating by identifier
    ISBN-10 identifiers: country-publisher-title-check
    ISBN-13 identifiers: EAN-country-publisher-title-check

    Used the iterative version of the `sliding-window` algorithm.
    Not pretty but fast! Lines 35-45 implement the search loop.
    O(n) for n - number of keys, if data structure like ranges in data4mask.py
    """
    ib = canonical(isbn)

    if (ib == ''): # empty input
        return None

    isbn10 = False
    if len(ib) == 10:
        check10 = ib[-1]
        ib = to_isbn13(ib) # convert to isbn-13
        isbn10 = True

    idx = None
    check = ib[-1]
    
    group = ib[0:3] + '-' + ib[3]
    cur = 3

    for _ in range(6):
        if group in ranges: # found EAN + country id:
            sevens = ib[cur + 1:cur + 8].ljust(7, '0')
            for l in ranges[group]:
                if l[0] <= int(sevens) <= l[1]: # found publisher id range and
                    idx = l[2]                  # length of publisher id
                    break
            break
        # didn't find EAN + country id:                               
        cur += 1
        if (cur < len(ib)):
            group = group + ib[cur]     # append the next digit and re-enter check loop

    if idx:
        if isbn10:
            group = group[4:]
            check = check10
        return separator.join([
            group,                      # ćountry id (prefixed with EAN for isbn-13)
            ib[cur + 1:cur + idx + 1],  # publisher id
            ib[cur + idx + 1:-1],       # title id
            check                       # check digit
            ])

    LOGGER.warning('identifier not found! Please, update the program.')
    return
