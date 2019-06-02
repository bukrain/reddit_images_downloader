# Project Title

Python class that downloads images from subreddit. Supports images from imgur and reddit for now.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Praw
```
pip install praw
```
Program is using reddit api and imgur api. To use it you must [register reddit application](https://www.reddit.com/prefs/apps/) and to download images from imgur you should register imgur application. Credentials that you will get from registering you must put in data.json file in data folder.

### Usage

To download images from subreddit simply use get_images function.

```
image_downloader = ImageDownloader()
image_downloader.get_images("name of subreddit")
```

By default only top 10 subreddit submissions are checked. To change this you need to change belowe line to something else.

```
# Gets first 10 top submissions of subreddit
submissions = subreddit.top(limit=10)

# Gets first 20 submissions in hot of subreddit
submissions = subreddit.hot(limit=20)
```
Get first 10 top pictures in **pics** subreddit.
```
image_downloader = ImageDownloader()
image_downloader.get_images("pics")
```

Pictures are saved in folder with the name of subreddit inside images folder. Image is named after reddit submission id plus imgur id if downloaded from imgur.

## Built With

* [Praw](https://praw.readthedocs.io/en/latest/) - The Python Reddit API Wrapper
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
