# -*- coding: utf-8 -*-

from . import consumers


class BuilderReadyStep(object):

    def __init__(self, fetcher, handler, filters=None):
        self._fetcher = fetcher
        self._handler = handler
        self._filters = filters or list()

    def with_filter(self, filter):
        self._filters.append(filter)
        builder = BuilderReadyStep(fetcher=self._fetcher,
                                   handler=self._handler,
                                   filters=self._filters)
        return builder

    def build(self):
        consumer = consumers.Consumer(fetcher=self._fetcher,
                                      handler=self._handler,
                                      filters=self._filters)
        return consumer


class BuilderHandlerStep(object):

    def __init__(self, fetcher):
        self._fetcher = fetcher

    def with_handler(self, handler):
        builder = BuilderReadyStep(fetcher=self._fetcher, handler=handler)
        return builder


class BuilderFetcherStep(object):

    def with_fetcher(self, fetcher):
        builder = BuilderHandlerStep(fetcher=fetcher)
        return builder


Builder = BuilderFetcherStep
