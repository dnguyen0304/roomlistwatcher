# -*- coding: utf-8 -*-


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
