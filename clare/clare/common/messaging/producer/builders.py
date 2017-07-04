# -*- coding: utf-8 -*-

from . import producers


class BuilderReadyStep(object):

    def __init__(self, source, sender, filters=None):
        self._source = source
        self._sender = sender
        self._filters = filters or list()

    def with_filter(self, filter):
        self._filters.append(filter)
        builder = BuilderReadyStep(source=self._source,
                                   sender=self._sender,
                                   filters=self._filters)
        return builder

    def build(self):
        producer = producers.Producer(source=self._source,
                                      sender=self._sender,
                                      filters=self._filters)
        return producer


class BuilderSenderStep(object):

    def __init__(self, source):
        self._source = source

    def with_sender(self, sender):
        builder = BuilderReadyStep(source=self._source, sender=sender)
        return builder


class BuilderSourceStep(object):

    def with_source(self, source):
        builder = BuilderSenderStep(source=source)
        return builder


Builder = BuilderSourceStep
