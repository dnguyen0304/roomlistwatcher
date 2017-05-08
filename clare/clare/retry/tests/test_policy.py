# -*- coding: utf-8 -*-

import collections

import mock
from nose.tools import (assert_equal,
                        assert_greater,
                        assert_in,
                        assert_is_instance,
                        assert_items_equal,
                        raises)

from .. import PolicyBuilder, exceptions, stop_strategies, wait_strategies
from .. import policy


class MockObserver(policy.INotifyable):

    def notify(self, event):
        pass


class TestObservable(object):

    def __init__(self):
        self.observable = None
        self.observer = None

    def setup(self):
        self.observable = policy.Observable()
        self.observer = MockObserver()
        self.observer.notify = mock.Mock()
        self.observable.register(observer=self.observer)

    def test_register_adds_only_unique_observers(self):
        self.observable.register(observer=self.observer)
        self.observable.notify(event=None)
        assert_equal(self.observer.notify.call_count, 1)

    def test_notify_pushes_to_all_observers(self):
        observer_2 = MockObserver()
        observer_2.notify = mock.Mock()
        self.observable.register(observer=observer_2)
        self.observable.notify(event=None)
        assert_equal(self.observer.notify.call_count, 1)
        assert_equal(observer_2.notify.call_count, 1)


def test_observable_factory_build_returns_i_notifyable():

    observable_factory = policy.ObservableFactory()
    observable = observable_factory.build()
    assert_is_instance(observable, policy.INotifyable)


class TestBroker(object):

    def __init__(self):
        self.broker = None
        self.topic_name_1 = None
        self.topic_name_2 = None

    def setup(self):
        observable_factory = policy.ObservableFactory()
        self.broker = policy.Broker(observable_factory=observable_factory)
        self.topic_name_1 = 'foo'
        self.topic_name_2 = 'bar'

    def test_list_topics_returns_sequence(self):
        topic_names = self.broker.list_topics()
        assert_is_instance(topic_names, collections.Sequence)

    def test_create_topic(self):
        self.broker.create_topic(name=self.topic_name_1)
        topic_names = self.broker.list_topics()
        assert_in(self.topic_name_1, topic_names)

    def test_create_topic_creates_only_unique_topics(self):
        self.broker.create_topic(name=self.topic_name_1)
        self.broker.create_topic(name=self.topic_name_1)
        topic_names = self.broker.list_topics()
        assert_equal(len(topic_names), 1)

    def test_publish_pushes_to_all_subscribers_by_topic_name(self):
        self.broker.create_topic(name=self.topic_name_1)
        self.broker.create_topic(name=self.topic_name_2)

        subscriber_1 = MockObserver()
        subscriber_1.notify = mock.Mock()
        subscriber_2 = MockObserver()
        subscriber_2.notify = mock.Mock()

        self.broker.subscribe(subscriber=subscriber_1,
                              topic_name=self.topic_name_1)
        self.broker.subscribe(subscriber=subscriber_2,
                              topic_name=self.topic_name_2)

        self.broker.publish(event=None, topic_name='foo')

        assert_equal(subscriber_1.notify.call_count, 1)
        assert_equal(subscriber_2.notify.call_count, 0)


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
        assert_equal(pre_hook.call_count, 1)

    def test_execute_add_pre_hook_context(self):
        def pre_hook(context):
            expected = ('attempt_number',)
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
