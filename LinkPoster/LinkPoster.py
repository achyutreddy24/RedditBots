import urllib.request
import time
from bs4 import BeautifulSoup
import re
import sqlite3
import praw # simple interface to the reddit API, also handles rate limiting of requests

#MAKE SURE YOU CHANGE THE USERNAME, PASSWORD, SUBREDDIT, and USERAGENT(short description, include main reddit account) to your own bots details

resp = urllib.request.urlopen("http://rudaw.net/NewsListing.aspx?pageid=528")
soup = BeautifulSoup(resp.read(), from_encoding=resp.info().get_param('charset'))
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    SUBREDDIT = Config.SUBREDDIT
    MAXPOSTS = Config.MAXPOSTS
    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
    
WAIT = 20
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.
WAITS = str(WAIT)


article_links = []
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(LINK TEXT, TITLE TEXT, PID TEXT, RLINK TEXT)')
print('Loaded SQL Database')
sql.commit()

def update_links():
    for link in soup.find_all('a', href=True):
        if re.search(REGEXLINK, link['href']):
            print(link['href'])
            article_links.append(link['href'])
    return article_links

def hour_check():
    subreddit = r.get_subreddit(SUBREDDIT)
    links = update_links()
    for link in links:
        cur.execute('SELECT * FROM posts WHERE LINK=?', [link])
        if not cur.fetchone():
            sublink = BeautifulSoup(urllib.request.urlopen(link))
            title = sublink.title.string
            make_submission(link, title)
        else:
            print("Already made that post")
            
def make_submission(link, title):
    subreddit = r.get_subreddit(SUBREDDIT)
    print('Making post...')
    try:
        newpost = r.submit(SUBREDDIT, title, url=link, captcha=None)
        print('Success: ' + newpost.short_link)
        cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?)', [link, title, newpost.id, newpost.short_link])
        sql.commit()
    except praw.requests.exceptions.HTTPError as e:
        print('ERROR: PRAW HTTP Error.', e)

while True:
    try:
        hour_check()
    except Exception as e:
        print("ERROR:", e)
    print('Sleeping ' + WAITS + ' seconds.\n')
    time.sleep(WAIT)
