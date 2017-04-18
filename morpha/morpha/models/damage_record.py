# -*- coding: utf-8 -*-

import re

from . import IRecord


class DamageRecord(IRecord):

    def __init__(self,
                 taken_by_position,
                 taken_by_pokemon_name,
                 remaining_hit_points,
                 total_hit_points,
                 indirectly_dealt_by):

        self.record_id = 0

        self.taken_by_position = int(taken_by_position)
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
                   '\|p(?P<taken_by_position>\d)a: (?P<taken_by_pokemon_name>[^\n\r|]+)'
                   '\|(?P<remaining_hit_points>\d+)(?:\\\/(?P<total_hit_points>\d+))?(?: [^\n\r|]+)?'
                   '(?:\|\[from\] (?P<indirectly_dealt_by>[^\n\r|]+))?')
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError('The message was not formatted correctly.')

        return record

    def __repr__(self):
        repr_ = ('{}('
                 'record_id={}, '
                 'taken_by_position={}, '
                 'taken_by_pokemon_name="{}", '
                 'remaining_hit_points={}, '
                 'total_hit_points={}, '
                 'indirectly_dealt_by="{}")')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.taken_by_position,
                            self.taken_by_pokemon_name,
                            self.remaining_hit_points,
                            self.total_hit_points,
                            self.indirectly_dealt_by)
