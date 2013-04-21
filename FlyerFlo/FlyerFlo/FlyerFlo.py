#
# Reddit Header Image Retriever 1.0
# Author: Thomas Lordello
# Descrition: Downloads the alien icon from any given subreddit
# Usage: Simply input the URL of the subreddit whose alien header image you
# wish to download; then, specify the path of the file.
#

import sys #Used to exit program in case error occurs
import urllib.request #library needed for http request
import html.parser #library used for parsing HTML
import urllib.error #Used to detect potential HTTP errors



#helper functions used in html parsing
foundImage = False      #Creating a flag for keeping track of image finding

def findImagesAndDownload(tag, attrs):  #The alien icon is found in an "img" tag and with the attributes "id = header-img". This function scans the HTML code for these key words.
 global foundImage
 if tag == 'img' and not foundImage:
    for attr in attrs:
        if attr[0] == 'id' and attr[1] == 'header-img':
            for atr in attrs:       #Once we've found the right tag, we search that tag for the source URL.
                if atr[0] == 'src':
                    try:
                        image = urllib.request.urlopen(atr[1]).read()   #These three lines access the image's URL and save it to the specified path.
                        imagefile = open(store, 'wb')                   #
                        imagefile.write(image)                          #
                        foundImage = True   #Report that the image was found
                    except Exception as ex:
                        print("Found image but failed to retrieve it or save it to the specified path. Error was: ", ex)
                    break   #Now we break from the nested "for" loop.
            else:
                continue    #This line is executed if the nested loop ended on its own (i.e.  no image
                            #was found)
            break       #This line is executed if the nested for loop was terminated (i.e.  we
                        #found the image).


#inputs
subredditurl = input("Subreddit URL: ")
store = input("File path: ")

#access the website:
try:     
    #I had to change the User-Agent because Reddit denies access to default user agents such as "Python/urllib". See https://github.com/reddit/reddit/wiki/API                                                                                                                   
    httprequest = urllib.request.Request(subredditurl, headers = { 'User-Agent' : 'Reddit header image retriever 1.0' }) 
    httpresponse = urllib.request.urlopen(httprequest)
    htmlstr = httpresponse.read().decode('utf-8')
except urllib.error.HTTPError as httpex:
    print("HTTP Error. Error code was: ", httpex.code)
    sys.exit(0)
except Exception as ex:
    print("Failed to retrieve subreddit html page. Error was: ", ex)
    sys.exit(0)

#Find the image file:
p = html.parser.HTMLParser()        #Creates the parser
p.handle_starttag = findImagesAndDownload       #Setting a custom handler for start tags and star end tags (defined
                                                #above)
p.handle_startendtag = findImagesAndDownload    #
p.feed(htmlstr) #Will call the helper method defined above for each start and start end tag.


#Check if the search was successful:
if foundImage:
    print("Successfully retrieved image")
else:
    print("Did not find an image")

