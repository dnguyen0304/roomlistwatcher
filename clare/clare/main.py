#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from clare.application import factories


def get_configuration():

    configuration_file_path = os.environ['CLARE_CONFIGURATION_FILE_PATH']

    with open(configuration_file_path, 'rb') as file:
        parsed_configuration = json.loads(file.read())

    return parsed_configuration


def main():

    configuration = get_configuration()
    factory = factories.Factory(properties=configuration)
    application = factory.create()
    application.start()


if __name__ == '__main__':
    main()
