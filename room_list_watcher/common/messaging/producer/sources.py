# -*- coding: utf-8 -*-

import abc


class Source(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def emit(self):

        """
        Returns
        -------
        str

        Raises
        ------
        room_list_watcher.common.messaging.producer.exceptions.EmitTimeout
            If the source times out.
        """

        raise NotImplementedError
