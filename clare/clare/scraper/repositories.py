# -*- coding: utf-8 -*-

import random
import string

from . import interfaces


class EntityNotFound(Exception):
    pass


class Default(interfaces.IRepository):

    def __init__(self):
        self._entities = dict()

    def add(self, entity):
        entity_id = self.generate_entity_id()
        self._entities[entity_id] = entity
        return entity_id

    def get(self, entity_id):
        try:
            entity = self._entities[entity_id]
        except KeyError:
            raise EntityNotFound
        return entity

    @staticmethod
    def generate_entity_id():
        valid_characters = string.ascii_letters + string.digits
        sid = ''.join(random.SystemRandom().choice(valid_characters)
                      for _
                      in range(32))
        return sid
