# -*- coding: utf-8 -*-

import abc


class Producer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def produce(self):

        """
        Emit and send data.

        Returns
        -------
        None

        Raises
        ------
        room_list_watcher.common.messaging.producing.exceptions.EmitFailed
            If the source fails to emit data.
        """

        raise NotImplementedError
