# -*- coding: utf-8 -*-

import datetime

from clare.common import messaging


class RecordFactory(object):

    _record_class = messaging.records.Record

    def __init__(self, time_zone):

        """
        Parameters
        ----------
        time_zone : datetime.tzinfo
        """

        self._time_zone = time_zone

    def create(self, value=None):
        timestamp = datetime.datetime.utcnow().replace(tzinfo=self._time_zone)
        record = messaging.records.Record(timestamp=timestamp, value=value)
        return record

    def __repr__(self):
        repr_ = '{}(time_zone={})'
        return repr_.format(self.__class__.__name__, self._time_zone)
