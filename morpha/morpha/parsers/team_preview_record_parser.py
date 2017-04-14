# -*- coding: utf-8 -*-

import re

from . import IRecordParser
from .. import models


class TeamPreviewRecordParser(IRecordParser):

    @staticmethod
    def parse(message):
        pattern = '\|poke\|p(?P<player_id>\d)\|(?P<pokemon_name>[\w\s-]+)(?:, [F|M])?\|item'
        match = re.match(pattern=pattern, string=message)

        if match:
            record = models.TeamPreviewRecord(**match.groupdict())
        else:
            raise ValueError('The message was not formatted correctly.')

        return record
