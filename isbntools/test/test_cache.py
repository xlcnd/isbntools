# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""Tests for the shelvecache."""

# TODO add more tests for other operations

from nose.tools import assert_equals, assert_raises
from ..app import editions, meta, registry

cache = registry.metadata_cache


def setup_module():
    meta("9780375869020")  #  <-- set
    editions("9780375869020")  #  <-- set


def teardown_module():
    del cache["9000000000000test"]


def test_shelvecache_meta():
    """Test 'shelvecache' operations (set/get meta)."""
    assert_equals(len(repr(cache.get("9780375869020default"))) > 100, True)
    assert_equals(
        len(repr(cache.get("9780375869020default"))),
        len(repr(cache["9780375869020default"])))


def test_shelvecache_editions():
    """Test 'shelvecache' operations (set/get editions)."""
    assert_equals(len(repr(cache.get("ed9780375869020merge"))) > 12, True)
    assert_equals(
        len(repr(cache.get("ed9780375869020merge"))),
        len(repr(cache["ed9780375869020merge"])))


def test_shelvecache_setget():
    """Test 'shelvecache' operations (set/get test)."""
    cache.set("9000000000000test", {}, allow_empty=False)  #  <-- set
    assert_equals(cache.get("9000000000000test"), None)
    cache.set("9000000000000test", {}, allow_empty=True)  #  <-- set
    assert_equals(cache.get("9000000000000test"), {})
