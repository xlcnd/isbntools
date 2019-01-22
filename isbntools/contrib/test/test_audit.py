# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

import sys

from isbntools.contrib.modules.report import audit
"""
nose tests
"""


def test_audit():
    """Test if the audit report runs without errors"""
    errcode = audit()
    #assert errcode == 0
