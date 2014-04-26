#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
nose tests
"""

from ..dev import goom
from nose.tools import assert_equals


def test_goom():
    assert_equals(len(repr(goom.query('the old man and the sea'))) > 1000, True)
