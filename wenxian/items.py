# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WenxianItem(scrapy.Item):
    file_urls = scrapy.Field()
    name = scrapy.Field()
    files = scrapy.Field()

