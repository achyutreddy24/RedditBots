import praw # simple interface to the reddit API, also handles rate limiting of requests
import time

SUMMONTEXT = """+/u/ascii-text-bot"""

#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    MAXPOSTS = Config.MAXPOSTS
    REPLYMESSAGE = Config.REPLYMESSAGE
    SUBREDDIT = COnfig.SUBREDDIT    

    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
    
WAIT = 5

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

sql = sqlite3.connect('posts.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, CLink TEXT, CLinkParent TEXT, ILink TEXT)')
sql.commit()

ssql = sqlite3.connect('small.db')
small = ssql.cursor()
small.execute('CREATE TABLE IF NOT EXISTS threads(PID TEXT, Title TEXT)')
ssql.commit()

print('Loaded SQL Database')

def refresh_db(flairs):
    subreddit = r.get_subreddit(SUBREDDIT)
	posts = subreddit.get_new(limit=MAXPOSTS)
	for post in posts:
		# Anything that needs to happen every loop goes here.
		pid = post.id
        if 'Small Questions' in post.title
        small.execute('INSERT INTO posts VALUES(?, ?)', [pid, post.title])
        ssql.commit()


def find_in_submissions(string, flairs):
	

def scan():
    comments = r.get_mentions(limit=MAXPOSTS)
    for comment in comments:
        
        cbody = comment.body.lower()
        Clink = comment.permalink
        cid = comment.id
        
        print(comment.created_utc)
        
        #if comment.is_root:
        #    print("Comment is root, ignoring")
        #    continue
        if SUMMONTEXT not in cbody:
            print("summontext not found, ignoring")
            continue
                
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            parent = r.get_info(thing_id=comment.parent_id)
            try:
                pbody = html.unescape(parent.body)
                ClinkParent = parent.permalink
            except Exception as e:
                pbody = html.unescape(parent.selftext)
                ClinkParent = parent.permalink
            
            pbody = pbody.replace("\xc2\xa0", " ")
            
            print("Writing txt file")
            f = open('CurrentAscii.txt', 'w', encoding='utf-32')
            f.write(pbody)
            f.close()
            print('Wrote text file')
            
            mp.make_jpg('CurrentAscii', 'CurrentJPG')
            ILink = upload_imgur('CurrentJPG.jpg')['link']
            print(ILink)
        
            print('Replying to ' + cid)
            comment.reply(REPLYMESSAGE.format(ILink))
            
            cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?)', [cid, Clink, ClinkParent, ILink])
            sql.commit()
        else:
            print("Already replied to that comment")
