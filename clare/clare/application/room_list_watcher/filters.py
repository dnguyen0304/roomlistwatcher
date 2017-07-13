# -*- coding: utf-8 -*-

import abc

from clare.common import messaging


class Base(messaging.interfaces.IFilter):

    def filter(self, message):
        if not self._should_filter(message=message):
            self._process(message=message)
            return message

    @abc.abstractmethod
    def _should_filter(self, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message

        Returns
        -------
        bool
            True if the message should be filtered.
        """

        pass

    @abc.abstractmethod
    def _process(self, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message

        Returns
        -------
        clare.common.messaging.models.Message
        """

        pass


class NoDuplicateBody(Base):

    def __init__(self, flush_strategy):

        """
        Processing, if applicable, is applied in-place. Flushing, if
        applicable, occurs last.

        Parameters
        ----------
        flush_strategy : clare.application.room_list_watcher.interfaces.IFlushStrategy
            Strategy for deciding if the collection of seen messages
            should be flushed.
        """

        self._flush_strategy = flush_strategy
        self._seen = set()

    def filter(self, message):
        message = super(NoDuplicateBody, self).filter(message=message)
        if self._flush_strategy.should_flush(collection=self._seen):
            self._seen = set()
        return message

    def _should_filter(self, message):
        if message.body in self._seen:
            should_filter = True
        else:
            self._seen.add(message.body)
            should_filter = False
        return should_filter

    def _process(self, message):
        return message

    def __repr__(self):
        repr_ = '{}(flush_strategy={})'
        return repr_.format(self.__class__.__name__, self._flush_strategy)
