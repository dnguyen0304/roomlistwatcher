# -*- coding: utf-8 -*-

import mock
from nose.tools import assert_equals

from .. import marshallers


def test_selenium_web_element_to_string():

    expected = '/battle-gen0foo-0'
    outer_html = """
<a href=\"""" + expected + """\" class="ilink">
  <small style="float:right">(rated: {rating})</small>
  <small>[[{generation}] {metagame}]</small>
  <br>
  <em class="p1">{player_1}</em> <small class="vs">vs.</small> <em class="p2">{player_2}</em>
</a>
"""
    element = mock.Mock()
    element.get_attribute = mock.Mock(return_value=outer_html.strip())

    output = marshallers.SeleniumWebElementToString().marshall(element)
    element.get_attribute.assert_called_with('outerHTML')
    assert_equals(output, expected)
