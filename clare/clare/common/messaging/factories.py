# -*- coding: utf-8 -*-

import datetime

from . import models
from . import records


class Message(object):

    def __init__(self, message_type=models.Message):

        """
        Parameters
        ----------
        message_type : Type[clare.common.messaging.models.Message]
            Defaults to Type[clare.common.messaging.models.Message].
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


class RecordFactory(object):

    def __init__(self, time_zone):

        """
        Parameters
        ----------
        time_zone : datetime.tzinfo
        """

        self._time_zone = time_zone

    def create(self, value=None):

        """
        Parameters
        ----------
        value : typing.Any
        """

        timestamp = datetime.datetime.utcnow().replace(tzinfo=self._time_zone)
        record = records.Record(timestamp=timestamp, value=value)
        return record

    def __repr__(self):
        repr_ = '{}(time_zone={})'
        return repr_.format(self.__class__.__name__, self._time_zone)
