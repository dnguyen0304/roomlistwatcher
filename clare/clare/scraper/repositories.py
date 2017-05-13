# -*- coding: utf-8 -*-

import os
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


class Filesystem(interfaces.IRepository):

    def __init__(self, root_directory_path, generate_id_strategy):

        """
        Parameters
        ----------
        root_directory_path : str
        generate_id_strategy : collections.Iterable
        """

        self._root_directory_path = root_directory_path
        self._generate_id_strategy = generate_id_strategy

    def add(self, entity):
        entity_id = next(self._generate_id_strategy)
        file_path = os.path.join(self._root_directory_path, entity_id)
        with open(file_path, mode='wb') as file:
            file.write(entity)
        return entity_id

    def get(self, entity_id):
        file_path = os.path.join(self._root_directory_path, entity_id)
        with open(file_path, mode='rb') as file:
            entity = file.read()
        return entity

    def __repr__(self):
        repr_ = '{}(root_directory_path="{}", generate_id_strategy={})'
        return repr_.format(self.__class__.__name__,
                            self._root_directory_path,
                            self._generate_id_strategy)
