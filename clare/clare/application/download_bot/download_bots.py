# -*- coding: utf-8 -*-

import os


class DownloadBot(object):

    def __init__(self, replay_downloader, download_validator):

        """
        Parameters
        ----------
        replay_downloader : clare.application.download_bot.interfaces.IReplayDownloader
        download_validator : clare.application.download_bot.interfaces.DownloadValidator
        """

        self._replay_downloader = replay_downloader
        self._download_validator = download_validator

    def run(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        str
            Path to the downloaded file.
        """

        self._replay_downloader.run(url=url)
        file_path = self._download_validator.run()
        return file_path

    def dispose(self):
        self._replay_downloader.dispose()

    def __repr__(self):
        repr_ = '{}(replay_downloader={}, download_validator={})'
        return repr_.format(self.__class__.__name__,
                            self._replay_downloader,
                            self._download_validator)


class UrlPathDownloadBot(object):

    def __init__(self, download_bot, root_url):

        """
        Parameters
        ----------
        download_bot : clare.application.download_bot.download_bots.DownloadBot
        root_url : str
        """

        self._download_bot = download_bot
        self._root_url = root_url

    def run(self, url):
        url = self._url_join(root_url=self._root_url, path=url)
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
