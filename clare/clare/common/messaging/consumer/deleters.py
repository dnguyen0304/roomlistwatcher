# -*- coding: utf-8 -*-

import abc


class Deleter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def delete(self, message):

        """
        Parameters
        ----------
        message : clare.common.messaging.models.Message2

        Raises
        ------
        clare.common.messaging.consumer.exceptions.DeleteFailed
        """

        raise NotImplementedError
