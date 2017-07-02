# -*- coding: utf-8 -*-

from clare import common


class OrchestratingConsumer(object):

    def __init__(self, consumer, logger):

        """
        Parameters
        ----------
        consumer : clare.application.download_bot.consumers.OrchestratingConsumer
        logger : logging.Logger
        """

        self._consumer = consumer
        self._logger = logger

    def start(self):
        try:
            self._consumer.start()
        except Exception as e:
            message = common.logging.utilities.format_exception(e=e)
            self._logger.exception(msg=message)

    def __repr__(self):
        repr_ = '{}(consumer={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._consumer,
                            self._logger)
