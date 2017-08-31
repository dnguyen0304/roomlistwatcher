# -*- coding: utf-8 -*-

import re

from nose.tools import assert_equal, assert_is_not_none

from .. import generators


class TestIncrementingFilePath(object):

    def setup(self):
        self.template = '[\w/]+{qualifier_delimiter}(?P<counter>\d)\.\w+'

        self.directory_path = '/home/foo/'
        self.file_name = 'bar'
        self.file_extension = '.foobar'
        self.qualifier_delimiter = '-'

        self.generator = generators.IncrementingFilePath(
            directory_path=self.directory_path,
            file_name=self.file_name,
            file_extension=self.file_extension)

    def test_qualifier_delimiter(self):
        qualifier_delimiter = '_'
        pattern = self.template.format(qualifier_delimiter=qualifier_delimiter)
        generator = generators.IncrementingFilePath(
            directory_path=self.directory_path,
            file_name=self.file_name,
            file_extension=self.file_extension,
            qualifier_delimiter=qualifier_delimiter)
        file_path = generator.generate()
        assert_is_not_none(re.match(pattern, file_path))

    def counter_is_appended(self):
        pattern = self.template.format(
            qualifier_delimiter=self.qualifier_delimiter)
        file_path = self.generator.generate()
        assert_is_not_none(re.match(pattern, file_path))

    def counter_is_incremented(self):
        pattern = self.template.format(
            qualifier_delimiter=self.qualifier_delimiter)
        match = re.match(pattern=pattern, string=self.generator.generate())
        before = int(match.groupdict()['counter'])
        match = re.match(pattern=pattern, string=self.generator.generate())
        after = int(match.groupdict()['counter'])
        assert_equal(before, after - 1)

    def test_from_file_path(self):
        expected = self.generator.generate()
        file_path = ''.join((self.directory_path,
                             self.file_name,
                             self.file_extension))
        generator = generators.IncrementingFilePath.from_file_path(file_path)
        output = generator.generate()
        assert_equal(expected, output)
