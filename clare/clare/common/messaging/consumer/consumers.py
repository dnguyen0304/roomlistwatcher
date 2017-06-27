# -*- coding: utf-8 -*-

import time


class Consumer(object):

    def __init__(self, fetcher, handler, filters=None):

        """
        Parameters
        ----------
        fetcher : clare.common.messaging.consumer.fetchers.Fetcher
        handler : clare.common.messaging.consumer.interfaces.IHandler
        filters : collections.Iterable
            Defaults to list.
        """

        self._fetcher = fetcher
        self._handler = handler
        self._filters = filters or list()

    def consume(self, interval, timeout):

        """
        Parameters
        ----------
        interval : float
        timeout : float
        """

        while True:
            self._consume_once(timeout=timeout)
            time.sleep(interval)

    def _consume_once(self, timeout):
        record = self._fetcher.pop(timeout=timeout)
        for filter_ in self._filters:
            record = filter_.filter(record=record)
            if record is None:
                break
        else:
            self._handler.handle(record=record)

    def __repr__(self):
        repr_ = '{}(fetcher={}, handler={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._fetcher,
                            self._handler,
                            self._filters)
