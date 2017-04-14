# -*- coding: utf-8 -*-

import abc


class IRecordParser(object):

    __metaclass__ = abc.ABCMeta

    # Using the staticmethod and abc.abstractmethod decorators
    # together is not supported until Python 3.3.
    @abc.abstractmethod
    def parse(message):
        pass
