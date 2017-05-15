# -*- coding: utf-8 -*-

import abc


class IJsonSerializable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_json(self):

        """
        Returns
        -------
        str
        """

        pass


class IEvent(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def INTERFACE_VERSION(self):
        pass
