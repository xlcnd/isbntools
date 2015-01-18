#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import sys

from isbnlib.dev.bouth23 import u

from isbntools._lab import sprint


"""
nose tests
"""


def test_sprint():
    try:
        sprint(u('海明威'))
    except:
        raise
