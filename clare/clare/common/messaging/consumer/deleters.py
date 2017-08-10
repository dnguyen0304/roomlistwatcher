# -*- coding: utf-8 -*-

import abc


class Deleter(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def delete(self, message_id, delivery_receipt):

        """
        Parameters
        ----------
        message_id : str
            Unique identifier associated with the message.
        delivery_receipt : str
            Unique identifier associated with the transaction of
            receiving this message.
        """

        raise NotImplementedError
