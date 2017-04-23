#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, sys, time, argparse, requests, slugify
import xml.etree.ElementTree as XML


class Podcast(object):
    def __init__(self, feedlist, download_dir):
        self.version = "0.2.0"
        self.feeds = []
        self.base_folder = download_dir
        self.feedlist = feedlist

    def parse_feed_list(self):
        with open(self.feedlist, "r") as configfile:
            array = []
            for idx, line in enumerate(configfile):
                line = line.rstrip('\n').rstrip('\r')
                line = line.strip()
                if line == '':
                    continue

                if line[0] == '#':
                    continue

                self.parse_feed(line)
                array.append(line)
            self.feeds = array

    def build_podcast(self, title):
        slug_title = slugify.slugify(title)
        p = os.path.join(self.base_folder, slug_title)
    
        if not os.path.exists(p):
            os.makedirs(p)

        guids = []
        p = os.path.join(p, '.guid_cache')
        if os.path.isfile(p):
            with open(p, "r") as guidfile:
                guids = guidfile.read().splitlines()
        else:
            open(p, 'a').close()

        return (p, guids)

        
    def parse_feed(self, feed):
        ua = "curl-podcatcher/%s" % (self.version)
        headers = {'user-agent': ua, 'Accept': 'text/xml'}
        
        r = requests.get(feed, headers=headers)
        r.encoding = 'utf-8'
        parser = XML.XMLParser(encoding='utf-8')
        if r.status_code == requests.codes.ok:
            xroot = XML.fromstring(r.text.encode( "utf-8" ), parser=parser)
            
            # build podcast dir or reade list with
            # already downloaded podcasts
            title = xroot.find('channel/title')
            pod = self.build_podcast(title.text)
            (podpath, guids) = pod

            for item in xroot.iter('item'):
                enc = item.find('enclosure')
                guid = item.find('guid')

                url = enc.get('url')
                uuid = guid.text

                if uuid not in guids:
                    self.download_podcast(url, uuid, podpath)


    def download_podcast(self, url, guid, path):
        p = os.path.dirname(path) 
        print("Downloading %s to %s" % (url, p))

        r = requests.get(url, stream=True, allow_redirects=True)

        filename = r.url.split("?")[0].split("/")[-1] # fuck yeah
        file_path = os.path.join(p, filename)

        with open(file_path, 'wb') as f:
           for chunk in r.iter_content(chunk_size=1024): 
              if chunk: # filter out keep-alive new chunks
                 f.write(chunk)
                 f.flush()
        
        # log guid
        with open(path, "a") as f:
            f.write("%s%s\n" % (time.strftime("%Y_%m_%d %H:%M|"), guid))
        
        print("Finished the download of %s" %(file_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI podcast client.")
    parser.add_argument("-f", "--feed", help="A file where every feed url is listed.")
    parser.add_argument("-d", "--download-dir", help="A directory where the files are saved.")
    parser.add_argument("--version", action="store_true", help="The Podcatcher version.")
    args = parser.parse_args()

    p = Podcast(args.feed, args.download_dir)
    if args.version:
        print("Podcatcher %s" % (p.version))
        exit()

    # print help for missing arguments
    if len(sys.argv) == 1:
        print("Podcatcher %s" % (p.version))
        parser.print_help()
        sys.exit(1)

    # validate params
    valid = True
    if args.feed is None or not os.path.isfile(args.feed):
        valid = False
        print("Please provide a valid file with your feedlist! (-f/--feed FEED)")

    if args.download_dir is None or not os.path.isdir(args.download_dir):
        valid = False
        print("Please provide a valid folder to download! (-d/--download-dir DOWNLOAD_DIR)")

    if valid:
        p.parse_feed_list()
        p.create_directory() 

