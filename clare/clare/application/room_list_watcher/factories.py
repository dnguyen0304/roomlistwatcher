# -*- coding: utf-8 -*-

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import scrapers


class Factory(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):
        # Construct the scraper.
        web_driver = selenium.webdriver.Chrome()
        wait_context = WebDriverWait(
            driver=web_driver,
            timeout=self._properties['scraper']['wait_context']['timeout'])
        scraper = scrapers.RoomList(web_driver=web_driver,
                                    wait_context=wait_context)

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
