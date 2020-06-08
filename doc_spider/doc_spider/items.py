# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#clean_text = Compose(MapCompose(lambda v: v.strip("\n").strip("\t").strip("\u201c").strip("\u2019").strip("")), Join())
#to_int = Compose(TakeFirst(), int)


class DocSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    links = scrapy.Field()
    texts = scrapy.Field()
