# -*- coding: utf-8 -*-

import functools

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from . import exceptions
from . import interfaces
from clare import common


class ReplayDownloader(interfaces.IReplayDownloader):

    def __init__(self, web_driver, wait_context):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.Chrome
        wait_context : selenium.webdriver.support.ui.WebDriverWait
        """

        self._web_driver = web_driver
        self._wait_context = wait_context

    def run(self, url):

        """
        Raises
        ------
        clare.application.download_bot.exceptions.BattleNotCompleted
            If the battle has not yet completed.
        """

        self._initialize(url=url)
        self._do_run()

    def _initialize(self, url):
        self._web_driver.get(url=url)

    def _do_run(self):
        download_button = self._find_download_button()
        try:
            download_button.click()
        except AttributeError:
            message = 'The battle has not yet completed.'
            raise exceptions.BattleNotCompleted(message)

    def _find_download_button(self):

        """
        Returns
        -------
        selenium.webdriver.remote.webelement.WebElement
            If the battle has completed.
        None
            If the battle has not yet completed.
        """

        locator = (By.CLASS_NAME, 'replayDownloadButton')
        condition = expected_conditions.element_to_be_clickable(locator=locator)
        try:
            download_button = self._wait_context.until(condition)
        except selenium.common.exceptions.TimeoutException:
            download_button = None
        return download_button

    def dispose(self):
        self._web_driver.quit()

    def __repr__(self):
        repr_ = '{}(web_driver={}, wait_context={})'
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._wait_context)


class Validating(interfaces.IReplayDownloader):

    def __init__(self, replay_downloader, validator):

        """
        Parameters
        ----------
        replay_downloader : clare.application.download_bot.interfaces.IReplayDownloader
        validator : clare.common.automation.validators.PokemonShowdown
        """

        self._replay_downloader = replay_downloader
        self._validator = validator

    def run(self, url):
        self._replay_downloader._initialize(url=url)
        self._do_run()

    def _do_run(self):

        """
        Raises
        ------
        clare.application.download_bot.exceptions.ResourceExpired
            If the room has expired.
        common.automation.exceptions.ValidationFailed:
            If the connection with the target server was lost.
        """

        try:
            self._validator.check_room_was_entered()
        except common.automation.exceptions.ValidationFailed:
            try:
                self._validator.check_no_server_error()
            except common.automation.exceptions.ValidationFailed:
                raise
            else:
                message = 'The room has expired.'
                raise exceptions.ResourceExpired(message)
        self._replay_downloader._do_run()

    def dispose(self):
        self._replay_downloader.dispose()

    def __repr__(self):
        repr_ = '{}(replay_downloader={}, validator={})'
        return repr_.format(self.__class__.__name__,
                            self._replay_downloader,
                            self._validator)


class Retrying(interfaces.IReplayDownloader):

    def __init__(self, replay_downloader, policy):

        """
        Parameters
        ----------
        replay_downloader : clare.application.download_bot.interfaces.IReplayDownloader
        policy : clare.common.retry.policy.Policy
        """

        self._replay_downloader = replay_downloader
        self._policy = policy

    def run(self, url):
        download = functools.partial(self._replay_downloader.run, url=url)
        self._policy.execute(download)

    def dispose(self):
        self._replay_downloader.dispose()

    def __repr__(self):
        repr_ = '{}(replay_downloader={}, policy={})'
        return repr_.format(self.__class__.__name__,
                            self._replay_downloader,
                            self._policy)
