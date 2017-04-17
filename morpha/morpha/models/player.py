# -*- coding: utf-8 -*-


class Player(object):

    def __init__(self, name):
        self.name = name
        self.pokemon = list()

    def __repr__(self):
        repr_ = '{}(name="{}")'
        return repr_.format(self.__class__.__name__, self.name)
