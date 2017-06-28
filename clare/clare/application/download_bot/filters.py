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

    def _process(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record

        Returns
        -------
        clare.common.messaging.records.Record
        """

        return record


class ExceptGenerationSevenMetagame(Base):

    def _should_filter(self, record):
        _, metagame_name, _ = record.value.split('-')
        if metagame_name.startswith('gen7'):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class ExceptOverusedMetagame(Base):

    def _should_filter(self, record):
        _, metagame_name, _ = record.value.split('-')
        if metagame_name.endswith('ou'):
            return False
        else:
            return True

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
