# -*- coding: utf-8 -*-


class Record(object):

    def __init__(self, queue_name, timestamp, key=None, value=None):

        """
        Parameters
        ----------
        queue_name : str
        timestamp : float
        key : typing.Any
            Defaults to None.
        value : typing.Any
            Defaults to None.
        """

        self.queue_name = queue_name
        self.timestamp = timestamp
        self.key = key
        self.value = value

    def __repr__(self):
        repr_ = '{}(queue_name="{}", timestamp={}, key={}, value={})'
        return repr_.format(self.__class__.__name__,
                            self.queue_name,
                            self.timestamp,
                            self.key,
                            self.value)
