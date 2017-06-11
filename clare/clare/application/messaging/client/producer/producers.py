# -*- coding: utf-8 -*-


class Producer(object):

    def __init__(self, sender, source, filters=None):

        """
        Parameters
        ----------
        source : clare.application.messaging.client.producer.internals.interfaces.ISource
        sender : clare.application.messaging.client.producer.internals.senders.Sender
        filters : collections.Iterable
            Defaults to list.
        """

        self._source = source
        self._sender = sender
        self._filters = filters or list()

    def produce(self):
        while True:
            self.produce_once()

    def produce_once(self):
        records = self._source.emit()
        for record in records:
            for filter_ in self._filters:
                record = filter_.filter(record=record)
                if record is None:
                    break
            else:
                self._sender.push(record=record, timeout=None)

    def __repr__(self):
        repr_ = '{}(source={}, sender={}, filters={})'
        return repr_.format(self.__class__.__name__,
                            self._source,
                            self._sender,
                            self._filters)
