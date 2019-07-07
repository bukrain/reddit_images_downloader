# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class RedditimagespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class CustomImagesPipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        meta = {'post_id': item['id'], 'subreddit_name': item['subreddit_name'],}
        return [scrapy.Request(x, meta=meta) for x in item.get('image_urls',[])]

    def file_path(self, request, response=None, info=None):
        return '{}/{}.jpg'.format(request.meta['subreddit_name'], request.meta['post_id'])