# -*- coding: utf-8 -*-

from room_list_watcher import factories
from room_list_watcher.common import utility

if __name__ == '__main__':
    properties = utility.get_configuration()['scraper']
    scraper = factories.Scraper(properties=properties).create()
    scraper.scrape(url=properties['url'])
