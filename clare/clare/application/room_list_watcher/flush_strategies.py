# -*- coding: utf-8 -*-

from . import interfaces


class AfterDuration(interfaces.IFlushStrategy):

    def __init__(self, maximum_duration, timer_factory):

        """
        Parameters
        ----------
        maximum_duration : float
            Maximum duration in seconds since the epoch.
        timer_factory : clare.common.utilities.timer_factories.CountdownTimerFactory
        """

        self._maximum_duration = maximum_duration
        self._timer_factory = timer_factory

        self._timer = None

    def should_flush(self, collection):

        """
        Parameters
        ----------
        collection : typing.Any

        Returns
        -------
        bool
            True if the collection should be flushed.
        """

        if not self._timer:
            timer = self._timer_factory.create(duration=self._maximum_duration)
            self._timer = timer

        # Do not use the not operator in the following line. Tests
        # often set dummy start time values of 0.0 seconds.
        if self._timer.start_time is None:
            self._timer.start()
            should_flush = False
        else:
            should_flush = self._timer.should_stop()

        if should_flush:
            self._timer = None

        return should_flush

    def __repr__(self):
        repr_ = '{}(maximum_duration={}, timer_factory={})'
        return repr_.format(self.__class__.__name__,
                            self._maximum_duration,
                            self._timer_factory)


class AfterSize(interfaces.IFlushStrategy):

    def __init__(self, maximum_size):

        """
        Parameters
        ----------
        maximum_size : int
        """

        self._maximum_size = maximum_size

    def should_flush(self, collection):

        """
        Parameters
        ----------
        collection : collections.Sized

        Returns
        -------
        bool
            True if the collection should be flushed.
        """

        if len(collection) >= self._maximum_size:
            should_flush = True
        else:
            should_flush = False
        return should_flush

    def __repr__(self):
        repr_ = '{}(maximum_size={})'
        return repr_.format(self.__class__.__name__, self._maximum_size)
