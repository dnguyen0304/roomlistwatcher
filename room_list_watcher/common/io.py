# -*- coding: utf-8 -*-

import abc


class Disposable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispose(self):

        """
        Garbage collect the resources.
        """

        raise NotImplementedError


class JsonSerializable(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_json(self):

        """
        Returns
        -------
        str
        """

        raise NotImplementedError
