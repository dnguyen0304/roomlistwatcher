# -*- coding: utf-8 -*-

from clare.clare.common.messaging import models


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
