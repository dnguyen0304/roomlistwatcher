# -*- coding: utf-8 -*-

import collections

import mock
from nose.tools import assert_equal, assert_is_instance, assert_in

from .. import policy_builder


class MockObserver(policy_builder.INotifyable):

    def notify(self, event):
        pass


class TestObservable(object):

    def __init__(self):
        self.observable = None
        self.observer = None

    def setup(self):
        self.observable = policy_builder.Observable()
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

    observable_factory = policy_builder.ObservableFactory()
    observable = observable_factory.build()
    assert_is_instance(observable, policy_builder.INotifyable)


class TestBroker(object):

    def __init__(self):
        self.broker = None
        self.topic_name_1 = None
        self.topic_name_2 = None

    def setup(self):
        observable_factory = policy_builder.ObservableFactory()
        self.broker = policy_builder.Broker(
            observable_factory=observable_factory)
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
