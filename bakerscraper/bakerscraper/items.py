# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BakerscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    notes = scrapy.Field()
    reviews = scrapy.Field()
