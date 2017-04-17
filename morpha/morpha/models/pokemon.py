# -*- coding: utf-8 -*-


class Pokemon(object):

    def __init__(self, name):
        self.name = name
        self.remaining_hit_points = 0
        self.total_hit_points = 0

    def __repr__(self):
        repr_ = '{}(name="{}")'
        return repr_.format(self.__class__.__name__, self.name)
