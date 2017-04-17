# -*- coding: utf-8 -*-


class Side(object):

    def __init__(self, position, player):
        self.position = position
        self.player = player

    def __repr__(self):
        repr_ = '{}(position={}, player={})'
        return repr_.format(self.__class__.__name__,
                            self.position,
                            self.player)


class Battle(object):

    def __init__(self):
        self._side_index = dict()

    def add_player(self, position, player):
        side = Side(position=position, player=player)
        self._side_index[position] = side

    def get_player(self, position):
        return self._side_index[position].player

    def get_all_players(self):
        players = [side.player for side in self._side_index.values()]
        return players

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
