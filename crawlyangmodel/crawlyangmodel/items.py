# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrwalyangmodelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class YangModelItem(scrapy.Item):
    area = scrapy.Field()
    wg   = scrapy.Field()
    title= scrapy.Field()
    url  = scrapy.Field()
    last_update = scrapy.Field(serializer=str)

class UnavailableItem(scrapy.Item):
    url = scrapy.Field()
    
