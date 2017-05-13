# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from .. import documents


class TestDocument(object):

    def __init__(self):
        self.document = None

    def setup(self):
        string = """
<head>
  <div class="foo">Foo</div>
  <div class="bar">Bar</div>
</head>"""
        self.document = documents.LXmlDocument.from_string(string)

    def test_find_by_css_selector(self):
        css_selector = '.foo'
        elements = self.document.find_by_css_selector(css_selector)
        assert_equal(len(elements), 1)
        assert_equal(elements[0].attrib['class'], 'foo')

    def test_find_by_class_name(self):
        class_name = 'foo'
        elements = self.document.find_by_class_name(class_name)
        assert_equal(len(elements), 1)
        assert_equal(elements[0].attrib['class'], 'foo')
