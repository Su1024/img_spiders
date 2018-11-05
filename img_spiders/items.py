# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    cdn_path = scrapy.Field()
    ctime = scrapy.Field()
    info1 = scrapy.Field()
    info2 = scrapy.Field()
    view_num = scrapy.Field()
    tags = scrapy.Field()
    link = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    size = scrapy.Field()
    formats = scrapy.Field()
    plate_type = scrapy.Field()
    hs = scrapy.Field()


class SheJiDiGuo(scrapy.Item):
    link = scrapy.Field()
