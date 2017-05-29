# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true

from .. import flush_strategies


class Mock(object):

    def __init__(self, start_time, next_time):
        self._start_time = start_time
        self._next_time = next_time
        self._call_counter = 0

    @classmethod
    def greater_than(cls, maximum_duration):
        start_time = 1.0
        next_time = start_time + maximum_duration + 1
        mock = cls(start_time=start_time, next_time=next_time)
        return mock

    @classmethod
    def equal_to(cls, maximum_duration):
        start_time = 1.0
        next_time = start_time + maximum_duration
        mock = cls(start_time=start_time, next_time=next_time)
        return mock

    @classmethod
    def less_than(cls, maximum_duration):
        start_time = 1.0
        next_time = start_time + maximum_duration - 1
        mock = cls(start_time=start_time, next_time=next_time)
        return mock

    def get_now_in_seconds(self):
        if self._call_counter == 0:
            now = self._start_time
        else:
            now = self._next_time
        self._call_counter += 1
        return now


class TestAfterDuration(object):

    def __init__(self):
        self.maximum_duration = None
        self.sequence = None

    def setup(self):
        self.maximum_duration = 0.0

    def test_should_flush_first_call_should_not_flush(self):
        flush_strategy = flush_strategies.AfterDuration(
            maximum_duration=None,
            _get_now_in_seconds=lambda: None)
        assert_false(flush_strategy.should_flush(sequence=self.sequence))

    def test_should_flush_greater_than_maximum_duration_should_flush(self):
        mock = Mock.greater_than(self.maximum_duration)
        flush_strategy = flush_strategies.AfterDuration(
            maximum_duration=self.maximum_duration,
            _get_now_in_seconds=mock.get_now_in_seconds)
        flush_strategy.should_flush(sequence=self.sequence)
        assert_true(flush_strategy.should_flush(sequence=self.sequence))

    def test_should_flush_equal_to_maximum_duration_should_flush(self):
        mock = Mock.equal_to(self.maximum_duration)
        flush_strategy = flush_strategies.AfterDuration(
            maximum_duration=self.maximum_duration,
            _get_now_in_seconds=mock.get_now_in_seconds)
        flush_strategy.should_flush(sequence=self.sequence)
        assert_true(flush_strategy.should_flush(sequence=self.sequence))

    def test_should_flush_less_than_maximum_duration_should_not_flush(self):
        mock = Mock.less_than(self.maximum_duration)
        flush_strategy = flush_strategies.AfterDuration(
            maximum_duration=self.maximum_duration,
            _get_now_in_seconds=mock.get_now_in_seconds)
        flush_strategy.should_flush(sequence=self.sequence)
        assert_false(flush_strategy.should_flush(sequence=self.sequence))


def test_after_size_should_flush_greater_than_maximum_size_should_flush():
    flush_strategy = flush_strategies.AfterSize(maximum_size=0)
    sequence = ['foo']
    assert_true(flush_strategy.should_flush(sequence=sequence))


def test_after_size_should_flush_equal_to_maximum_size_should_flush():
    flush_strategy = flush_strategies.AfterSize(maximum_size=1)
    sequence = ['foo']
    assert_true(flush_strategy.should_flush(sequence=sequence))


def test_after_size_should_flush_less_than_maximum_size_should_not_flush():
    flush_strategy = flush_strategies.AfterSize(maximum_size=2)
    sequence = ['foo']
    assert_false(flush_strategy.should_flush(sequence=sequence))
