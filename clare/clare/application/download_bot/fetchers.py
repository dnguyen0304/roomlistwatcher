# -*- coding: utf-8 -*-

import sys
import time

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import collections

from . import interfaces
from clare.common import messaging
from clare.common import utilities


class Fetcher(interfaces.IFetcher):

    def __init__(self, queue):

        """
        Parameters
        ----------
        queue : Queue.Queue
        """

        self._queue = queue

    def pop(self, block, timeout):
        try:
            record = self._queue.get(block=block, timeout=timeout)
        except queue.Empty:
            if not block or not timeout:
                message = 'The fetcher timed out immediately.'
            else:
                message = 'The fetcher timed out after {timeout} seconds.'.format(
                    timeout=timeout)
            raise messaging.consumer.exceptions.FetchTimeout(message)
        else:
            return record

    def __repr__(self):
        repr_ = '{}(queue={})'
        return repr_.format(self.__class__.__name__, self._queue)


class BufferingFetcher(interfaces.IFetcher):

    def __init__(self,
                 fetcher,
                 size,
                 _get_now_in_seconds=None,
                 _should_stop=None):

        """
        Parameters
        ----------
        fetcher : clare.application.download_bot.interfaces.IFetcher
        size : int
        _get_now_in_seconds : collections.Callable
            Used internally. Defaults to time.time.
        _should_stop : collections.Callable
            Used internally. Defaults to clare.common.utilities.should_stop.
        """

        self._fetcher = fetcher
        self._size = size
        self._get_now_in_seconds = _get_now_in_seconds or time.time
        self._should_stop = _should_stop or utilities.should_stop

        self._buffer = collections.deque()

    def pop(self, block, timeout):

        """
        If the buffer has records, then fetch from the buffer. If the
        buffer is empty, then fill from the queue before fetching. Both
        scenarios block and wait as specified.
        """

        start_time = self._get_now_in_seconds()

        if not self._buffer:
            for i in xrange(self._size):
                record = self._fetcher.pop(block=block, timeout=timeout)
                self._buffer.append(record)

                should_stop = self._should_stop(
                    maximum_duration=timeout,
                    start_time=start_time,
                    _get_now_in_seconds=self._get_now_in_seconds)

                if should_stop:
                    message = 'The fetcher timed out after at least {timeout} seconds.'
                    raise messaging.consumer.exceptions.FetchTimeout(
                        message.format(timeout=timeout))

        record = self._buffer.popleft()
        return record

    def __repr__(self):
        repr_ = '{}(fetcher={}, size={})'
        return repr_.format(self.__class__.__name__,
                            self._fetcher,
                            self._size)
