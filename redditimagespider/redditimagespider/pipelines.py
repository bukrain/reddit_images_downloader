# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import filetype
import os
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.misc import md5sum
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

class RedditimagespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class CustomFilesPipline(FilesPipeline):
    def get_media_requests(self, item, info):
        meta = {'post_id': item['id'], 'subreddit_name': item['subreddit_name'], 'type': item['media_type']}
        return [scrapy.Request(x, meta=meta) for x in item.get('file_urls',[])]

    def file_path(self, request, response=None, info=None):
        return '{}/{}'.format(request.meta['subreddit_name'], request.meta['post_id'])

    def file_downloaded(self, response, request, info):
        buf = BytesIO(response.body)
        ext = filetype.guess(buf)
        extension = ''
        if ext is None:
            extension = os.path.splitext(request.url)[1]
        else:
            extension = ext.extension
        checksum = md5sum(buf)
        buf.seek(0)
        path = self.file_path(request, response=response, info=info) + '.{}'.format(extension)
        self.store.persist_file(path, buf, info)
        return checksum