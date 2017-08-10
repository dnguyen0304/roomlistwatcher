# -*- coding: utf-8 -*-

from clare.common.messaging import consumer


class Nop(consumer.deleters):

    def delete(self, message):
        pass
