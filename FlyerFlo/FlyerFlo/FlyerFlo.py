#
# Reddit Header Image Retriever 1.0
# Author: Thomas Lordello
# Descrition:
# Usage: How to use it.
#

import sys
import urllib.request #library needed for http request
import html.parser #library used for parsing HTML
import urllib.error #Used to detect potential HTTP errors


#helper functions used in html parsing
def findImagesAndDownload(tag, attrs):
 if tag == 'img':
    for attr in attrs:
        if attr[0] == 'id' and attr[1] == 'header-img':
            for atr in attrs:
                if atr[0] == 'src':
                    try:
                        image = urllib.request.urlopen(atr[1]).read()
                        imagefile = open(store, 'wb')
                        imagefile.write(image)
                        print("Successfully retrieved image")
                    except Exception as ex:
                        print("Found image but failed to retrieve it or save it to the specified path. Error was: ", ex)

#inputs
subredditurl = "http://www.reddit.com/r/news" #input("Subreddit URL: ")
store = "T:/asdfasdf.png" #input("File path: ")

#access the website:
try:
    httprequest = urllib.request.Request(subredditurl, headers = { 'User-Agent' : 'Reddit header image retriever 1.0' }) #Note we had to change the User-Agent because Reddit denies access to default user agents such as "Python/urllib". See https://github.com/reddit/reddit/wiki/API
    httpresponse = urllib.request.urlopen(httprequest)
    htmlstr = httpresponse.read().decode('utf-8')
except urllib.error.HTTPError as httpex:
    print("HTTP Error. Error code was: ", httpex.code)
    sys.exit(0)
except Exception as ex:
    print("Failed to retrieve subreddit html page. Error was: ", ex)
    sys.exit(0)

#Find the image file:
p = html.parser.HTMLParser()
p.handle_starttag = findImagesAndDownload
p.handle_startendtag = findImagesAndDownload
p.feed(htmlstr)