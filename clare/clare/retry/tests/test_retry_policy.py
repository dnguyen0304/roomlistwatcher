# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equal, assert_greater

from .. import RetryPolicy, stop_strategies, wait_strategies


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
        retry_policy = RetryPolicy(
            stop_strategy=stop_strategies.AfterNever(),
            wait_strategy=wait_strategies.Fixed(wait_time=0))
        retry_policy.execute(callable=self.service.call)
        assert_equal(self.service.call_count, 1)

    def test_execute_wait(self):
        _sleep = mock.MagicMock()
        retry_policy = RetryPolicy(
            stop_strategy=stop_strategies.AfterAttempt(maximum_attempt=2),
            wait_strategy=wait_strategies.Fixed(wait_time=None),
            handled_exceptions=self.handled_exceptions)
        retry_policy.execute(callable=self.service.call_and_raise,
                             _sleep=_sleep)
        _sleep.assert_called()

    def test_execute_successful_attempt_returns_result(self):
        retry_policy = RetryPolicy(
            stop_strategy=stop_strategies.AfterNever(),
            wait_strategy=wait_strategies.Fixed(wait_time=0))
        result = retry_policy.execute(callable=self.service.call_and_return)
        assert_equal(result, 'foo')

    def test_execute_continue_on_handled_exceptions(self):
        retry_policy = RetryPolicy(
            stop_strategy=stop_strategies.AfterAttempt(maximum_attempt=2),
            wait_strategy=wait_strategies.Fixed(wait_time=0),
            handled_exceptions=self.handled_exceptions)
        retry_policy.execute(callable=self.service.call_and_raise)
        assert_greater(self.service.call_count, 1)
