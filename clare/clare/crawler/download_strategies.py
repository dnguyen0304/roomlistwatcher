# -*- coding: utf-8 -*-

import abc
import functools
import os


class DownloadFailed(Exception):
    pass


class IDownloadStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        str
            Path to the downloaded file.
        """

        pass

    def dispose(self):
        pass


class Fail(IDownloadStrategy):

    def execute(self, url):

        """
        Raises
        ------
        clare.crawler.download_strategies.DownloadFailed
        """

        raise DownloadFailed

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)


class Simple(IDownloadStrategy):

    def __init__(self,
                 web_driver,
                 directory_path,
                 download_retry_policy,
                 confirmation_retry_policy):

        """
        Parameters
        ----------
        web_driver : Selenium web driver
        directory_path : str
            Path to the directory where files will be downloaded.
        download_retry_policy : clare.retry.policy.Policy
            Retry policy for when the page is not yet ready to be
            downloaded.
        confirmation_retry_policy : clare.retry.policy.Policy
            Retry policy for when the page has not yet finished
            downloading.
        """

        self._web_driver = web_driver
        self._directory_path = directory_path
        self._download_retry_policy = download_retry_policy
        self._confirmation_retry_policy = confirmation_retry_policy

    def execute(self, url):
        self._web_driver.get(url=url)

        callable = functools.partial(
            self._web_driver.find_element_by_class_name,
            name='replayDownloadButton')

        element = self._download_retry_policy.execute(callable=callable)
        element.click()

        newest_file_path = self._confirmation_retry_policy.execute(
            callable=self._find_newest_file)

        return newest_file_path

    @staticmethod
    def do_find_newest_file(directory_path):

        """
        This method may be extended or overridden by subclasses.

        Parameters
        ----------
        directory_path : str

        Returns
        -------
        str
        """

        file_paths = (os.path.join(directory_path, file_name)
                      for file_name
                      in os.listdir(directory_path))
        try:
            newest_file_path = max(file_paths, key=os.path.getctime)
        except ValueError:
            newest_file_path = ''
        return newest_file_path

    def dispose(self):
        self._web_driver.quit()

    def __repr__(self):
        repr_ = ('{}('
                 'web_driver={}, '
                 'directory_path="{}", '
                 'download_retry_policy={}, '
                 'confirmation_retry_policy={})')
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._directory_path,
                            self._download_retry_policy,
                            self._confirmation_retry_policy)
