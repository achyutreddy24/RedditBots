import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
import html
from imgurpython import ImgurClient
import OAuth2Util
import subprocess

SUMMONTEXT = """+/u/ascii-text-bot"""

#  Import Settings from Config.py
try:
    import Config
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
#r.login(USERNAME, PASSWORD)
o = OAuth2Util.OAuth2Util(r)


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
        
        cbody = comment.body
        Clink = comment.permalink
        cid = comment.id
        
        print(comment.created_utc)
        
        if comment.is_root:
            print("Comment is root, ignoring")
            continue
        if SUMMONTEXT not in cbody.lower():
            print("summontext not found, ignoring")
            continue
                
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            parent = r.get_info(thing_id=comment.parent_id)
            try:
                pbody = parent.body
                ClinkParent = parent.permalink
            except Exception as e:
                pbody = parent.selftext
                ClinkParent = parent.permalink
            
            temp = open('comment.html', 'r')
            t = temp.read()
            t = t.format(karma=parent.score, username=parent.author, body=pbody)
            temp.close

            f = open('CurrentAscii.html', 'w')
            f.write(t)
            f.close()
            print('Wrote text file')

            subprocess.call('xvfb-run --server-args="-screen 0, 1280x1200x24" cutycapt --url=127.0.0.1/asciibot/CurrentAscii.html --out=CurrentPNG.png', shell=True)

            ILink = upload_imgur('CurrentPNG.png')['link']
            print(ILink)
            
            print('Replying to ' + cid)
            comment.reply(REPLYMESSAGE.format(ILink))

            subprocess.call('rm CurrentPNG.png CurrentAscii.html', shell=True)
            
            cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?)', [cid, Clink, ClinkParent, ILink])
            sql.commit()
        else:
            print("Already replied to that comment")
                
    
while True:
    try:
        o.refresh()
        scan()
    except Exception as e:
        print("ERR", e)
    print('Sleeping ' + str(WAIT))
    time.sleep(WAIT)
