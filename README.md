# cron-podcast

Can download your podcasts.

## Quickstart

1. install python (Tested with Python 3.4.2 and Python 2.7.10)
2. install virtualenv (probably something like `apt-get install python-virtualenv`)
3. clone this repo
4. create a virtualenv with `virtualenv env`
5. load it `. env/bin/actiavate`
6. install dependencies `pip install -r requirements.txt`
7. your done run it `./podcatcher.py -f feedlist.conf -d /here/are/your/podcast/stored`

## Usage

```
Podcatcher 0.1.0
usage: podcatcher.py [-h] [-f FEED] [-d DOWNLOAD_DIR] [--version]

CLI podcast client.

optional arguments:
  -h, --help            show this help message and exit
  -f FEED, --feed FEED  A file where every feed url is listed.
  -d DOWNLOAD_DIR, --download-dir DOWNLOAD_DIR
                        A directory where the files are saved.
  --version             The Podcatcher version.
```

## The config (feedlist.conf)

The configuration is really simple. Just add for each podcast a new line with the feed url. 


**Example feedlist.conf**
```
http://blog.binaergewitter.de/podcast_feed/all/mp3/atom.xml
http://feeds.feedburner.com/DieWrintheit
```

My Podcastlist can be found in this gist: [fliiiix/259bc74a40c9bf56cef7d9cb9b7441b5](https://gist.github.com/fliiiix/259bc74a40c9bf56cef7d9cb9b7441b5)

## Internals

### How to keep track what's downloaded

Each item should have a guid which is saved to `$podcastname/.guid_cache` where each line represents a 
downloaded podcast. The format for it is `%Y_%m_%d %H:%M|GUID` the date is the download time.