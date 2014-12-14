from bs4 import BeautifulSoup
import urllib.request
import re

#Import Settings from Config.py
try:
    import Config
    REGEXLINK = Config.REGEXLINK
    YOUTUBEVIDEOSPAGE = Config.YOUTUBEVIDEOSPAGE
except ImportError:
    print("Error Importing Config.py")

 
def CheckIfUploaded(videoTitle):
    resp = urllib.request.urlopen(YOUTUBEVIDEOSPAGE)
    soup = BeautifulSoup(resp.read(), from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if re.search(REGEXLINK, link['href']):
            if link.string == videoTitle:
                return link['href']
            else:
                pass
        else:
            pass