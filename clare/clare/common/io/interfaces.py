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
