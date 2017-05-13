# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import documents, repositories, download_strategies


class TestSerializableDecorator(object):

    def __init__(self):
        self.document = None
        self.repository = None

    def setup(self):
        string = """
<head>
  <div class="foo">Foo</div>
  <div class="bar">Bar</div>
</head>"""

        length = 32
        generate_id_strategy = repositories.random_alphanumeric_strings(
            length=length)
        repository = repositories.Default(
            generate_id_strategy=generate_id_strategy)

        self.document = documents.LXmlDocument.from_string(string)
        self.repository = download_strategies.SerializableDecorator(
            repository=repository,
            serializable=documents.LXmlDocument)

    def test_get_return_value_is_same_entity(self):
        input_entity = expected_entity = self.document
        entity_id = self.repository.add(entity=input_entity)
        output_entity = self.repository.get(entity_id=entity_id)
        assert_equal(output_entity.to_string(), expected_entity.to_string())

    @raises(repositories.EntityNotFound)
    def test_get_raises_entity_not_found(self):
        self.repository.get(entity_id=None)
