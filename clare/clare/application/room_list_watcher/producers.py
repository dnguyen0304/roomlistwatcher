# -*- coding: utf-8 -*-

from clare import common


class OrchestratingProducer(object):

    def __init__(self, producer, logger):

        """
        Parameters
        ----------
        producer : clare.common.messaging.producer.producers.Producer
        logger : logging.Logger
        """

        self._producer = producer
        self._logger = logger

    def produce(self, interval):
        try:
            self._producer.produce(interval=interval)
        except Exception as e:
            message = common.logging.utilities.format_exception(e=e)
            self._logger.exception(msg=message)

    def __repr__(self):
        repr_ = '{}(producer={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._producer,
                            self._logger)
