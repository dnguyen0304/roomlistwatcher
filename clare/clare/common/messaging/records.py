# -*- coding: utf-8 -*-


class Record(object):

    def __init__(self, timestamp, value=None):

        """
        Parameters
        ----------
        timestamp : datetime.datetime
        value : typing.Any
            Defaults to None.
        """

        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        repr_ = '{}(timestamp={}, value={})'
        return repr_.format(self.__class__.__name__,
                            repr(self.timestamp),
                            self.value)
