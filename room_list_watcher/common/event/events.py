# -*- coding: utf-8 -*-

import abc


class IEvent(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def INTERFACE_VERSION(self):
        pass
