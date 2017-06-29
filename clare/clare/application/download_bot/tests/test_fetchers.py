# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import mock
from nose.tools import assert_equal, raises

from .. import fetchers
from clare.common import messaging


class TestFetcher(object):

    def __init__(self):
        self.message_queue = None
        self.composed_fetcher = None
        self.fetcher = None

    def setup(self):
        self.message_queue = queue.Queue()
        self.composed_fetcher = messaging.consumer.fetchers.Fetcher(
            message_queue=self.message_queue)
        self.fetcher = fetchers.Fetcher(fetcher=self.composed_fetcher)

    def test_calculate_message_count(self):
        expected = len('foo')
        for i in xrange(expected):
            self.message_queue.put(i)
        assert_equal(self.fetcher.calculate_message_count(), expected)


class TestBuffering(object):

    def __init__(self):
        self.composed_fetcher = None
        self.size = None
        self.fetcher = None

    def setup(self):
        self.composed_fetcher = messaging.consumer.fetchers.Fetcher(
            message_queue=None)
        self.size = 2
        self.fetcher = fetchers.Buffering(fetcher=self.composed_fetcher,
                                          size=self.size)

    def test_does_fetch_when_buffer_is_empty(self):
        message_queue_size = self.size * 2
        side_effect = xrange(message_queue_size)
        self.composed_fetcher.pop = mock.Mock(side_effect=side_effect)
        for i in xrange(self.size + 1):
            self.fetcher.pop(timeout=None)
        assert_equal(self.composed_fetcher.pop.call_count, self.size * 2)

    def test_does_not_fetch_while_buffer_has_elements(self):
        message_queue_size = self.size * 2
        side_effect = xrange(message_queue_size)
        self.composed_fetcher.pop = mock.Mock(side_effect=side_effect)
        for i in xrange(self.size):
            self.fetcher.pop(timeout=None)
        assert_equal(self.composed_fetcher.pop.call_count, self.size)

    def test_is_ordered(self):
        message_queue_size = self.size * 2
        side_effect = expected = list(xrange(message_queue_size))
        self.composed_fetcher.pop = mock.Mock(side_effect=side_effect)
        records = [self.fetcher.pop(timeout=None) for i in expected]
        assert_equal(records, expected)

    @raises(messaging.consumer.exceptions.FetchTimeout)
    def test_raises_exception_on_timeout(self):
        side_effect = messaging.consumer.exceptions.FetchTimeout
        self.composed_fetcher.pop = mock.Mock(side_effect=side_effect)
        self.fetcher.pop(timeout=None)
