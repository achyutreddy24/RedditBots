import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
from imgurpython import ImgurClient

import make_picture as mp

#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    SUBREDDIT = Config.SUBREDDIT
    MAXPOSTS = Config.MAXPOSTS
    REPLYMESSAGE = Config.REPLYMESSAGE
    
    ID = Config.ID
    SECRET = Config.SECRET
    
    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
    
WAIT = 5

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

img = ImgurClient(ID, SECRET)

sql = sqlite3.connect('sqlSummon.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, CLink TEXT, CLinkParent TEXT, ILink TEXT)')
print('Loaded SQL Database')
sql.commit()

def occurances(str, chars):
    count = 0
    for char in chars:
        count = count + str.count(char)
    return count
    
def upload_imgur(filename):
    return img.upload_from_path(filename, anon=True)

def scan():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    comments = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        cid = comment.id
        cauthor = comment.author.name
        cfullBody = comment.body
        cbody = comment.body.lower()
        Clink = comment.permalink

        print("CO is "+str(CO)+" cbody len is "+str(clength)+" per is "+str(p))
        if p<PERCENTAGE:
            cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
            if not cur.fetchone():
                print("Found an ascii comment")
                f = open('CurrentAscii.txt', 'w', encoding='utf-8')
                f.write(cfullBody)
                f.close()
                
                mp.make_jpg('CurrentAscii', 'CurrentJPG')
                ILink = upload_imgur('CurrentJPG.jpg')['link']
                print(ILink)
            
                print('Replying to ' + cid + ' by ' + cauthor)
                comment.reply(REPLYMESSAGE.format(ILink))
                
                cur.execute('INSERT INTO posts VALUES(?, ?, ?)', [cid, Clink, ILink])
                sql.commit()
        else:
            pass
                
    
while True:
    try:
        scan()
    except Exception as e:
        print("ERR", e)
    print('Sleeping ' + str(WAIT))
    time.sleep(WAIT)