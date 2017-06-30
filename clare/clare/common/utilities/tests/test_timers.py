# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true

from .. import timer_factories


class MockGetNowInSeconds(object):

    def __init__(self, start_time, next_time):

        """
        Parameters
        -------
        start_time : float
        next_time : float
        """

        self._start_time = start_time
        self._next_time = next_time

        self._call_count = 0

    @classmethod
    def greater_than(cls, duration, start_time):
        next_time = (duration * 2) + start_time
        mock = cls(start_time=start_time, next_time=next_time)
        return mock

    @classmethod
    def equal_to(cls, duration, start_time):
        next_time = (duration * 1) + start_time
        mock = cls(start_time=start_time, next_time=next_time)
        return mock

    @classmethod
    def less_than(cls, duration, start_time):
        next_time = (duration * 0) + start_time
        mock = cls(start_time=start_time, next_time=next_time)
        return mock

    def __call__(self):
        if self._call_count == 0:
            now = self._start_time
        else:
            now = self._next_time
        self._call_count += 1
        return now

    def __repr__(self):
        repr_ = '{}(start_time={}, next_time={})'
        return repr_.format(self.__class__.__name__,
                            self._start_time,
                            self._next_time)


class TestCountdownTimer(object):

    def __init__(self):
        self.duration = None
        self.start_time = None
        self.timer_factory = None

    def setup(self):
        self.duration = 1.0
        self.start_time = 0.0
        self.timer_factory = timer_factories.CountdownTimerFactory()

    def test_greater_than_duration_should_stop(self):
        _get_not_in_seconds = MockGetNowInSeconds.greater_than(
            duration=self.duration,
            start_time=self.start_time)
        timer = self.timer_factory.create(
            duration=self.duration,
            _get_not_in_seconds=_get_not_in_seconds)

        should_stop = timer.should_stop()
        assert_true(should_stop)

    def test_equal_to_duration_should_stop(self):
        _get_not_in_seconds = MockGetNowInSeconds.equal_to(
            duration=self.duration,
            start_time=self.start_time)
        timer = self.timer_factory.create(
            duration=self.duration,
            _get_not_in_seconds=_get_not_in_seconds)

        should_stop = timer.should_stop()
        assert_true(should_stop)

    def test_less_than_duration_should_not_stop(self):
        _get_not_in_seconds = MockGetNowInSeconds.less_than(
            duration=self.duration,
            start_time=self.start_time)
        timer = self.timer_factory.create(
            duration=self.duration,
            _get_not_in_seconds=_get_not_in_seconds)

        should_stop = timer.should_stop()
        assert_false(should_stop)
