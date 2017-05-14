# -*- coding: utf-8 -*-

from nose.tools import assert_is_instance

from .. import interfaces, ObservableFactory


def test_observable_factory_build_returns_i_notifyable():

    observable_factory = ObservableFactory()
    observable = observable_factory.build()
    assert_is_instance(observable, interfaces.INotifyable)
