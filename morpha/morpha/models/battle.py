# -*- coding: utf-8 -*-


class Battle(object):

    def __init__(self):
        self.side_mapping = dict()

    def get_player(self, position):
        return self.side_mapping[position]

    def get_all_players(self):
        return self.side_mapping.values()

    def add_player(self, position, player):
        self.side_mapping[position] = player

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
