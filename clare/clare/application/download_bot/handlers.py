# -*- coding: utf-8 -*-

from __future__ import print_function

from clare import common


class Download(common.messaging.client.consumer.internals.interfaces.IHandler):

    def __init__(self, download_bot):

        """
        Parameters
        ----------
        download_bot : clare.application.download_bot.download_bots.DownloadBot
        """

        self._download_bot = download_bot

    def handle(self, record):
        url = record.value
        file_path = self._download_bot.run(url=url)
        return file_path

    def __repr__(self):
        repr_ = '{}(download_bot={})'
        return repr_.format(self.__class__.__name__, self._download_bot)


class Printing(common.messaging.client.consumer.internals.interfaces.IHandler):

    def __init__(self, handler):

        """
        Parameters
        ----------
        handler : clare.application.download_bot.handlers.Download
        """

        self._handler = handler

    def handle(self, record):
        file_path = self._handler.handle(record=record)
        print(file_path)

    def __repr__(self):
        repr_ = '{}(handler={})'
        return repr_.format(self.__class__.__name__, self._handler)
