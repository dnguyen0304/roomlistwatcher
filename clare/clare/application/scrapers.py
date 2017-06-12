# -*- coding: utf-8 -*-

import clare.common
from . import scraping


class Marshalled(object):

    def __init__(self, scraper, record_factory):

        """
        Wrap the scrape behavior to return a sequence of marshalled
        records instead.

        Parameters
        ----------
        scraper : clare.watching.scraping.interfaces.IDisposable and
                  clare.watching.scraping.interfaces.IScraper
        record_factory : clare.application.factories.Record
        """

        self._scraper = scraper
        self._record_factory = record_factory

    def scrape(self, url):

        """
        Returns
        -------
        collections.Iterable
        """

        elements = self._scraper.scrape(url=url)
        records = list()
        for element in elements:
            html = element.get_attribute('outerHTML')
            record = self._record_factory.create_from_html(html)
            records.append(record)
        return records

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={}, record_factory={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._record_factory)


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
