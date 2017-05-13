# -*- coding: utf-8 -*-

import types

from nose.tools import assert_equal, assert_is_instance, assert_true, raises

from .. import repositories


def test_random_alphanumeric_strings_is_generator():

    length = None
    output = repositories.random_alphanumeric_strings(length=length)
    assert_is_instance(output, types.GeneratorType)


def test_random_alphanumeric_strings_return_value_is_of_type_string():

    length = 0
    id = next(repositories.random_alphanumeric_strings(length=length))
    assert_is_instance(id, str)


def test_random_alphanumeric_strings_return_value_has_correct_length():

    length = 1
    id = next(repositories.random_alphanumeric_strings(length=length))
    assert_equal(len(id), length)


def test_random_alphanumeric_strings_return_value_is_alphanumeric():

    length = 1
    id = next(repositories.random_alphanumeric_strings(length=length))
    assert_true(id.isalnum())


class TestDefault:

    def __init__(self):
        self.repository = None

    def setup(self):
        length = 32
        generate_id_strategy = repositories.random_alphanumeric_strings(
            length=length)
        self.repository = repositories.Default(
            generate_id_strategy=generate_id_strategy)

    def test_get_return_value_is_same_entity(self):
        input_entity = expected_entity = 'foo'
        entity_id = self.repository.add(entity=input_entity)
        output_entity = self.repository.get(entity_id=entity_id)
        assert_equal(output_entity, expected_entity)

    @raises(repositories.EntityNotFound)
    def test_get_raises_entity_not_found(self):
        self.repository.get(entity_id=None)
