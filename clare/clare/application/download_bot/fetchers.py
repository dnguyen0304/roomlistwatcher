# -*- coding: utf-8 -*-

import collections

from clare.common import messaging


class Buffering(messaging.consumer.interfaces.IFetcher):

    def __init__(self, fetcher, size):

        """
        Parameters
        ----------
        fetcher : clare.common.messaging.consumer.interfaces.IFetcher
        size : int
        """

        self._fetcher = fetcher
        self._size = size
        self._buffer = collections.deque()

    def pop(self, timeout):
        if not self._buffer:
            for i in xrange(self._size):
                try:
                    record = self._fetcher.pop(timeout=timeout)
                except messaging.consumer.exceptions.FetchTimeout:
                    break
                else:
                    self._buffer.append(record)
        try:
            record = self._buffer.popleft()
        except IndexError:
            message = 'The fetcher timed out after {timeout} seconds.'
            raise messaging.consumer.exceptions.FetchTimeout(
                message.format(timeout=timeout))
        return record

    def __repr__(self):
        repr_ = '{}(fetcher={}, size={})'
        return repr_.format(self.__class__.__name__,
                            self._fetcher,
                            self._size)
