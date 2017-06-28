# -*- coding: utf-8 -*-

import abc

from clare.common import messaging


class Base(messaging.interfaces.IFilter):

    def filter(self, record):
        if not self._should_filter(record=record):
            self._process(record=record)
            return record

    @abc.abstractmethod
    def _should_filter(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record

        Returns
        -------
        bool
            True if the record should be filtered.
        """

        pass

    @abc.abstractmethod
    def _process(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record

        Returns
        -------
        clare.common.messaging.records.Record
        """

        pass


class NoDuplicate(Base):

    def __init__(self, flush_strategy):

        """
        Processing, if applicable, is applied in-place. Flushing, if
        applicable, occurs last.

        Parameters
        ----------
        flush_strategy : clare.application.room_list_watcher.interfaces.IFlushStrategy
            Strategy for deciding if the collection of seen values
            should be flushed.
        """

        self._flush_strategy = flush_strategy
        self._seen = set()

    def filter(self, record):
        record = super(NoDuplicate, self).filter(record=record)
        if self._flush_strategy.should_flush(collection=self._seen):
            self._seen = set()
        return record

    def _should_filter(self, record):
        if record.value in self._seen:
            should_filter = True
        else:
            self._seen.add(record.value)
            should_filter = False
        return should_filter

    def _process(self, record):
        return record

    def __repr__(self):
        repr_ = '{}(flush_strategy={})'
        return repr_.format(self.__class__.__name__, self._flush_strategy)
