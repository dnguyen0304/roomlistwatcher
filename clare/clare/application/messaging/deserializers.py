# -*- coding: utf-8 -*-

from . import interfaces


class StringDeserializer(interfaces.IDeserializer):

    def deserialize(self, data):
        return data
