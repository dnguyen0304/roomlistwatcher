# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_is_none

from ..attempt import Attempt


class TestAttempt(object):

    def __init__(self):
        self.attempt = None

    def setup(self):
        self.attempt = Attempt.first(_get_now_in_seconds=lambda: 0)

    def test_first(self):
        assert_equal(self.attempt.number, 0)
        assert_equal(self.attempt.first_attempt_start_time, 0)
        assert_is_none(self.attempt.was_successful)
        assert_is_none(self.attempt.result)
        assert_is_none(self.attempt.exception)
