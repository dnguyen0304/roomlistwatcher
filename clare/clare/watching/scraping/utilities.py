# -*- coding: utf-8 -*-

import selenium.common
from selenium.webdriver.support import expected_conditions


def find_button(locator, wait_context):

    """
    Parameters
    ----------
    locator : tuple
        Two-element tuple. The first element is the select strategy.
        The second element is the value.
    wait_context : selenium.webdriver.support.ui.WebDriverWait

    Returns
    -------
    selenium.webdriver.remote.webelement.WebElement
        If the button could be found.
    None
        If the button could not be found.
    """

    condition = expected_conditions.element_to_be_clickable(locator=locator)
    try:
        button = wait_context.until(condition)
    except selenium.common.exceptions.TimeoutException:
        button = None
    return button
