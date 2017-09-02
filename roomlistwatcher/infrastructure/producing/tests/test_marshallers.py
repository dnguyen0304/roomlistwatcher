# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equals, raises

from .. import marshallers


class TestSeleniumWebElementToString(object):

    def __init__(self):
        self.element = None

    def setup(self):
        self.element = mock.Mock()

    def test_valid_input_returns_room_path(self):
        expected = '/battle-gen0foo-0'
        outer_html = """
<a href=\"""" + expected + """\" class="ilink">
  <small style="float:right">(rated: {rating})</small>
  <small>[[{generation}] {metagame}]</small>
  <br>
  <em class="p1">{player_1}</em> <small class="vs">vs.</small> <em class="p2">{player_2}</em>
</a>
"""
        self.element.get_attribute = mock.Mock(return_value=outer_html.strip())

        output = marshallers.SeleniumWebElementToString().marshall(
            self.element)
        self.element.get_attribute.assert_called_with('outerHTML')
        assert_equals(output, expected)

    @raises(ValueError)
    def test_invalid_input_raises_value_error(self):
        self.element.get_attribute = mock.Mock(return_value='foo')
        marshallers.SeleniumWebElementToString().marshall(self.element)
