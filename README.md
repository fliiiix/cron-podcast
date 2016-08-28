# cron-podcast

Can download your podcasts.

## Quickstart

1. install python (I just tested python 2.7 shame on me)
2. install virtualenv (probably something like `apt-get install python-virtualenv`)
3. clone this repo
4. create a virtualenv with `virtualenv env`
5. load it `. env/bin/actiavate`
6. install dependencies `pip install -r requirements.txt`
7. your done run it with python podcatcher.py
8. (maybe edit the podcast list in `feedlist.conf`, but hey I have good taste so you can just take my list)

## The config (feedlist.conf)

The configuration is really simple. Just add for each podcast a new line with the feed url. 
Except for the first line, here you define the download directory which can be an absolute or a relative path 
on your filesystem.


**Example feedlist.conf**
```
./podcasts
http://blog.binaergewitter.de/podcast_feed/all/mp3/atom.xml
http://feeds.feedburner.com/DieWrintheit
```
