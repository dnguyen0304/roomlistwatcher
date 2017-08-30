# -*- coding: utf-8 -*-

import abc


class ISender(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, data):

        """
        Parameters
        ----------
        data : object

        Raises
        ------
        clare.common.messaging.producer.exceptions.SendTimeout
        """

        raise NotImplementedError
