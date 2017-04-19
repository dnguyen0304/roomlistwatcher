# -*- coding: utf-8 -*-

import re

from . import IRecord


class DamageRecord(IRecord):

    def __init__(self, remaining_hit_points, indirectly_dealt_by=''):

        self.record_id = 0

        self.remaining_hit_points = int(remaining_hit_points)
        self.indirectly_dealt_by = indirectly_dealt_by or ''

    @classmethod
    def from_message(cls, message):
        pattern = ('\|-damage'
                   '\|p\da: [^\n\r|]+'
                   '\|(?P<remaining_hit_points>\d+)(?:\\\/\d+)?(?: [^\n\r|]+)?'
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
                 'remaining_hit_points={}, '
                 'indirectly_dealt_by="{}")')
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.remaining_hit_points,
                            self.indirectly_dealt_by)
