# -*- coding: utf-8 -*-

import collections

from clare.common import messaging


class ScraperToBufferingSource(messaging.producer.interfaces.ISource):

    def __init__(self, scraper, url, marshall_strategy):

        """
        Parameters
        ----------
        scraper : typing.Type[clare.application.room_list_watcher.interfaces.IScraper]
        url : str
        marshall_strategy : clare.application.room_list_watcher.marshall_strategies.SeleniumWebElementToMessage
        """

        self._scraper = scraper
        self._url = url
        self._marshall_strategy = marshall_strategy

        self._buffer = collections.deque()

    def emit(self):
        # Use extend() followed by popleft() to have FIFO behavior
        # as with a queue. Using extendleft() followed by pop()
        # expectedly also accomplishes this goal.
        #
        # Iterating through the records in reverse is done because
        # the room list is scraped "backwards". In other words, the
        # newest rooms are at the head of the array and the oldest
        # ones are at its tail.
        if not self._buffer:
            elements = self._scraper.scrape(url=self._url)
            self._buffer.extend(reversed(elements))
        element = self._buffer.popleft()
        message = self._marshall_strategy.marshall(element)
        return message

    def __repr__(self):
        repr_ = '{}(scraper={}, url="{}", marshall_strategy={})'
        return repr_.format(self.__class__.__name__,
                            self._scraper,
                            self._url,
                            self._marshall_strategy)
