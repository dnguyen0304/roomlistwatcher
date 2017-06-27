# -*- coding: utf-8 -*-

import abc


class IFilter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def filter(self, record):

        """
        Parameters
        ----------
        record : clare.common.messaging.records.Record

        Returns
        -------
        clare.common.messaging.records.Record
            If the record should not be filtered.
        None
            If the record should be filtered.
        """

        pass
