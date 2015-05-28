# coding: utf-8

import requests
import xml.etree.ElementTree as XML

# force encoding to utf8
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

class Podcast(object):
    def __init__(self):
        self.version = "0.0.1"
        self.feeds = []
    
    def parse_feed_list(self):
        filename="./feedlist.conf"

        with open(filename, "r") as ins:
            array = []
            for line in ins:
                line = line.rstrip('\n').rstrip('\r')
                print(line)
                self.parse_feed(line)
                array.append(line)
            self.feeds = array

    def parse_feed(self, feed):
        ua = "curl-podcatcher/%s" % (self.version)
        headers = {'user-agent': ua, 'Accept': 'text/xml'}

        r = requests.get(feed, headers=headers)
        if r.status_code == requests.codes.ok:
            #data = r.text.decode("ascii", errors='ignore')
            xroot = XML.fromstring(r.text)
            for item in xroot.iter('item'):
                enc = item.find('enclosure')
                print(enc.attrib)
                print(item.find('guid').text)

if __name__ == "__main__":
    p = Podcast()
    print("Podcatcher %s" % (p.version))
    p.parse_feed_list()
