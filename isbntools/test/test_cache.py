# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""Tests for the shelvecache."""

# TODO add more tests for other operations

from nose.tools import assert_equals, assert_raises
from ..app import editions, meta, registry

cache = registry.metadata_cache


def setup_module():
    meta("9780375869020")      #  <-- set
    editions("9780375869020")  #  <-- set


def test_shelvecache_meta():
    """Test 'shelvecache' operations (set/get meta)."""
    assert_equals(len(repr(cache.get("9780375869020default"))) > 100, True)


def test_shelvecache_editions():
    """Test 'shelvecache' operations (set/get editions)."""
    assert_equals(len(repr(cache.get("ed9780375869020merge"))) > 12, True)
