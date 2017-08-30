# -*- coding: utf-8 -*-

from . import models


class Message(object):

    _MESSAGE_TYPE = models.Message

    def create(self):

        """
        Returns
        -------
        clare.common.messaging.models.Message
        """

        return self.__class__._MESSAGE_TYPE()

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
