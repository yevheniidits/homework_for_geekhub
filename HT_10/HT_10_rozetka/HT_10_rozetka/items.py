# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ht10RozetkaItem(scrapy.Item):
    product = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
