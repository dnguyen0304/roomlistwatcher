# -*- coding: utf-8 -*-

import abc


class IQueue(object):

    @abc.abstractmethod
    def send(self, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message

        Returns
        -------
        None
        """

        raise NotImplementedError
