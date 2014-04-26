#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
nose tests
"""

from .. import words
from nose.tools import assert_equals


def test_goom():
    assert_equals(len(words.goos('the old man and the sea')), 13)
