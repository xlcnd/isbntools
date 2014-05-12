#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
nose tests
"""

from .. import merge
from nose.tools import assert_equals


def test_vias():
    assert_equals(len(repr(merge.query('9780321534965', 'parallel'))) in (173, 179), True)
    assert_equals(len(repr(merge.query('9780321534965', 'multi'))) in (173, 179), True)
    assert_equals(len(repr(merge.query('9780321534965', 'serial'))) in (173, 179), True)
