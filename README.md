# Reddit images downloader
Scrapper that downloads images or videos from given subreddit. Suports external sites: imgur, giphy, gfycat.

## Getting Started

### Prerequisites

#### Filetype
```
pip install filetype
```
#### Pywin32
```
pip install pywin32
```
#### Pillow
```
pip install Pillow
```
#### Scrapy
```
pip install scrapy
```

### Usage

To run the scrapper go to redditimagespider folder and run command
```
scrapy crawl reddit-spider
```
To change subreddit from which to download or sort type you need to change url of start_urls
```
# Downloads from gifs subreddit
start_urls = ["https://gateway.reddit.com/desktopapi/v1/subreddits/gifs?sort=new&allow_over18=1"]

# Change subreddits/gifs to subreddits/pics to download from pics subreddit
start_urls = ["https://gateway.reddit.com/desktopapi/v1/subreddits/pics?sort=new&allow_over18=1"]

# To change sort type, change sort parameter. For example to sort by hot change to sort=hot
start_urls = ["https://gateway.reddit.com/desktopapi/v1/subreddits/gifs?sort=hot&allow_over18=1"]
```
Pictures are saved in folder with the name of subreddit inside images folder. Image is named after reddit submission id sometimes there is added Imgur id.

To change where images are downloaded, change FILES_STORE inside `settings.py`
```
# Images are downloaded in folder images on c disk
FILES_STORE = 'c:\\images'
```

## Built With

* [Scrapy](https://scrapy.org/) - An open source and collaborative framework for extracting the data you need from websites.
* [Pillow](https://pillow.readthedocs.io/en/stable/index.html) - PIL fork by [Alex Clark and Contributors](https://github.com/python-pillow/Pillow/graphs/contributors)
* [Pywin32](https://github.com/mhammond/pywin32) - Python for Win32 (pywin32) extensions, which provides access to many of the Windows APIs from Python
* [Filetype](https://pypi.org/project/filetype/) - Package to infer file type and MIME type
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
