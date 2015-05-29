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
                guids = guidfile.read().splitlines()
        else:
            open(p, 'a').close()

        return (p, guids)

        
    def parse_feed(self, feed):
        ua = "curl-podcatcher/%s" % (self.version)
        headers = {'user-agent': ua, 'Accept': 'text/xml'}

        r = requests.get(feed, headers=headers)
        if r.status_code == requests.codes.ok:
            xroot = XML.fromstring(r.text)
            
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

        filename = url.split("?")[0].split("/")[-1] # fuck yeah
        file_path = os.path.join(p, filename)

        r = requests.get(url, stream=True)
        with open(file_path, 'wb') as f:
           for chunk in r.iter_content(chunk_size=1024): 
              if chunk: # filter out keep-alive new chunks
                 f.write(chunk)
                 f.flush()
        
        # log guid
        with open(path, "a") as f:
            f.write("%s\n" % (guid))
        
        print("Finished the download of %s" %(file_path))


if __name__ == "__main__":
    p = Podcast()
    print("Podcatcher %s" % (p.version))
    p.parse_feed_list()
    p.create_directory()


