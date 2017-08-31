# -*- coding: utf-8 -*-

import abc


class Sender(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, data):

        """
        Parameters
        ----------
        data : str

        Returns
        -------
        None

        Raises
        ------
        room_list_watcher.common.messaging.producing.exceptions.SendTimeout
            If the sender times out.
        """

        raise NotImplementedError
