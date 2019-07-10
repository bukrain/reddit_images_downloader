from redditimagespider.items import RedditImageFileItem
import scrapy
import json

class RedditSpider(scrapy.Spider):
    name = 'reddit-images-spider'
    start_urls = ["https://gateway.reddit.com/desktopapi/v1/subreddits/gifs?sort=hot&allow_over18=1"]
    i = 0
    def parse(self, response):
        self.i += 1
        data = json.loads(response.text)
        last_id=''
        for postId in data['posts']:
            if not data['posts'][postId]['media'] is None:
                media_type = data['posts'][postId]['media']['type']
                if media_type != 'text':
                    title = data['posts'][postId]['title']
                    id = data['posts'][postId]['id']
                    subreddit_name = data['posts'][postId]['permalink'].split('/')[4]
                    last_id = id
                    meta = {'title': title, 'id': id, 'subreddit_name': subreddit_name, 'type': media_type}
                    if 'gfycat' in data['posts'][postId]['domain']:
                        url = data['posts'][postId]['source']['url']
                        if not 'thumbs.gfycat' in url:
                            yield scrapy.Request(url, callback=self.parse_gfycat, meta=meta)
                        else:
                            yield RedditImageFileItem(id = id, title = title, file_urls = [url], subreddit_name = subreddit_name, media_type=media_type) 
                    elif 'giphy' in data['posts'][postId]['domain']:
                        url = data['posts'][postId]['source']['url']
                        slash_indices = [i for i, a in enumerate(url) if a == '/']
                        url = url.replace(url[slash_indices[4]:], '/giphy.webp')
                        url = url.replace(url[slash_indices[1]:slash_indices[2]], '/i.giphy.com')
                        yield RedditImageFileItem(id = id, title = title, file_urls = [url], subreddit_name = subreddit_name, media_type=media_type)
                    elif 'imgur' in data['posts'][postId]['domain']:
                        url = data['posts'][postId]['source']['url']
                        yield scrapy.Request(url, callback=self.parse_imgur, meta=meta)
                    else:
                        image_url = data['posts'][postId]['media']['content']
                        if 'gif' in media_type or 'video' in media_type:
                            #TODO
                            pass
                        else:
                            yield RedditImageFileItem(id = id, title = title, file_urls = [image_url], subreddit_name = subreddit_name, media_type=media_type)
                else:
                    pass
        if self.i < 1 :
            yield scrapy.Request(response.url + '&after={}'.format(last_id), self.parse)
        
    def parse_gfycat(self, response):
        image_url = response.css('.actual-gif-image').xpath('@src').get()
        yield RedditImageFileItem(id = response.meta['id'], title = response.meta['title'], subreddit_name = response.meta['subreddit_name'], file_urls = [image_url], media_type=response.meta['type'])

    def parse_imgur(self, response):
        image_url = response.url
        if 'gif' in response.url:
            content_type = response.headers['Content-Type'].decode('utf-8')
            
            if 'image' not in content_type and 'video' not in content_type:
                src = response.css('.video-elements').xpath('source/@src')
                image_url = 'https:' + src.get()
        yield RedditImageFileItem(id = response.meta['id'], title = response.meta['title'], subreddit_name = response.meta['subreddit_name'], file_urls = [image_url], media_type=response.meta['type']) 
