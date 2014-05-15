#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

""" nose tests
D25 |-> RELEASE MINIMAL TESTING. (I DON'T WANTED TO BE BLACKLISTED BY THE SERVICES) <-|
"""

from ..metadata import query
from ..ext import meta
from nose.tools import assert_equals, assert_raises


def test_query():
    # test query from metadata
    assert_raises(Exception, query, '9781849692342', 'goog')
    assert_equals(len(repr(query('9781849692342', 'goob'))) in (201, 208), True)
    assert_raises(Exception, query, '9781849692342', 'wcat')
    assert_equals(len(repr(query('9780321534965', 'wcat'))) in (252, 258), True)
    assert_equals(len(repr(query('9780321534965'))) in (173, 179), True)
    assert_equals(len(repr(query('9780321534965', 'merge'))) in (173, 179), True)
    assert_equals(len(repr(query('9780321534965', 'goob'))) in (189, 195), True)
    assert_equals(len(repr(query('9789934015960'))) in (166, 187), True)
    assert_equals(len(repr(query('9781118241257'))) in (177, 183), True)


def test_ext_meta():
    # test meta from core
    assert_equals(len(repr(meta('9781849692342', 'goob'))) in (201, 208), True)
    assert_equals(len(repr(meta('9780321534965', 'wcat'))) in (252, 258), True)
    assert_equals(len(repr(meta('9780321534965', 'merge'))) in (173, 179), True)
    assert_equals(len(repr(meta('9780321534965'))) in (173, 179), True)
