# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import mock
from nose.tools import (assert_equal,
                        assert_false,
                        assert_in,
                        assert_raises,
                        raises)

from .. import fetchers
from clare.common import messaging


class TestFetcher(object):

    def __init__(self):
        self.queue = None
        self.fetcher = None

    def setup(self):
        self.queue = queue.Queue()
        self.fetcher = fetchers.Fetcher(queue=self.queue)

    def test_raises_exception_if_not_blocking(self):
        block = False
        timeout = None

        with assert_raises(messaging.consumer.exceptions.FetchTimeout) as context:
            self.fetcher.pop(block=block, timeout=timeout)
        assert_in('immediate', context.exception.message)

    def test_raises_exception_on_timeout(self):
        block = True
        timeout = 0.001

        with assert_raises(messaging.consumer.exceptions.FetchTimeout) as context:
            self.fetcher.pop(block=block, timeout=timeout)
        assert_in(str(timeout), context.exception.message)

    def test_raises_exception_on_immediate_timeout(self):
        block = True
        timeout = 0.0

        with assert_raises(messaging.consumer.exceptions.FetchTimeout) as context:
            self.fetcher.pop(block=block, timeout=timeout)
        assert_in('immediate', context.exception.message)


class TestBufferingFetcher(object):

    def __init__(self):
        self.queue = None
        self.composed_fetcher = None
        self.size = None
        self.fetcher = None

    def setup(self):
        self.queue = queue.Queue()
        self.composed_fetcher = fetchers.Fetcher(queue=self.queue)
        self.size = 2
        countdown_timer = self.create_mock_countdown_timer(
            has_time_remaining=True)
        self.fetcher = fetchers.BufferingFetcher(
            fetcher=self.composed_fetcher,
            size=self.size,
            countdown_timer=countdown_timer)

    def test_does_fetch_when_buffer_is_empty(self):
        side_effect = xrange(self.size)
        self.composed_fetcher.pop = mock.Mock(side_effect=side_effect)
        self.fetcher.pop(block=True, timeout=None)

        assert_equal(self.composed_fetcher.pop.call_count, self.size)

    def test_does_not_fetch_while_buffer_has_records(self):
        for i in xrange(self.size):
            self.queue.put(i)

        # The composed fetcher should not be called on the second
        # round.
        self.fetcher.pop(block=True, timeout=None)
        self.composed_fetcher.pop = mock.Mock()
        self.fetcher.pop(block=True, timeout=None)

        assert_false(self.composed_fetcher.pop.called)

    def test_is_ordered(self):
        expected = list()
        records = list()

        # These loops cannot be merged because there are not enough
        # messages enqueued for the buffer.
        for i in xrange(self.size):
            expected.append(i)
            self.queue.put(i)
        for i in xrange(self.size):
            records.append(self.fetcher.pop(block=False, timeout=None))

        assert_equal(records, expected)

    @raises(messaging.consumer.exceptions.FetchTimeout)
    def test_raises_exception_on_timeout(self):
        self.fetcher.pop(block=False, timeout=None)

    def test_raises_exception_on_buffering_timeout(self):
        countdown_timer = self.create_mock_countdown_timer(
            has_time_remaining=False)
        fetcher = fetchers.BufferingFetcher(fetcher=self.composed_fetcher,
                                            size=self.size,
                                            countdown_timer=countdown_timer)
        for i in xrange(self.size):
            self.queue.put(i)

        timeout = 0.001

        with assert_raises(messaging.consumer.exceptions.FetchTimeout) as context:
            fetcher.pop(block=True, timeout=timeout)
        assert_in('at least', context.exception.message)
        assert_in(str(timeout), context.exception.message)

    @staticmethod
    def create_mock_countdown_timer(has_time_remaining):

        """
        Parameters
        ----------
        has_time_remaining : bool
        """

        countdown_timer = mock.Mock()
        has_time_remaining = mock.PropertyMock(return_value=has_time_remaining)
        type(countdown_timer).has_time_remaining = has_time_remaining
        return countdown_timer
