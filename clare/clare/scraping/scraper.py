# -*- coding: utf-8 -*-

import collections
import functools
import json
import os

from . import Topic, exceptions
from clare import common


class Scraper(object):

    def __init__(self,
                 directory_path,
                 strategy,
                 retry_policy,
                 confirm_retry_policy,
                 logger):

        """
        Parameters
        ----------
        directory_path : str
            Path to the directory where files will be downloaded.
        strategy : clare.scraping.download_strategies.Base
        retry_policy : clare.common.retry.policy.Policy
            Retry policy when downloading.
        confirm_retry_policy : clare.common.retry.policy.Policy
            Retry policy when confirming the download.
        logger : logging.Logger
        """

        self._directory_path = directory_path
        self._strategy = strategy
        self._retry_policy = retry_policy
        self._confirm_retry_policy = confirm_retry_policy
        self._logger = logger

    def scrape(self, url):

        """
        Parameters
        ----------
        url : str

        Returns
        -------
        str
            Path to the downloaded page.
        """

        file_path = ''

        download = functools.partial(self._strategy.download, url=url)

        try:
            self._retry_policy.execute(download)
        except (exceptions.DownloadFailed, common.retry.exceptions.MaximumRetry) as e:
            message = format_exception(e=e)
            self._logger.debug(msg=message)
        else:
            confirm_download = functools.partial(
                find_newest_file,
                directory_path=self._directory_path)
            try:
                file_path = self._confirm_retry_policy.execute(confirm_download)
            except common.retry.exceptions.MaximumRetry as e:
                message = format_exception(e=e)
                self._logger.debug(msg=message)
            else:
                self._log_scrape(url=url)

        return file_path

    def _log_scrape(self, url):
        arguments = collections.OrderedDict()
        arguments['url'] = url
        event = common.logging.Event(topic=Topic.PAGE_SCRAPED,
                                     arguments=arguments)
        self._logger.info(msg=event.to_json())

    def dispose(self):
        self._strategy.dispose()

    def __repr__(self):
        repr_ = ('{}('
                 'directory_path, '
                 'strategy, '
                 'retry_policy, '
                 'confirm_retry_policy, '
                 'logger={})')
        return repr_.format(self.__class__.__name__,
                            self._directory_path,
                            self._strategy,
                            self._retry_policy,
                            self._confirm_retry_policy,
                            self._logger)


def find_newest_file(directory_path):

    """
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


def format_exception(e):

    data = collections.OrderedDict()
    data['exception_type'] = type(e).__module__ + '.' + e.__class__.__name__
    data['exception_message'] = e.message

    return json.dumps(data)
