# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""nose tests for audit module."""

import os

from isbntools.contrib.modules.report import audit


def test_audit():
    """Test if the audit report runs without errors"""
    if os.getenv('GITHUB', '') != '':
        return True
    errcode = audit()
    assert errcode == 0
