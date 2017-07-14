# -*- coding: utf-8 -*-

from . import models


class Message(object):

    def __init__(self, message_type=models.Message):

        """
        Parameters
        ----------
        message_type : typing.Type[clare.common.messaging.models.Message]
            Defaults to typing.Type[clare.common.messaging.models.Message].
        """

        self._message_type = message_type

    def create(self, body):

        """
        Parameters
        ----------
        body : str

        Returns
        -------
        clare.common.messaging.models.Message
        """

        message = self._message_type(body=body)
        return message

    def __repr__(self):
        repr_ = '{}(message_type={})'
        return repr_.format(self.__class__.__name__, self._message_type)
