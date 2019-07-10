# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RedditImageFileItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    subreddit_name = scrapy.Field()
    media_type = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()