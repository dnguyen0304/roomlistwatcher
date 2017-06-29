# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true

from .. import utilities


class MockTimer(object):

    maximum_duration = 1.0

    def __init__(self, next_time):
        self._next_time = next_time

    @classmethod
    def greater_than(cls, start_time):
        next_time = start_time + (cls.maximum_duration * 2)
        mock_timer = cls(next_time=next_time)
        return mock_timer

    @classmethod
    def equal_to(cls, start_time):
        next_time = start_time + (cls.maximum_duration * 1)
        mock_timer = cls(next_time=next_time)
        return mock_timer

    @classmethod
    def less_than(cls, start_time):
        next_time = start_time + (cls.maximum_duration * 0)
        mock_timer = cls(next_time=next_time)
        return mock_timer

    def get_now_in_seconds(self):
        return self._next_time

    def __repr__(self):
        repr_ = '{}(next_time={})'
        return repr_.format(self.__class__.__name__, self._next_time)


class TestShouldStop(object):

    def __init__(self):
        self.start_time = None

    def setup(self):
        self.start_time = 0.0

    def test_greater_than_maximum_duration_should_stop(self):
        mock_timer = MockTimer.greater_than(start_time=self.start_time)
        should_stop = utilities.should_stop(
            maximum_duration=mock_timer.maximum_duration,
            start_time=self.start_time,
            _get_now_in_seconds=mock_timer.get_now_in_seconds)
        assert_true(should_stop)

    def test_equal_to_maximum_duration_should_stop(self):
        mock_timer = MockTimer.equal_to(start_time=self.start_time)
        should_stop = utilities.should_stop(
            maximum_duration=mock_timer.maximum_duration,
            start_time=self.start_time,
            _get_now_in_seconds=mock_timer.get_now_in_seconds)
        assert_true(should_stop)

    def test_less_than_maximum_duration_should_not_stop(self):
        mock_timer = MockTimer.less_than(start_time=self.start_time)
        should_stop = utilities.should_stop(
            maximum_duration=mock_timer.maximum_duration,
            start_time=self.start_time,
            _get_now_in_seconds=mock_timer.get_now_in_seconds)
        assert_false(should_stop)
