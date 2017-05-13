# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_is_instance, assert_true, raises

from .. import repositories


class TestDefault:

    def __init__(self):
        self.repository = None

    def setup(self):
        self.repository = repositories.Default()

    def test_get_return_value_is_same_entity(self):
        input_entity = expected_entity = 'foo'
        entity_id = self.repository.add(entity=input_entity)
        output_entity = self.repository.get(entity_id=entity_id)
        assert_equal(output_entity, expected_entity)

    @raises(repositories.EntityNotFound)
    def test_get_raises_entity_not_found(self):
        self.repository.get(entity_id=None)


def test_generate_entity_id_return_value_is_of_type_string():

    entity_id = repositories.Default.generate_entity_id()
    assert_is_instance(entity_id, str)


def test_generate_entity_id_return_value_is_32_characters_long():

    entity_id = repositories.Default.generate_entity_id()
    assert_true(len(entity_id) == 32)


def test_generate_entity_id_return_value_is_alphanumeric():

    entity_id = repositories.Default.generate_entity_id()
    assert_true(entity_id.isalnum())
