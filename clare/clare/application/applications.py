# -*- coding: utf-8 -*-

import time


class Default(object):

    def __init__(self, producer, consumer):
        self._producer = producer
        self._consumer = consumer

    def start(self):
        ONE_DAY_IN_SECONDS = 60 * 60 * 24

        # Start the room list watcher.
        self._producer.start()

        # Start the consumer.
        self._consumer.start()

        # Block the main thread indefinitely.
        try:
            while True:
                time.sleep(ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            pass

    def __repr__(self):
        repr_ = '{}(producer={}, consumer={})'
        return repr_.format(self.__class__.__name__,
                            self._producer,
                            self._consumer)
