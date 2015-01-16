#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
nose tests
"""

from .. import isbn_from_words
from nose.tools import assert_equals


def test_words():
    assert_equals(len(isbn_from_words('the old man and the sea')), 13)
    assert_equals(isbn_from_words('-ISBN -isbn') in ('9781364200329', None), True)
