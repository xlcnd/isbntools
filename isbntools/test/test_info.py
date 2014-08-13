#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa


from .. import info
from nose.tools import assert_equals, assert_raises


def test_ext_info():
    assert_equals(info('9524712946'), 'Finland')
    assert_raises(Exception, info, '')


