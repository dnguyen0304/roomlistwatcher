# -*- coding: utf-8 -*-

from clare.clare.common.messaging import exceptions


class EmitTimeout(exceptions.Timeout):
    pass


class SendTimeout(exceptions.Timeout):
    pass
