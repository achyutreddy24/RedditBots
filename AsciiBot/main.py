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
PERCENTAGE = 0.3 #the percent of normal chars the comment has to be over to be considered ascii art.

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

img = ImgurClient(ID, SECRET)

sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, CLink, ILink TEXT)')
print('Loaded SQL Database')
sql.commit()

NormalChars = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','x','.',',','/',"/",'(',')','[',']','^']


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
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            cfullBody = comment.body
            cbody = comment.body.lower().replace(" ", "")
            Clink = comment.permalink
            CO = occurances(cbody, NormalChars)
            print("CO is "+str(CO)+" cbody len is "+str(len(cbody))+" per is "+str(CO/len(cbody)))
            if (CO/len(cbody)<PERCENTAGE):
                print("Found an ascii comment")
                f = open('CurrentAscii.txt', 'w')
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
                print("Ignored")
                
    
while True:
    try:
        scan()
    except Exception as e:
        print("ERR", e)
    print('Sleeping ' + str(WAIT))
    time.sleep(WAIT)