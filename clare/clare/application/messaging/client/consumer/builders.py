# -*- coding: utf-8 -*-

from . import consumers


class BuilderReadyStep(object):

    def __init__(self, fetcher, handlers, filters=None):
        self._fetcher = fetcher
        self._handlers = handlers
        self._filters = filters or list()

    def with_handler(self, handler):
        self._handlers.append(handler)
        builder = BuilderReadyStep(fetcher=self._fetcher,
                                   handlers=self._handlers,
                                   filters=self._filters)
        return builder

    def with_filter(self, filter):
        self._filters.append(filter)
        builder = BuilderReadyStep(fetcher=self._fetcher,
                                   handlers=self._handlers,
                                   filters=self._filters)
        return builder

    def build(self):
        consumer = consumers.Consumer(fetcher=self._fetcher,
                                      handlers=self._handlers,
                                      filters=self._filters)
        return consumer


class BuilderHandlerStep(object):

    def __init__(self, fetcher):
        self._fetcher = fetcher
        self._handlers = list()

    def with_handler(self, handler):
        self._handlers.append(handler)
        builder = BuilderReadyStep(fetcher=self._fetcher,
                                   handlers=self._handlers)
        return builder


class BuilderFetcherStep(object):

    def with_fetcher(self, fetcher):
        builder = BuilderHandlerStep(fetcher=fetcher)
        return builder


Builder = BuilderFetcherStep
