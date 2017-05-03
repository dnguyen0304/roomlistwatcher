# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from .. import Fixed


def test_fixed_wait_time():

    wait_time = 1
    wait_strategy = Fixed(wait_time=wait_time)
    attempt = None
    output = wait_strategy.compute_wait_time(attempt=attempt)
    assert_equal(output, wait_time)
