# -*- coding: utf-8 -*-

import abc


class IDeserializer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def deserialize(self, data):

        """
        Parameters
        ----------
        data : bytes

        Returns
        -------
        typing.Any
        """

        pass
