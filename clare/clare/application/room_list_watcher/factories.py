# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] == (2, 7):
    import Queue as queue

import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import scrapers
from clare import common


class Factory(object):

    def __init__(self, properties):

        """
        Parameters
        ----------
        properties : collections.Mapping
        """

        self._properties = properties

    def create(self):
        # Construct the scraper with validation and queuing.
        web_driver = selenium.webdriver.Chrome()
        wait_context = WebDriverWait(
            driver=web_driver,
            timeout=self._properties['scraper']['wait_context']['timeout'])
        scraper = scrapers.RoomList(web_driver=web_driver,
                                    wait_context=wait_context)
        wait_context = WebDriverWait(
            web_driver,
            timeout=self._properties['wait_context']['timeout'])
        validator = common.automation.validators.PokemonShowdown(
            wait_context=wait_context)
        scraper = scrapers.Validating(scraper=scraper, validator=validator)
        message_queue = queue.Queue()
        scraper = scrapers.QueuingDecorator(scraper=scraper,
                                            message_queue=message_queue)

        return scraper

    def __repr__(self):
        repr_ = '{}(properties={})'
        return repr_.format(self.__class__.__name__, self._properties)
