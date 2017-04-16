# -*- coding: utf-8 -*-

import re

from . import IRecord


class PlayerRecord(IRecord):

    def __init__(self, player_id, name):

        self.record_id = 0

        self.player_id = int(player_id)
        self.name = name

    @classmethod
    def from_message(cls, message):
        pattern = '\|player\|p(?P<player_id>\d)\|(?P<name>.+)\|.+'
        match = re.match(pattern=pattern, string=message)

        if match:
            record = cls(**match.groupdict())
        else:
            raise ValueError

        return record

    def __repr__(self):
        repr_ = '{}(record_id={}, player_id={}, name="{}")'
        return repr_.format(self.__class__.__name__,
                            self.record_id,
                            self.player_id,
                            self.name)
