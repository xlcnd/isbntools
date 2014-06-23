#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
nose tests
"""

from ..modules.gwords import gwords as words
from nose.tools import assert_equals


def test_words():
    assert_equals(len(words.goos('the old man and the sea')), 13)
    # assert_equals(words.goos('-ISBN') in ('9781364200329', None), True)
