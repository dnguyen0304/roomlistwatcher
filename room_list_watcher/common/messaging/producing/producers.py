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


class Simple(Producer):

    def __init__(self, sender, source, filters=None):

        """
        Parameters
        ----------
        source : room_list_watcher.common.messaging.producing.sources.Source
        sender : room_list_watcher.common.messaging.producing.senders.Sender
        filters : typing.Iterable[room_list_watcher.common.messaging.filters.StringFilter]
            Defaults to list.
        """

        self._source = source
        self._sender = sender
        self._filters = filters or list()

    def produce(self):
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


class Blocking(Producer):

    def __init__(self, producer, interval, _sleeper=None):

        """
        Parameters
        ----------
        producer : room_list_watcher.common.messaging.producing.producers.Producer
        interval : float
        """

        self._producer = producer
        self._interval = interval
        self._sleeper = _sleeper or time.sleep

    def produce(self):
        while True:
            self._producer.produce()
            self._sleeper.sleep(self._interval)

    def __repr__(self):
        repr_ = '{}(producer={}, interval={})'
        return repr_.format(self.__class__.__name__,
                            self._producer,
                            self._interval)
