# -*- coding: utf-8 -*-

import time


class Consumer(object):

    def __init__(self, fetcher, handlers, filters=None):

        """
        Parameters
        ----------
        fetcher : clare.application.messaging.client.consumer.internals.fetchers.Fetcher
        handlers : collections.Iterable
        filters : collections.Iterable
            Defaults to list.
        """

        self._fetcher = fetcher
        self._handlers = handlers
        self._filters = filters or list()

    def consume(self, interval, timeout, _sleep=None):

        """
        Parameters
        ----------
        interval : float
        timeout : float
        _sleep : collections.Callable
            Used internally. Defaults to time.sleep.
        """

        _sleep = _sleep or time.sleep

        while True:
            self._consume_once(timeout=timeout)
            _sleep(interval)

    def _consume_once(self, timeout):
        record = self._fetcher.pop(timeout=timeout)
        for filter_ in self._filters:
            record = filter_.filter(record=record)
            if record is None:
                break
        else:
            for handler in self._handlers:
                handler.handle(record=record)

    def __repr__(self):
        repr_ = '{}(fetcher={}, handlers={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._fetcher,
                            self._handlers,
                            self._filters)
