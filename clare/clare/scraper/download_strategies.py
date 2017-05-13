# -*- coding: utf-8 -*-

from . import interfaces


class SerializableDecorator(interfaces.IRepository):

    def __init__(self, repository, serializable):

        """
        Parameters
        ----------
        repository : clare.scraper.interfaces.IRepository
        serializable : clare.scraper.interfaces.ISerializable
        """

        self._repository = repository
        self._serializable = serializable

    def add(self, entity):

        """
        Parameters
        ----------
        entity : clare.scraper.interfaces.ISerializable
        """

        entity_id = self._repository.add(entity=entity.to_string())
        return entity_id

    def get(self, entity_id):
        data = self._repository.get(entity_id=entity_id)
        deserialized = self._serializable.from_string(data)
        return deserialized

    def __repr__(self):
        repr_ = '{}(repository={}, serializable={})'
        return repr_.format(self.__class__.__name__,
                            self._repository,
                            self._serializable)
