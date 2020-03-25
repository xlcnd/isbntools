# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""nose tests for audit module."""


from isbntools.contrib.modules.report import audit


def test_audit():
    """Test if the audit report runs without errors"""
    errcode = audit()
    assert errcode == 1
