# -*- coding: utf-8 -*-

import logging

from nose.tools import assert_in

import morpha


def test_package_logger_exists():

    assert_in('morpha', logging.Logger.manager.loggerDict)
