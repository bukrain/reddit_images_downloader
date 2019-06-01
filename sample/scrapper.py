import praw
import prawcore as pwc
import datetime as dt
import urllib.request as req
import urllib.error as reqError
import os
import time
import logging

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = ROOT + "\\images\\"

def get_time(created):
    return dt.datetime.timestamp(created)

def get_content_type(info):
    for item in info.split("\n"):
        if item.startswith("Content-Type"):
            ctype = item.split(' ')[1].split('/')
            if ctype[0] == "image":
                return ctype[1]
            elif ctype == "video":
                return ctype[1]
    return "No"

def sub_exists(subreddit_name, reddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit_name, exact = True)
    except pwc.exceptions.NotFound:
        exists = False
    return exists

def get_images(subreddit_name):
    logging.basicConfig(format='%(asctime)s - %(message)s', filename="log.log", filemode='a', level=logging.INFO)

    reddit = praw.Reddit(client_id='ID',\
                        client_secret='SECRET',\
                        user_agent='AGENT',\
                        username='USERNAME',\
                        password='PASSWORD')

    if sub_exists(subreddit_name, reddit):
        subreddit = reddit.subreddit(subreddit_name)
        for sub in subreddit.display_name.split('+'):
            if not os.path.exists(IMG_DIR + sub):
                os.makedirs(IMG_DIR + sub)

        top_subreddit = subreddit.top(limit=10)

        for submission in top_subreddit:
            dir = IMG_DIR + submission.subreddit.display_name + "\\" 
            try:
                with req.urlopen(submission.url) as url:
                    try:
                        info = url.info().as_string()
                    except reqError.URLError:
                        logging.warning('Can\'t get header of {0}'.format(submission.url))
                    content_type = get_content_type(info)
                    if content_type != "No":
                        id = submission.id
                        with open(dir + id + '.' + content_type, "b+w") as f:
                            f.write(url.read())
                            logging.info('Downloaded from {0}'.format(submission.url))
                    else:
                        logging.info('Not image or video {0}'.format(submission.url))
            except reqError.URLError:
                logging.warning('Can\'t open {0}'.format(submission.url))
    else:
        logging.error("Subreddit: {0} doesn't exists".format(subreddit_name))

get_images("pics")