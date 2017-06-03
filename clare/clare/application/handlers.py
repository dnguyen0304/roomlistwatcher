# -*- coding: utf-8 -*-

from __future__ import print_function

from .messaging.client.consumer import interfaces


class Print(interfaces.IHandler):

    def handle(self, record):
        print(record)
