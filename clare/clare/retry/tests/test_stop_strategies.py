# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true

from .. import Attempt, AfterAttempt


def test_after_attempt_should_stop():

    maximum_attempt = 1
    stop_strategy = AfterAttempt(maximum_attempt=maximum_attempt)
    attempt = Attempt(number=1,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(stop_strategy.should_stop(attempt=attempt))


def test_after_attempt_should_not_stop():

    maximum_attempt = 1
    stop_strategy = AfterAttempt(maximum_attempt=maximum_attempt)
    attempt = Attempt(number=0,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_false(stop_strategy.should_stop(attempt=attempt))


def test_after_attempt_prioritizes_success():

    maximum_attempt = 10
    stop_strategy = AfterAttempt(maximum_attempt=maximum_attempt)
    attempt = Attempt(number=None,
                      was_successful=True,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(stop_strategy.should_stop(attempt=attempt))
