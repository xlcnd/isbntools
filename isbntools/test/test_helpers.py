#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""
nose tests
"""

from ..dev.helpers import last_first
from nose.tools import assert_equals


def test_last_first():
    assert_equals(last_first("Surname, First Name"), {"last": "Surname", "first": "First Name"})
    assert_equals(last_first("First Name Surname"), {"last": "Surname", "first": "First Name"})
    assert_equals(last_first("Surname1, First1 and Sur2, First2"), {"last": "Surname1", "first": "First1 and Sur2, First2"})
