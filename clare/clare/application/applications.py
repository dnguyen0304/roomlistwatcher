# -*- coding: utf-8 -*-

import time

from clare import common


class Application(object):

    def __init__(self, room_list_watcher, download_bot):
        self._room_list_watcher = room_list_watcher
        self._download_bot = download_bot

    def start(self):
        ONE_DAY_IN_SECONDS = 60 * 60 * 24

        self._room_list_watcher.start()
        self._download_bot.start()

        # Block the main thread indefinitely.
        try:
            while True:
                time.sleep(ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            pass

    def __repr__(self):
        repr_ = '{}(room_list_watcher={}, download_bot={})'
        return repr_.format(self.__class__.__name__,
                            self._room_list_watcher,
                            self._download_bot)


class OrchestratingApplication(object):

    def __init__(self, application, logger):

        """
        Parameters
        ----------
        application : clare.application.applications.Application
        logger : logging.Logger
        """

        self._application = application
        self._logger = logger

    def start(self):
        try:
            self._application.start()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            message = common.logging.utilities.format_exception(e=e)
            self._logger.exception(msg=message)

    def __repr__(self):
        repr_ = '{}(application={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._application,
                            self._logger)
