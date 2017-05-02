# -*- coding: utf-8 -*-


class Attempt(object):

    def __init__(self,
                 number,
                 was_successful,
                 result,
                 exception,
                 first_attempt_start_time):

        self.number = number
        self.was_successful = was_successful
        self.result = result
        self.exception = exception
        self.first_attempt_start_time = first_attempt_start_time

    def __repr__(self):
        repr_ = ('{}('
                 'number={}, '
                 'was_successful={}, '
                 'result={}, '
                 'exception={}, '
                 'first_attempt_start_time={})')
        return repr_.format(self.__class__.__name__,
                            self.number,
                            self.was_successful,
                            self.result,
                            self.exception,
                            self.first_attempt_start_time)
