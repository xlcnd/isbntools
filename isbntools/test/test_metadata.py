#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

"""nose tests for metadata."""

from .. import meta
from nose.tools import assert_equals, assert_raises


def test_ext_meta():
    # test meta from core
    assert_equals(len(repr(meta('9781849692342', 'goob'))) in (201, 208), True)
    assert_equals(len(repr(meta('9780321534965', 'wcat'))) > 150, True)
    assert_equals(len(repr(meta('9780321534965', 'merge'))) in (173, 179), True)
    assert_equals(len(repr(meta('9780321534965'))) in (173, 179), True)
    assert_raises(Exception, meta, '9780000000', 'wcat', None)
    assert_raises(Exception, meta, randrange(0, 1000000), 'wcat')
