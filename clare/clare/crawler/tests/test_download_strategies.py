# -*- coding: utf-8 -*-

from nose.tools import raises

from .. import DownloadFailed, strategies


@raises(DownloadFailed)
def test_failed():
    strategy = strategies.Failed()
    strategy.execute(url=None)
