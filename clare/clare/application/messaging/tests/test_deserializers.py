# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from .. import deserializers


def test_string_deserializer_deserialize():

    deserialized = deserializers.StringDeserializer().deserialize(data='foo')
    assert_equal(deserialized, 'foo')
