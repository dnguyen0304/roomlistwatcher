# -*- coding: utf-8 -*-

from __future__ import print_function

from .messaging.client import consumer


class Print(consumer.internals.interfaces.IHandler):

    def handle(self, record):
        print(record)
