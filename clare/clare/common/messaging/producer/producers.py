# -*- coding: utf-8 -*-

import time


class Producer(object):

    def __init__(self, sender, source, filters=None):

        """
        Parameters
        ----------
        source : clare.common.messaging.producer.interfaces.ISource
        sender : clare.common.messaging.producer.senders.Sender
        filters : collections.Iterable
            Defaults to list.
        """

        self._source = source
        self._sender = sender
        self._filters = filters or list()

    def produce(self, interval, timeout):

        """
        Parameters
        ----------
        interval : float
        timeout : float
        """

        while True:
            self._produce_once(timeout=timeout)
            time.sleep(interval)

    def _produce_once(self, timeout):
        record = self._source.emit()
        for filter_ in self._filters:
            record = filter_.filter(record=record)
            if record is None:
                break
        else:
            self._sender.push(record=record, timeout=timeout)

    def __repr__(self):
        repr_ = '{}(source={}, sender={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._source,
                            self._sender,
                            self._filters)
