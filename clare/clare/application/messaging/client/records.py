# -*- coding: utf-8 -*-


class Record(object):

    def __init__(self, queue_name, timestamp, value=None):

        """
        Parameters
        ----------
        queue_name : str
        timestamp : float
        value : typing.Any
            Defaults to None.
        """

        self.queue_name = queue_name
        self.timestamp = timestamp
        self.value = value

    def __repr__(self):
        repr_ = '{}(queue_name="{}", timestamp={}, value={})'
        return repr_.format(self.__class__.__name__,
                            self.queue_name,
                            self.timestamp,
                            self.value)
