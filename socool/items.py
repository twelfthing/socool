# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MFWItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    name = scrapy.Field()
    level = scrapy.Field()
    tags = scrapy.Field()
    attention = scrapy.Field()
    groups = scrapy.Field()

    dynamic = scrapy.Field()
    download = scrapy.Field()
    note = scrapy.Field()
    path = scrapy.Field()
    review = scrapy.Field()
    together = scrapy.Field()

