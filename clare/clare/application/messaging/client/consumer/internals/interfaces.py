# -*- coding: utf-8 -*-

import abc


class IHandler(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, record):

        """
        Parameters
        ----------
        record : clare.application.messaging.client.records.Record
        """

        pass
