import praw
import prawcore as pwc
import datetime as dt
import urllib.request as req
import urllib.error as reqError
import os
import time
import logging
import requests
import json
from errors import UserLimitError, ClientLimitError


class Scrapper:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMG_DIR = ROOT + "\\images\\"
    DATA_FILE = ROOT + "\\data\\data.json"
    api_data = {}

    def __init__(self):
        if os.path.isfile(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as f:
                self.api_data = json.load(f)
        else:
            data = {
                "reddit_data":{
                    "client_id": "",
                    "client_secret": "",
                    "user_agent": "",
                    "username": "",
                    "password": ""
                },
                "imgur_data":{
                    "client_id": "",
                    "remaining_client": 12500,
                    "remaining_user": 500,
                    "client_limit": 50,
                    "user_limit": 50
                }
            }
            with open(self.DATA_FILE, "w") as f:
                json.dump(data,f)

    def get_time(self, created):
        return dt.datetime.timestamp(created)

    def get_content_type(self, info):
        for item in info.split("\n"):
            if item.startswith("Content-Type"):
                ctype = item.split(' ')[1].split('/')
                if ctype[0] == "image":
                    print(ctype[1])
                    return ctype[1]
                elif ctype[0] == "video":
                    return ctype[1]
        return "No"

    def sub_exists(self, subreddit_name, reddit):
        exists = True
        try:
            reddit.subreddits.search_by_name(subreddit_name, exact = True)
        except pwc.exceptions.NotFound:
            exists = False
        return exists

    def get_imgur_image_url(self, url):
        id_image = url.split('/')[3]
        api_url = 'https://api.imgur.com/3/image/'+ id_image
        headers = {
            'Authorization': 'Client-ID '+self.api_data["imgur_data"]["client_id"]
        }
        response = requests.request('GET', api_url, headers = headers, allow_redirects=False)
        if 'X-RateLimit-ClientRemaining' in response.headers.keys():
            self.api_data["imgur_data"]["remaining_client"] = int(response.headers['X-RateLimit-ClientRemaining'])
        if 'X-RateLimit-UserRemaining' in response.headers.keys():
            self.api_data["imgur_data"]["remaining_user"] = int(response.headers['X-RateLimit-UserRemaining'])
        with open(self.DATA_FILE,"w") as f:
            json.dump(self.api_data,f)
        return response.json()["data"]["link"]

    def get_images(self, subreddit_name):
        logging.basicConfig(format='%(asctime)s - %(message)s', filename="log.log", filemode='a', level=logging.INFO)

        reddit = praw.Reddit(client_id=self.api_data["reddit_data"]["client_id"],\
                            client_secret=self.api_data["reddit_data"]["client_secret"],\
                            user_agent=self.api_data["reddit_data"]["user_agent"],\
                            username=self.api_data["reddit_data"]["username"],\
                            password=self.api_data["reddit_data"]["password"])
        if self.sub_exists(subreddit_name, reddit):
            subreddit = reddit.subreddit(subreddit_name)
            for sub in subreddit.display_name.split('+'):
                if not os.path.exists(self.IMG_DIR + sub):
                    os.makedirs(self.IMG_DIR + sub)

            top_subreddit = subreddit.top(limit=10)

            for submission in top_subreddit:
                url_of_image = submission.url
                self.download_image(url_of_image, submission.subreddit.display_name, submission.id)
        else:
            logging.error("Subreddit: {0} doesn't exists".format(subreddit_name))


    def download_image(self, url_of_image, name_of_subreddit, id_of_submission):
        url_to_open = url_of_image
        try:
            if "//imgur" in url_to_open:
                if self.api_data["imgur_data"]["remaining_user"] <= self.api_data["imgur_data"]["user_limit"]:
                    raise UserLimitError('Too many requests per hour')
                if self.api_data["imgur_data"]["remaining_client"] <= self.api_data["imgur_data"]["client_limit"]:
                    raise ClientLimitError('Too many request per day')
                url_to_open = self.get_imgur_image_url(url_to_open)
            dir = self.IMG_DIR + name_of_subreddit + "\\" 

            if url_to_open.endswith(".gifv"):
                url_to_open = url_to_open[0:len(url_to_open) - 4] + 'mp4'

            with req.urlopen(url_to_open) as url:
                try:
                    info = url.info().as_string()
                except reqError.URLError:
                    logging.warning('Can\'t get header of {0}'.format(url_to_open))
                content_type = self.get_content_type(info)
                if content_type != "No":
                    id = id_of_submission
                    with open(dir + id + '.' + content_type, "b+w") as f:
                        f.write(url.read())
                        logging.info('Image: {0} downloaded from {1}'.format(id, url_to_open))
                else:
                    logging.info('Not image or video {0}'.format(url_to_open))
        except reqError.URLError:
            logging.warning('Can\'t open {0}'.format(url_to_open))
        except UserLimitError:
            logging.warning('You have made too many requests to imgur per hour {0}'.format(url_to_open))
        except ClientLimitError:
            logging.warning('You have made too many requests to imgur per day {0}'.format(url_to_open))


sc = Scrapper()
sc.get_images("GifRecipes")