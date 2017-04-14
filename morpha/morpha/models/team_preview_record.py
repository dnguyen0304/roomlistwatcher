# -*- coding: utf-8 -*-


class TeamPreviewRecord(object):

    def __init__(self, player_id, pokemon_name):
        self.record_id = 0
        self.player_id = int(player_id)
        self.pokemon_name = pokemon_name

    def __repr__(self):
        repr_ = '{}(record_id={}, player_id={}, pokemon_name="{}")'
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.player_id,
                            self.pokemon_name)
