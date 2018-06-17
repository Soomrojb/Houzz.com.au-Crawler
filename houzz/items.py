# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouzzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    posttitle = scrapy.Field()
    posthref = scrapy.Field()
    location = scrapy.Field()
    contact = scrapy.Field()
    phone = scrapy.Field()
