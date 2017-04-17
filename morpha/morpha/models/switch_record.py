# -*- coding: utf-8 -*-

import re

from . import IRecord


class SwitchRecord(IRecord):

    def __init__(self,
                 player_id,
                 pokemon_name,
                 remaining_hit_points,
                 total_hit_points):

        self.record_id = 0

        self.player_id = int(player_id)
        self.pokemon_name = pokemon_name
        self.remaining_hit_points = int(remaining_hit_points)
        self.total_hit_points = int(total_hit_points)

    @classmethod
    def from_message(cls, message):
        pattern = ('\|switch'
                   '\|p(?P<player_id>\d)a: [^\n\r|]+'
                   '\|(?P<pokemon_name>[^\n\r,]+)(?:, [^\n\r|]+)?'
                   '\|(?P<remaining_hit_points>\d+)\\\/(?P<total_hit_points>\d+)')
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError('The message was not formatted correctly.')

        return record

    def __repr__(self):
        repr_ = ('{}('
                 'record_id={}, '
                 'player_id={}, '
                 'pokemon_name="{}", '
                 'remaining_hit_points={}, '
                 'total_hit_points={})')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.player_id,
                            self.pokemon_name,
                            self.remaining_hit_points,
                            self.total_hit_points)
