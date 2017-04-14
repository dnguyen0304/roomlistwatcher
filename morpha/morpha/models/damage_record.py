# -*- coding: utf-8 -*-

import re

from . import IRecord


class DamageRecord(IRecord):

    def __init__(self,
                 dealt_by_player_id,
                 dealt_by_pokemon_name,
                 taken_by_player_id,
                 taken_by_pokemon_name,
                 remaining_hit_points,
                 total_hit_points,
                 indirectly_dealt_by):

        self.record_id = 0

        if dealt_by_player_id is None and taken_by_player_id:
            if taken_by_player_id == '1':
                self.dealt_by_player_id = 2
            elif taken_by_player_id == '2':
                self.dealt_by_player_id = 1
        else:
            self.dealt_by_player_id = int(dealt_by_player_id)
        self.dealt_by_pokemon_name = dealt_by_pokemon_name or ''
        self.taken_by_player_id = int(taken_by_player_id)
        self.taken_by_pokemon_name = taken_by_pokemon_name
        self.remaining_hit_points = int(remaining_hit_points)
        try:
            self.total_hit_points = int(total_hit_points)
        except TypeError:
            self.total_hit_points = 0
        self.indirectly_dealt_by = indirectly_dealt_by or ''

    @classmethod
    def from_message(cls, message):
        pattern = ('\|-damage'
                   '\|p(?P<taken_by_player_id>\d)a: (?P<taken_by_pokemon_name>[\w\s-]+)'
                   '\|(?P<remaining_hit_points>\d+)(?:\\\/(?P<total_hit_points>\d+))?(?: \w+)?'
                   '(?:\|\[from\] (?P<indirectly_dealt_by>[\w\s]+))?')
        match = re.match(pattern=pattern, string=message)

        if match:
            # Unpacking multiple arguments is not supported until
            # Python 3.5.
            arguments = dict()
            arguments.update(match.groupdict())
            arguments.update({
                'dealt_by_player_id': None,
                'dealt_by_pokemon_name': None
            })
            record = cls(**arguments)
        else:
            raise ValueError('The message was not formatted correctly.')

        return record

    def __repr__(self):
        repr_ = ('{}('
                 'record_id={}, '
                 'dealt_by_player_id={}, '
                 'dealt_by_pokemon_name="{}", '
                 'taken_by_player_id={}, '
                 'taken_by_pokemon_name="{}", '
                 'remaining_hit_points={}, '
                 'total_hit_points={}, '
                 'indirectly_dealt_by="{}")')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.dealt_by_player_id,
                            self.dealt_by_pokemon_name,
                            self.taken_by_player_id,
                            self.taken_by_pokemon_name,
                            self.remaining_hit_points,
                            self.total_hit_points,
                            self.indirectly_dealt_by)
