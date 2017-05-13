# -*- coding: utf-8 -*-

import random
import string
import sys

if sys.version_info[:2] == (2, 7):
    range = xrange

from . import interfaces


class EntityNotFound(Exception):
    pass


def random_alphanumeric_strings(length):

    valid_characters = string.ascii_letters + string.digits
    while True:
        sid = ''.join(random.SystemRandom().choice(valid_characters)
                      for _
                      in range(length))
        yield sid


class Default(interfaces.IRepository):

    def __init__(self, generate_id_strategy):

        """
        Parameters
        ----------
        generate_id_strategy : collections.Iterable
        """

        self._generate_id_strategy = generate_id_strategy
        self._entities = dict()

    def add(self, entity):
        entity_id = next(self._generate_id_strategy)
        self._entities[entity_id] = entity
        return entity_id

    def get(self, entity_id):
        try:
            entity = self._entities[entity_id]
        except KeyError:
            raise EntityNotFound
        return entity

    def __repr__(self):
        repr_ = '{}(generate_id_strategy={})'
        return repr_.format(self.__class__.__name__,
                            self._generate_id_strategy)
