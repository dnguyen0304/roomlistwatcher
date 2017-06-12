# -*- coding: utf-8 -*-

from . import events


class Logged(object):

    def __init__(self, sender, logger):

        """
        Wrap the push behavior with logging functionality.

        Parameters
        ----------
        sender : clare.application.messaging.client.producer.internals.senders.Sender
        logger : logging.Logger
        """

        self._sender = sender
        self._logger = logger

    def push(self, record, timeout):

        """
        Parameters
        ----------
        record : clare.application.messaging.client.records.Record
        timeout : float
        """

        self._sender.push(record=record, timeout=timeout)

        message = events.RoomCreated(room_path=record.value).to_json()
        self._logger.info(msg=message)

    def __repr__(self):
        repr_ = '{}(sender={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._sender,
                            self._logger)
