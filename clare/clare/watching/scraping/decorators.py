# -*- coding: utf-8 -*-

from . import interfaces


class SerializedElements(interfaces.IDisposable):

    def __init__(self, scraper):

        """
        Change the scrape behavior to return a sequence of serialized
        elements instead.

        Parameters
        ----------
        scraper : clare.watching.scraping.interfaces.IDisposable and
                  clare.watching.scraping.interfaces.IScraper
        """

        self._scraper = scraper

    def scrape(self, url):
        elements = self._scraper.scrape(url=url)
        serialized_elements = [element.get_attribute('outerHTML')
                               for element
                               in elements]
        return serialized_elements

    def dispose(self):
        self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self.__class__.__name__, self._scraper)
