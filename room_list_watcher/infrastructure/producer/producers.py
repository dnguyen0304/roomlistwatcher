# -*- coding: utf-8 -*-

from room_list_watcher.common import messaging
from room_list_watcher.common import utility


class Orchestrating(messaging.producer.producers.Producer):

    def __init__(self, producer, logger):

        """
        Extend to include error handling and logging.

        Parameters
        ----------
        producer : room_list_watcher.common.messaging.producer.producers.Blocking
        logger : logging.Logger
        """

        self._producer = producer
        self._logger = logger

    def produce(self):
        try:
            self._producer.produce()
        except Exception as e:
            message = utility.format_exception(e=e)
            self._logger.exception(msg=message)

    def __repr__(self):
        repr_ = '{}(producer={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._producer,
                            self._logger)
