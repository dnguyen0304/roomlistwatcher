# -*- coding: utf-8 -*-

import time


class Producer(object):

    def __init__(self, sender, source, filters=None):

        """
        Parameters
        ----------
        source : clare.common.messaging.producer.sources.Source
        sender : clare.common.messaging.producer.senders.Sender
        filters : typing.Iterable[clare.common.messaging.interfaces.IFilter]
            Defaults to list.
        """

        self._source = source
        self._sender = sender
        self._filters = filters or list()

    def produce(self, interval):

        """
        Parameters
        ----------
        interval : float
        """

        while True:
            self._produce_once()
            time.sleep(interval)

    def _produce_once(self):
        message = self._source.emit()
        for filter_ in self._filters:
            message = filter_.filter(message=message)
            if message is None:
                break
        else:
            self._sender.send(message=message)

    def __repr__(self):
        repr_ = '{}(source={}, sender={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._source,
                            self._sender,
                            self._filters)
