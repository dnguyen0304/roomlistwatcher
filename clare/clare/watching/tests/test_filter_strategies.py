# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true

from .. import filter_strategies


def test_no_duplicate_unique_path_should_not_filter():

    seen_paths = list()
    seen_paths.append('foo')
    filter_strategy = filter_strategies.NoDuplicate(seen_paths=seen_paths)
    assert_false(filter_strategy.should_filter(path='bar'))


def test_no_duplicate_duplicate_path_should_filter():

    seen_paths = list()
    seen_paths.append('foo')
    filter_strategy = filter_strategies.NoDuplicate(seen_paths=seen_paths)
    assert_true(filter_strategy.should_filter(path='foo'))
