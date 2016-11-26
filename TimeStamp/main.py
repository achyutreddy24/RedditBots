import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
import re
import OAuth2Util

URL_DETECT = re.compile("""(?:https?:\/\/)?(?:youtu\.be\/|(?:www\.)?youtube\.com\/watch(?:\.php)?\?.*v=)([a-zA-Z0-9\-_]+)((?:\?t=\d+)?)""")



TIMESTAMP_DETECT = re.compile("""(?:(\d{0,2}):)?(\d{1,2}):(\d{1,2})""")
#TIMESTAMP_DETECT = re.compile("""(\d{1,2}):(\d{2})""")

CON_URL = """https://youtu.be/{vid_id}?t={t}"""

BLOCKED = ['youtubefactsbot']

#  Import Settings from Config.py
try:
    import Config
    USERAGENT = Config.USERAGENT
    MAXPOSTS = Config.MAXPOSTS
    REPLYMESSAGE = Config.REPLYMESSAGE
    
    
    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
    
WAIT = 5

r = praw.Reddit(USERAGENT)
#r.login(USERNAME, PASSWORD)
o = OAuth2Util.OAuth2Util(r)



sql = sqlite3.connect('comments.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, CLink TEXT, YTLink TEXT, TIME TEXT, NewYTLink TEXT)')
print('Loaded SQL Database')
sql.commit()

def calc_seconds(hour, minute, second):
    return 3600*hour+60*minute+second

def scan():
    subreddit = r.get_subreddit("all")
    stream = praw.helpers.comment_stream(r, subreddit, limit=100)
    for comment in stream:
        
        cbody = comment.body
        
        
        # Faster than regex to eliminate most comments
        if 'youtu' not in cbody:
            continue
        
        print(cbody)
        
        Clink = comment.permalink
        cid = comment.id
        author = comment.author
        
        if author.name in BLOCKED:
            continue
        
        match_yt = URL_DETECT.search(cbody)
        if match_yt is None:
            continue
            
        if match_yt.group(2) is not '': # TimeStamp
            continue
                
        match_ts = TIMESTAMP_DETECT.search(cbody)
        if match_ts is None:
            continue

        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            yt_id = match_yt.group(1) # Video ID
            
            hours = int(match_ts.group(1)) if match_ts.group(1) is not None else 0
            minutes = int(match_ts.group(2))
            seconds = int(match_ts.group(3))
            
            total_time = calc_seconds(hours, minutes, seconds)
            
            new_url = CON_URL.format(vid_id=yt_id, t=total_time)
            
            print('Replying to ' + cid)
            comment.reply(REPLYMESSAGE.format(new_url))

            
            cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?, ?)', [cid, Clink, match_yt.group(0), match_ts.group(0), new_url])
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
