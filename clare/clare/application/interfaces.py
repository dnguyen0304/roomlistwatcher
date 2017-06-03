# -*- coding: utf-8 -*-

import abc


class IFlushStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def should_flush(self, collection):

        """
        Parameters
        ----------
        collection : typing.Any

        Returns
        -------
        bool
            True if the collection should be flushed.
        """

        pass
