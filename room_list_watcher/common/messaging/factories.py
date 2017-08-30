# -*- coding: utf-8 -*-

from . import models


class Message2(object):

    _MESSAGE_TYPE = models.Message2

    def create(self):

        """
        Returns
        -------
        clare.common.messaging.models.Message2
        """

        return Message2._MESSAGE_TYPE()

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
