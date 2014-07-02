#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""
nose tests
"""

from .. import _merge as merge
from nose.tools import assert_equals


def test_vias():
    assert_equals(len(repr(merge.query('9780321534965', 'parallel'))) > 140, True)
    assert_equals(len(repr(merge.query('9780321534965', 'multi'))) > 140, True)
    assert_equals(len(repr(merge.query('9780321534965', 'serial'))) > 140, True)
