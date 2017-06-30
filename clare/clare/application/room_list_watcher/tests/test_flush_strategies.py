# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_false, assert_is_none, assert_true

from .. import flush_strategies
from clare.common import utilities


class TestAfterDuration(object):

    def __init__(self):
        self.maximum_duration = None
        self.start_time = None
        self.collection = None

    def setup(self):
        self.maximum_duration = 1.0
        self.start_time = 0.0

    def test_first_call_does_not_flush(self):
        timer_factory = utilities.timer_factories.CountdownTimerFactory()
        flush_strategy = flush_strategies.AfterDuration(
            maximum_duration=self.maximum_duration,
            timer_factory=timer_factory)
        should_flush = flush_strategy.should_flush(collection=self.collection)
        assert_false(should_flush)

    def test_timer_is_disposed_after_flushing(self):
        side_effect = (self.start_time,
                       self.start_time + self.maximum_duration)
        _get_now_in_seconds = mock.Mock(side_effect=side_effect)
        timer_factory = utilities.timer_factories.CountdownTimerFactory(
            _get_now_in_seconds=_get_now_in_seconds)
        flush_strategy = flush_strategies.AfterDuration(
            maximum_duration=self.maximum_duration,
            timer_factory=timer_factory)
        flush_strategy.should_flush(collection=self.collection)
        flush_strategy.should_flush(collection=self.collection)
        assert_is_none(flush_strategy._timer)


def test_after_size_should_flush_greater_than_maximum_size_should_flush():
    flush_strategy = flush_strategies.AfterSize(maximum_size=0)
    collection = ['foo']
    assert_true(flush_strategy.should_flush(collection=collection))


def test_after_size_should_flush_equal_to_maximum_size_should_flush():
    flush_strategy = flush_strategies.AfterSize(maximum_size=1)
    collection = ['foo']
    assert_true(flush_strategy.should_flush(collection=collection))


def test_after_size_should_flush_less_than_maximum_size_should_not_flush():
    flush_strategy = flush_strategies.AfterSize(maximum_size=2)
    collection = ['foo']
    assert_false(flush_strategy.should_flush(collection=collection))
