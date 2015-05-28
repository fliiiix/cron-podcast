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

    def parse_feed(self, feed):
        ua = "curl-podcatcher/%s" % (self.version)
        headers = {'user-agent': ua, 'Accept': 'text/xml'}

        r = requests.get(feed, headers=headers)
        if r.status_code == requests.codes.ok:
            xroot = XML.fromstring(r.text)
            title = xroot.find('channel/title')
            
            print(title)
            slug_title = slugify.slugify(title.text)
            print(slug_title)

            for item in xroot.iter('item'):
                enc = item.find('enclosure')
                print(enc.attrib)
                print(item.find('guid').text)

if __name__ == "__main__":
    p = Podcast()
    print("Podcatcher %s" % (p.version))
    p.parse_feed_list()
    p.create_directory()
