# -*- coding: utf-8 -*-

import mock
from nose.tools import (assert_equal,
                        assert_greater,
                        assert_items_equal,
                        raises)

from .. import PolicyBuilder, exceptions, stop_strategies, wait_strategies


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

    def call_and_return(self):
        self.call_count += 1
        return 'foo'


class TestPolicy(object):

    def __init__(self):
        self.service = None

    def setup(self):
        self.service = MockService()

    def test_execute_stop_after_success(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .build()
        policy.execute(callable=self.service.call)
        assert_equal(self.service.call_count, 1)

    def test_execute_failed_attempt_does_wait(self):
        _sleep = mock.MagicMock()
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterAttempt(maximum_attempt=2)) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=None)) \
            .continue_on_exception(MockException) \
            .build()
        policy.execute(callable=self.service.call_and_raise, _sleep=_sleep)
        _sleep.assert_called()

    def test_execute_successful_attempt_returns_result(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .build()
        result = policy.execute(callable=self.service.call_and_return)
        assert_equal(result, 'foo')

    @raises(MockException)
    def test_execute_raises_exception(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .build()
        policy.execute(callable=self.service.call_and_raise)

    def test_execute_continue_on_exception(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterAttempt(maximum_attempt=2)) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .continue_on_exception(MockException) \
            .build()
        policy.execute(callable=self.service.call_and_raise)
        assert_greater(self.service.call_count, 1)

    def test_execute_continue_if_result(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterAttempt(maximum_attempt=2)) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .continue_if_result(predicate=lambda x: x == 'foo') \
            .build()
        try:
            policy.execute(callable=self.service.call_and_return)
        except exceptions.MaximumRetry:
            assert_greater(self.service.call_count, 1)

    def test_execute_add_pre_hook(self):
        pre_hook = mock.MagicMock()
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .add_pre_hook(pre_hook) \
            .build()
        policy.execute(callable=self.service.call_and_return)
        assert_equal(pre_hook.call_count, 2)

    def test_execute_add_pre_hook_context(self):
        def pre_hook(context):
            expected = ('previous_attempt_was_successful',
                        'current_attempt_number',
                        'is_stopping',
                        'is_continuing')
            assert_items_equal(context, expected)
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .add_pre_hook(pre_hook) \
            .build()
        policy.execute(callable=self.service.call_and_return)

    def test_execute_add_post_hook(self):
        post_hook = mock.MagicMock()
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .add_post_hook(post_hook) \
            .build()
        policy.execute(callable=self.service.call_and_return)
        assert_equal(post_hook.call_count, 1)

    def test_execute_add_post_hook_context(self):
        def post_hook(context):
            expected = ('result', 'exception', 'next_wait_time')
            assert_items_equal(context, expected)
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .add_post_hook(post_hook) \
            .build()
        policy.execute(callable=self.service.call_and_return)
