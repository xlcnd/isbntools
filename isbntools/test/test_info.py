#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ..infogroup import infogroup
from nose.tools import assert_equals


# nose tests
def test_infogroup():
    assert_equals(infogroup('9789720404427'), 'Portugal')
    assert_equals(infogroup('720404427'), 'China')
    assert_equals(infogroup('9524712946'), 'Finland')
    assert_equals(infogroup('0330284983'),
                  'English - (UK, US, Australia, NZ, Canada,South Africa, Zimbabwe) [Ireland, Puerto Rico, Swaziland]')
    assert_equals(infogroup('3796519008'),
                  'German (Germany, Austria, Switzerland)')
    assert_equals(infogroup('92xxxxxxxxxxx'), None)
    assert_equals(infogroup(''), None)
    assert_equals(infogroup('9791090636071'), 'France')
