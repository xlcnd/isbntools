# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""Tests for the shelvecache."""

# TODO add more tests for other operations

from nose.tools import assert_equals
from ..app import editions, meta, registry

cache = registry.metadata_cache


def setup_module():
    meta('9780375869020')  #  <-- set
    editions('9780375869020')  #  <-- set


def teardown_module():
    del cache['9000000000000test']


def test_shelvecache_meta():
    """Test 'shelvecache' operations (set/get meta)."""
    print(cache.keys())
    assert_equals(
        len(repr(cache.get("query('9780375869020', 'default'){}"))) > 100,
        True)
    assert_equals(
        len(repr(cache.get("query('9780375869020', 'default'){}"))),
        len(repr(cache["query('9780375869020', 'default'){}"])),
    )


def test_shelvecache_editions():
    """Test 'shelvecache' operations (set/get editions)."""
    assert_equals(
        len(repr(cache.get("get_editions('9780375869020', 'merge'){}"))),
        len(repr(cache["get_editions('9780375869020', 'merge'){}"])),
    )


def test_shelvecache_setget():
    """Test 'shelvecache' operations (set/get test)."""
    cache.set('9000000000000test', {}, allow_empty=False)  #  <-- set
    assert_equals(cache.get('9000000000000test'), None)
    cache.set('9000000000000test', {}, allow_empty=True)  #  <-- set
    assert_equals(cache.get('9000000000000test'), {})


def test_shelvecache_contains():
    """Test 'shelvecache' operations (contains)."""
    assert_equals("query('9780375869020', 'default'){}" in cache, True)
