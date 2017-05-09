# -*- coding: utf-8 -*-

from nose.tools import raises

from ..download_strategies import DownloadFailed, Fail


@raises(DownloadFailed)
def test_fail():
    strategy = Fail()
    strategy.execute(url=None)
