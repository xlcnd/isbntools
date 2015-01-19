#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import sys

from nose.tools import assert_equals
from isbnlib.dev.bouth23 import u, b, b2u3

from isbntools._lab import sprint
from isbntools.test.adapters import run_code

"""
nose tests
"""


def test_sprint1():
    try:
        sprint(u('海明威'))
    except:
        raise

def test_sprint2():
    code = "from isbnlib.dev.bouth23 import u;from isbntools._lab import sprint;sprint(u('abc'))"
    run_code(code)
    assert_equals(run_code(code), b('abc\n'))
