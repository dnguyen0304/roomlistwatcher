# -*- coding: utf-8 -*-

import time

from . import interfaces


class Polling(object):

    def __init__(self, scraper, wait_time, buffer):

        """
        Change the scrape behavior to poll the web page instead.

        Parameters
        ----------
        scraper : clare.watching.scraping.interfaces.IDisposable and
                  clare.watching.scraping.interfaces.IScraper
        wait_time : float
            Wait time in seconds.
        buffer : Queue.Queue
        """

        self._scraper = scraper
        self.wait_time = wait_time
        self._buffer = buffer

    def scrape(self, url, _sleep=time.sleep):

        """
        Parameters
        ----------
        url : str
            Web page URL.
        _sleep : collections.Callable
            Used internally. Defaults to time.sleep.
        """

        while True:
            data = self._scraper.scrape(url=url)
            for item in data:
                self._buffer.put(item=item)
            _sleep(self.wait_time)

    def __repr__(self):
        repr_ = '{}(scraper={}, wait_time={}, buffer={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self.wait_time,
                            self._buffer)


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
