# coding: utf-8

import os
import requests
import slugify
import xml.etree.ElementTree as XML

# force encoding to utf8
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

class Podcast(object):
    def __init__(self):
        self.version = "0.0.1"
        self.feeds = []
        self.base_folder = ''
    
    def create_directory(self):
        p = os.path.abspath(self.base_folder)
        self.base_path = p

        # create dir if needed
        if not os.path.exists(p):
            os.makedirs(p)
            print("The directory %s was created." % (p))

    def parse_feed_list(self):
        filename="./feedlist.conf"

        with open(filename, "r") as configfile:
            array = []
            for idx, line in enumerate(configfile):
                line = line.rstrip('\n').rstrip('\r')
                if idx == 0:
                    self.base_folder = line
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
                guidfile.seek(0)
                first_char = guidfile.read(1)

                if first_char:
                    guidfile.seek(0)
                    guids = f.read().splitlines()
        else:
            open(p, 'a').close()

        return guids

        
    def parse_feed(self, feed):
        ua = "curl-podcatcher/%s" % (self.version)
        headers = {'user-agent': ua, 'Accept': 'text/xml'}

        r = requests.get(feed, headers=headers)
        if r.status_code == requests.codes.ok:
            xroot = XML.fromstring(r.text)
            
            # build podcast dir or reade list with
            # already downloaded podcasts
            title = xroot.find('channel/title')
            self.build_podcast(title.text)

            for item in xroot.iter('item'):
                enc = item.find('enclosure')
                print(enc.attrib)
                print(item.find('guid').text)

if __name__ == "__main__":
    p = Podcast()
    print("Podcatcher %s" % (p.version))
    p.parse_feed_list()
    p.create_directory()
