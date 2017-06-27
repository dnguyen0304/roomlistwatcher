# -*- coding: utf-8 -*-

import datetime

from clare.common.messaging.client import records


class RecordFactory(object):

    _record_class = records.Record

    def __init__(self, queue_name, time_zone):

        """
        Parameters
        ----------
        queue_name : str
        time_zone : datetime.tzinfo
        """

        self._queue_name = queue_name
        self._time_zone = time_zone

    def create(self, value=None):
        timestamp = datetime.datetime.utcnow().replace(tzinfo=self._time_zone)
        record = records.Record(queue_name=self._queue_name,
                                timestamp=timestamp,
                                value=value)
        return record

    def __repr__(self):
        repr_ = '{}(queue_name="{}", time_zone={})'
        return repr_.format(self.__class__.__name__,
                            self._queue_name,
                            self._time_zone)
