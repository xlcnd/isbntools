#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" nose tests 
 
"""

from ..dev import Metadata, stdmeta
from nose.tools import assert_equals, assert_raises


def test_stdmeta():
    # test stdmeta from data
    r={
       'ISBN-13': u'9780123456789 ', 
       'Title': u'Bla. Bla /Title .', 
       'Publisher': u'', 
       'Year': u'2000', 
       'Language': u'en', 
       'Authors': [u'author1. mba', u'author2   ']
       }
    R={
       'ISBN-13': u'9780123456789', 
       'Title': u'Bla. Bla /Title .', 
       'Publisher': u'', 
       'Year': u'2000', 
       'Language': u'en', 
       'Authors': [u'author1. mba', u'author2']
       }
    A={
       'ISBN-13': u'9780123456789 ', 
       'Title': 'Bla. Bla /Title .', 
       'Publisher': u'', 
       'Year': '2000', 
       'Language': u'en', 
       'Authors': [u'author1. mba', u'author2   ']
       }   
    assert_equals(stdmeta(r), R)
    assert_equals(stdmeta(R), R)
    assert_raises(Exception, stdmeta, A)

def test_metaclass():
    R={
       'ISBN-13': u'9780123456789', 
       'Title': u'Bla. Bla /Title .', 
       'Publisher': u'', 
       'Year': u'2000', 
       'Language': u'en', 
       'Authors': [u'author1. mba', u'author2']
       }
    A={
       'ISBN-13': u'9780123456789', 
       'Title': u'Bla. Bla /Title .', 
       'Publisher': u'', 
       'Year': u'2000', 
       'Language': u'en', 
       'Authors': [u'author1. mba', u'author2']
       }
    B={
       'ISBN-13': u'9780123456789', 
       'Title': u'Bla. Bla /Title .', 
       'Publisher': u'', 
       'Year': u'2000', 
       'Language': u'en', 
       'Authors': [u'author1. mba', u'author2', u'Bambini']
       }
    dt=Metadata(R);  
    assert_equals(dt.canonical, R)
    dt.add_to_authors(u'Bambini')
    assert_equals(dt.canonical, B)


# flake8: noqa
