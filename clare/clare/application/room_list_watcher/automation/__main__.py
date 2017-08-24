# -*- coding: utf-8 -*-

from clare.application.room_list_watcher.automation import factories
from clare.main import get_configuration

if __name__ == '__main__':
    properties = get_configuration()['room_list_watcher']['scraper']
    scraper = factories.Scraper(properties=properties).create()
    scraper.scrape(url=properties['url'])
