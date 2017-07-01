# -*- coding: utf-8 -*-

import os


class RunPathAdapter(object):

    def __init__(self, download_bot, root_url):

        """
        Parameters
        ----------
        download_bot : clare.application.download_bot.download_bots.DownloadBot
        root_url : str
        """

        self._download_bot = download_bot
        self._root_url = root_url

    def run(self, path):
        url = self._url_join(root_url=self._root_url, path=path)
        self._download_bot.run(url=url)

    @staticmethod
    def _url_join(root_url, path):
        url = os.path.join(root_url, path.lstrip('/'))
        return url

    def __repr__(self):
        repr_ = '{}(download_bog={}, root_url={})'
        return repr_.format(self.__class__.__name__,
                            self._download_bot,
                            self._root_url)
