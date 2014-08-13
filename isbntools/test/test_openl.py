#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

""" nose tests
NEEDS isbntools installed!
"""
from .. import meta
from nose.tools import assert_equals


def test_query():
    # test query from metadata
    assert_equals(len(repr(meta('9780195132861', 'openl'))) in (185, 191), True)
