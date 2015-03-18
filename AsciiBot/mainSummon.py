import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
import html
from imgurpython import ImgurClient

import make_picture as mp

SUMMONTEXT = """+/u/ascii-text-bot"""

#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
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
    comments = r.get_mentions(limit=MAXPOSTS)
    for comment in comments:
        
        cbody = comment.body.lower()
        Clink = comment.permalink
        cid = comment.id
        
        if comment.is_root:
            print("Comment is root, ignoring")
            continue
        if SUMMONTEXT not in cbody:
            print("summontext not found, ignoring")
            continue
                
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            parent = r.get_info(thing_id=comment.parent_id)
            pbody = html.unescape(parent.body)
            ClinkParent = parent.permalink
            
            print("Writing txt file")
            f = open('CurrentAscii.txt', 'w', encoding='utf-8')
            f.write(pbody)
            f.close()
            
            mp.make_jpg('CurrentAscii', 'CurrentJPG')
            ILink = upload_imgur('CurrentJPG.jpg')['link']
            print(ILink)
        
            print('Replying to ' + cid)
            comment.reply(REPLYMESSAGE.format(ILink))
            
            cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?)', [cid, Clink, ClinkParent, ILink])
            sql.commit()
        else:
            print("Already replied to that comment")
                
    
while True:
    try:
        scan()
    except Exception as e:
        print("ERR", e)
    print('Sleeping ' + str(WAIT))
    time.sleep(WAIT)