# -*- coding: utf-8 -*-

import re

from . import IRecord


class MoveRecord(IRecord):

    def __init__(self,
                 used_by_player_id,
                 used_by_pokemon_name,
                 move_name,
                 targeted_player_id,
                 targeted_pokemon_name):

        self.record_id = 0

        self.used_by_player_id = int(used_by_player_id)
        self.used_by_pokemon_name = used_by_pokemon_name
        self.move_name = move_name
        self.targeted_player_id = int(targeted_player_id)
        self.targeted_pokemon_name = targeted_pokemon_name

    @classmethod
    def from_message(cls, message):
        pattern = ('\|move'
                   '\|p(?P<used_by_player_id>\d)a: (?P<used_by_pokemon_name>.+)'
                   '\|(?P<move_name>.+)'
                   '\|p(?P<targeted_player_id>\d)a: (?P<targeted_pokemon_name>.+)')
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError

        return record

    def __repr__(self):
        repr_ = ('{}('
                 'record_id={}, '
                 'used_by_player_id={}, '
                 'used_by_pokemon_name="{}", '
                 'move_name="{}", '
                 'targeted_player_id={}, '
                 'targeted_pokemon_name="{}")')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.used_by_player_id,
                            self.used_by_pokemon_name,
                            self.move_name,
                            self.targeted_player_id,
                            self.targeted_pokemon_name)
