# -*- coding: utf-8 -*-

import abc
import time


class Producer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def produce(self):

        """
        Emit and send data.

        Returns
        -------
        None
        """

        raise NotImplementedError


class Blocking(Producer):

    def __init__(self, sender, source, filters=None):

        """
        Parameters
        ----------
        source : room_list_watcher.common.messaging.producer.sources.Source
        sender : room_list_watcher.common.messaging.producer.senders.Sender
        filters : typing.Iterable[room_list_watcher.common.messaging.filters.StringFilter]
            Defaults to list.
        """

        self._source = source
        self._sender = sender
        self._filters = filters or list()

    def produce(self, interval):
        while True:
            self._produce_once()
            time.sleep(interval)

    def _produce_once(self):
        data = self._source.emit()
        for filter_ in self._filters:
            data = filter_.filter(data)
            if data is None:
                break
        else:
            self._sender.send(data=data)

    def __repr__(self):
        repr_ = '{}(source={}, sender={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._source,
                            self._sender,
                            self._filters)
