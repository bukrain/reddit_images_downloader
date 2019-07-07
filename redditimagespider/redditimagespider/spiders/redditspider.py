from redditimagespider.items import RedditimagespiderItem
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
                if data['posts'][postId]['media']['type'] != 'text':
                    title = data['posts'][postId]['title']
                    id = data['posts'][postId]['id']
                    subreddit_name = data['posts'][postId]['permalink'].split('/')[4]
                    last_id = id
                    if 'gfycat' in data['posts'][postId]['domain']:
                        meta = {'title': title, 'id': id, 'subreddit_name': subreddit_name,}
                        url = data['posts'][postId]['source']['url']
                        yield scrapy.Request(url, callback=self.parse_gfycat, meta=meta)
                    else:
                        image_url = data['posts'][postId]['media']['content']
                        yield RedditimagespiderItem(id = id, title = title, image_urls = [image_url], subreddit_name = subreddit_name)
                else:
                    pass
        if self.i < 1 :
            yield scrapy.Request(response.url + '&after={}'.format(last_id), self.parse)
        #print(response.url +'&after={}'.format(last_id))
        
        #urls = response.css('.SQnoC3ObvgnGjWt90zD9Z').xpath('@href').getall()
        #for url in urls:
            #yield scrapy.Request(response.urljoin(url), self.parse_post)
        
        
    def parse_gfycat(self, response):
        image_url = response.css('.actual-gif-image').xpath('@src').get()
        yield RedditimagespiderItem(id = response.meta['id'], title = response.meta['title'], subreddit_name = response.meta['subreddit_name'], image_urls = [image_url])

'''
    https://gateway.reddit.com/desktopapi/v1/frontpage?rtj=only&redditWebClient=web2x&app=web2x-client-production&after=t3_c9eja8&dist=9&sort=best&layout=card&useMockData=false&clickUrl=/r/memes/&allow_over18=1&include=
    https://gateway.reddit.com/desktopapi/v1/frontpage?after=t3_c9eja8&sort=best&allow_over18=1
    https://gateway.reddit.com/desktopapi/v1/subreddits/memes?rtj=only&redditWebClient=web2x&app=web2x-client-production&layout=card&allow_over18=1&include=identity
    Zwraca json z postami do zdjecia dochodzi sie data['posts']['post_id']['media']['content'] i to owinno dać link do zdjęcia
'''