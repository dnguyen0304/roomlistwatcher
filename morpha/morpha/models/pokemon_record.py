# -*- coding: utf-8 -*-

import re

from . import IRecord


class PokemonRecord(IRecord):

    def __init__(self, position, name):
        self.record_id = 0
        self.position = int(position)
        self.name = name

    @classmethod
    def from_message(cls, message):
        pattern = '\|poke\|p(?P<position>\d)\|(?P<name>[\w\s-]+)(?:, [F|M])?\|item'
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError('The message was not formatted correctly.')

        return record

    def __repr__(self):
        repr_ = '{}(record_id={}, position={}, name="{}")'
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.position,
                            self.name)
