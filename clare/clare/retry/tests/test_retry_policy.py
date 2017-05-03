# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equal

from .. import AfterAttempt, AfterNever, FixedWaitStrategy, RetryPolicy


class MockException(Exception):
    pass


class MockService(object):

    def __init__(self):
        self.call_count = 0

    def call(self):
        self.call_count += 1

    def call_and_raise(self):
        self.call_count += 1
        if self.call_count == 1:
            raise MockException

    @staticmethod
    def call_and_return():
        return 'foo'


class TestRetryPolicy(object):

    def __init__(self):
        self.service = None
        self.handled_exceptions = None

    def setup(self):
        self.service = MockService()
        self.handled_exceptions = (MockException,)

    def test_execute_stop_after_success(self):
        stop_strategy = AfterNever()
        wait_time = 0
        wait_strategy = FixedWaitStrategy(wait_time=wait_time)
        retry_policy = RetryPolicy(stop_strategy=stop_strategy,
                                   wait_strategy=wait_strategy)
        retry_policy.execute(callable=self.service.call)
        assert_equal(self.service.call_count, 1)

    def test_execute_wait(self):
        maximum_attempt = 2
        stop_strategy = AfterAttempt(maximum_attempt=maximum_attempt)
        wait_time = None
        wait_strategy = FixedWaitStrategy(wait_time=wait_time)

        retry_policy = RetryPolicy(stop_strategy=stop_strategy,
                                   wait_strategy=wait_strategy,
                                   handled_exceptions=self.handled_exceptions)

        _sleep = mock.MagicMock()
        retry_policy.execute(callable=self.service.call_and_raise,
                             _sleep=_sleep)
        _sleep.assert_called()

    def test_execute_successful_attempt_returns_result(self):
        stop_strategy = AfterNever()
        wait_time = 0
        wait_strategy = FixedWaitStrategy(wait_time=wait_time)
        retry_policy = RetryPolicy(stop_strategy=stop_strategy,
                                   wait_strategy=wait_strategy)
        result = retry_policy.execute(callable=self.service.call_and_return)
        assert_equal(result, 'foo')

    def test_execute_continue_on_handled_exceptions(self):
        maximum_attempt = 2
        stop_strategy = AfterAttempt(maximum_attempt=maximum_attempt)
        wait_time = 0
        wait_strategy = FixedWaitStrategy(wait_time=wait_time)
        retry_policy = RetryPolicy(stop_strategy=stop_strategy,
                                   wait_strategy=wait_strategy,
                                   handled_exceptions=self.handled_exceptions)
        retry_policy.execute(callable=self.service.call_and_raise)
        assert_equal(self.service.call_count, maximum_attempt)
