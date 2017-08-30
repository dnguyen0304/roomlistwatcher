# -*- coding: utf-8 -*-

import json
import os

_ENVIRONMENT_VARIABLE_NAME = 'ROOM_LIST_WATCHER_CONFIGURATION_FILE_PATH'


def get_configuration():

    """
    Read the application configuration.
    """

    configuration_file_path = os.environ[_ENVIRONMENT_VARIABLE_NAME]

    with open(configuration_file_path, 'rb') as file:
        parsed_configuration = json.loads(file.read())

    return parsed_configuration
