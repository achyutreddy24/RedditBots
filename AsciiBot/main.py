import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3

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
    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
    
PERCENTAGE = 70 #the percent of normal chars the comment has to be under to be considered ascii art.

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, ILink TEXT)')
print('Loaded SQL Database')
sql.commit()

NormalChars = [' ','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','x','.',',',':','/',"/",'(',')','[',']','^']


def occurances(str, chars):
    count = 0
    for char in chars:
        count = count + str.count(c)
    return count

def scan():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        cid = comment.id
        cauthor = comment.author.name
        cur.execute('SELECT * FROM posts WHERE ID=?', [cid])
        if not cur.fetchone():
            cur.execute('INSERT INTO posts VALUES(?)', [cid])
            sql.commit()
            cfullBody = comment.body
            cbody = comment.body.lower()
            CO = occurances(cbody, NormalChars)            
            if (CO/len(cbody)>PERCENTAGE):
                f = open('CurrentAscii.txt', 'w')
                f.write(cfullBody)
                f.close()
                
                mp.make_jpg('CurrentAscii', 'CurrentJPG')
                
            
                print('Replying to ' + cid + ' by ' + cauthor)
                post.reply(REPLYMESSAGE.format("""IMGUR LINK"""))
