#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" nose tests

"""

from ..dev import Metadata, stdmeta
from nose.tools import assert_equals, assert_raises
from ..bouth23 import u


def test_stdmeta():
    # test stdmeta from data
    r={
       'ISBN-13': u('9780123456789 '),
       'Title': u('Bla. Bla /Title .'),
       'Publisher': u(''),
       'Year': u('2000'),
       'Language': u('en'),
       'Authors': [u('author1. mba'), u('author2   ')]
       }
    R={
       'ISBN-13': u('9780123456789'),
       'Title': u('Bla. Bla /Title .'),
       'Publisher': u(''),
       'Year': u('2000'),
       'Language': u('en'),
       'Authors': [u('author1. mba'), u('author2')]
       }
    A={
       'ISBN-13': u('9780123456789 '),
       'Title': b'Bla. Bla /Title .',
       'Publisher': u(''),
       'Year': b'2000',
       'Language': u('en'),
       'Authors': [u('author1. mba'), u('author2   ')]
       }
    assert_equals(stdmeta(r), R)
    assert_equals(stdmeta(R), R)
    assert_raises(Exception, stdmeta, A)

def test_metaclass():
    R={
       'ISBN-13': u('9780123456789'),
       'Title': u('Bla. Bla /Title .'),
       'Publisher': u(''),
       'Year': u('2000'),
       'Language': u('en'),
       'Authors': [u('author1. mba'), u('author2')]
       }
    A={
       'ISBN-13': u('9780123456789'),
       'Title': u('Bla. Bla /Title .'),
       'Publisher': u(''),
       'Year': u('2000'),
       'Language': u('en'),
       'Authors': [u('author1. mba'), u('author2')]
       }
    dt = Metadata(R)
    assert_equals(dt.value, R)


# flake8: noqa
