
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" nose tests
D25 |-> RELEASE MINIMAL TESTING. (I DON'T WANTED TO BE BLACKLISTED BY THE SERVICES) <-|
"""

from ..metadata import query
from ..ext import meta
from nose.tools import assert_equals, assert_raises


def test_query():
    # test query from metadata
    assert_raises(Exception, query, '9781849692342', 'goog')
    assert_equals(len(repr(query('9781849692342', 'goob'))), 208)
    assert_raises(Exception, query, '9781849692342', 'wcat')
    assert_equals(len(repr(query('9780321534965', 'wcat'))), 258)
    assert_equals(len(repr(query('9780321534965'))), 179)
    assert_equals(len(repr(query('9780321534965', 'merge'))), 179)
    assert_equals(len(repr(query('9780321534965', 'goob'))), 195)
    assert_equals(len(repr(query('9789934015960'))), 187)
    assert_equals(len(repr(query('9781118241257'))), 183)


def test_ext_meta():
    # test meta from core
    assert_equals(len(repr(meta('9781849692342', 'goob'))), 208)
    assert_equals(len(repr(meta('9780321534965', 'wcat'))), 258)
    assert_equals(len(repr(meta('9780321534965', 'merge'))), 179)
    assert_equals(len(repr(meta('9780321534965'))), 179)
# flake8: noqa
