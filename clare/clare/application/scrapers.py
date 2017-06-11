# -*- coding: utf-8 -*-

import clare.common
from . import scraping


class Orchestration(object):

    def __init__(self, scraper, logger):

        """
        Wrap the scrape behavior with exception handling and logging
        functionality.

        Parameters
        ----------
        scraper : clare.watching.scraping.interfaces.IDisposable and
                  clare.watching.scraping.interfaces.IScraper
        logger : logging.Logger
        """

        self._scraper = scraper
        self._logger = logger

    def scrape(self, url):

        """
        Parameters
        ----------
        url : str
            Web page URL.
        """

        while True:
            try:
                self._scraper.scrape(url=url)
            except scraping.exceptions.ExtractFailed as e:
                message = clare.common.logging.utilities.format_exception(e=e)
                self._logger.debug(msg=message)

    def __repr__(self):
        repr_ = '{}(scraper={}, logger={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._logger)
