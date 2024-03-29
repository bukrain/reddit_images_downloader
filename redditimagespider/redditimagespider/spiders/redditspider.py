from redditimagespider.items import RedditImageFileItem
import scrapy
import json

class RedditSpider(scrapy.Spider):
    name = 'reddit-spider'
    start_urls = ["https://gateway.reddit.com/desktopapi/v1/subreddits/gifs?sort=new&allow_over18=1"]
    page_limit = 10
    i = 0
    
    def parse(self, response):
        self.i += 1
        data = json.loads(response.text)
        last_id=''
        for postId in data['posts']:
            if data['posts'][postId]['media'] is not None:
                media_type = data['posts'][postId]['media']['type']
                if media_type != 'text':
                    title = data['posts'][postId]['title']
                    id = data['posts'][postId]['id']
                    subreddit_name = data['posts'][postId]['permalink'].split('/')[4]
                    meta = {'title': title, 'id': id, 'subreddit_name': subreddit_name, 'type': media_type}
                    if 'gfycat' in data['posts'][postId]['domain']:
                        url = data['posts'][postId]['source']['url']
                        if 'thumbs.gfycat' in url:
                            yield RedditImageFileItem(id = id, title = title, file_urls = [url],
                                                      subreddit_name = subreddit_name, media_type=media_type)
                        else:
                            yield scrapy.Request(url, callback=self.parse_gfycat, meta=meta)
                    elif 'giphy' in data['posts'][postId]['domain']:
                        url = data['posts'][postId]['source']['url']
                        slash_indices = [i for i, a in enumerate(url) if a == '/']
                        url = url.replace(url[slash_indices[4]:], '/giphy.webp')
                        url = url.replace(url[slash_indices[1]:slash_indices[2]], '/i.giphy.com')
                        yield RedditImageFileItem(id = id, title = title, file_urls = [url], 
                                                  subreddit_name = subreddit_name, media_type=media_type)
                    elif 'imgur' in data['posts'][postId]['domain']:
                        url = data['posts'][postId]['source']['url']
                        yield scrapy.Request(url, callback=self.parse_imgur, meta=meta)
                    else:
                        image_url = data['posts'][postId]['media']['content']
                        yield RedditImageFileItem(id = id, title = title, file_urls = [image_url],
                                                  subreddit_name = subreddit_name, media_type=media_type)
        if self.i < self.page_limit :
            last_id = data['postIds'][-1]
            url = response.url
            if 'after' in response.url:
                url = response.url[:response.url.rfind('&')]
            yield scrapy.Request(url + '&after={}'.format(last_id), self.parse)
        
    def parse_gfycat(self, response):
        image_url = response.css('.actual-gif-image').xpath('@src').get()
        yield RedditImageFileItem(id = response.meta['id'], title = response.meta['title'],
                                  subreddit_name = response.meta['subreddit_name'], 
                                  file_urls = [image_url], media_type=response.meta['type'])

    def parse_imgur(self, response):
        image_urls = {}
        id = response.meta['id']
        title = response.meta['title']
        subreddit_name = response.meta['subreddit_name']
        media_type = response.meta['type']
        if media_type == 'embed':
            image_containers = response.css('.post-image-container')
            
            for image_container in image_containers:
                name = id + '_{}'.format(image_container.xpath('@id').get())
                id = image_container.xpath('@id').get()
                image_type = image_container.xpath('@itemtype').get()
                ext = 'jpg'
                if 'VideoObject' in image_type or 'MusicVideoObject' in image_type or 'Clip' in image_type:
                    ext = 'gifv'
                image_urls[name] = 'https://i.imgur.com/{}.{}'.format(id, ext)
        else:
            image_urls[id] = response.url

        for image_id, image_url in image_urls.items():
            if 'gif' in image_url:
                content_type = response.headers['Content-Type'].decode('utf-8')
                if 'image' not in content_type and 'video' not in content_type:
                    src = response.css('.video-elements').xpath('source/@src')
                    if src.get() is not None:
                        image_url = 'https:' + src.get()
            yield RedditImageFileItem(id = image_id, title = title,
                                    subreddit_name = subreddit_name,
                                    file_urls = [image_url], media_type = media_type) 

