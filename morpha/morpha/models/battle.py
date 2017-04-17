# -*- coding: utf-8 -*-

from . import Player, PlayerRecord, Pokemon, PokemonRecord, SwitchRecord


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

    _mapping = {
        PlayerRecord: 'handle_player_record',
        PokemonRecord: 'handle_pokemon_record',
        SwitchRecord: 'handle_switch_record'
    }

    def __init__(self):
        self.pokemon_are_loaded = False
        self._sides = list()
        self._sides_index = dict()
        self._players = list()
        self._players_index = dict()

    def apply_log_record(self, log_record):
        if len(self._players) == 2 and not isinstance(log_record, PokemonRecord):
            self.pokemon_are_loaded = True
        try:
            handler = getattr(self, self._mapping[type(log_record)])
        except KeyError:
            pass
        else:
            handler(log_record)

    def get_all_players(self):
        return self._players

    def handle_player_record(self, record):
        player = Player(name=record.name)
        side = Side(position=record.position, player=player)
        self._sides.append(side)
        self._sides_index[record.position] = side
        self._players.append(player)
        self._players_index[record.position] = player

    def handle_pokemon_record(self, record):
        pokemon = Pokemon(name=record.pokemon_name)
        player = self._players_index[record.position]
        player.pokemon.append(pokemon)

    def handle_switch_record(self, record):
        player = self._players_index[record.position]
        for pokemon in player.pokemon:
            if pokemon.name == record.pokemon_name:
                pokemon.total_hit_points = record.total_hit_points
                break

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)
