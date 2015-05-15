import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import re

SUMMONTEXT = """\+\/u\/conlangbot\s*\"([\s\S]+)\""""

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

sql = sqlite3.connect('data.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, CLink TEXT, CLinkParent TEXT, ILink TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS threads(PID TEXT, Title TEXT)')
sql.commit()

print('Loaded SQL Database')

def refresh_db(flairs):
    subreddit = r.get_subreddit(SUBREDDIT)
	posts = subreddit.get_new(limit=MAXPOSTS)
	for post in posts:
		# Anything that needs to happen every loop goes here.
		pid = post.id
        cur.execute('SELECT * FROM threads WHERE ID=?', [pid])
		if cur.fetchone():
            continue
        if 'Small Questions' in post.title or 'WWSQ' in post.title
        cur.execute('INSERT INTO threads VALUES(?, ?)', [pid, post.title])
        sql.commit()


def find_in_submissions(search_string):
	small.execute('SELECT * FROM threads')
    for row in cur:
        ID = row(0)
        post = r.get_info(thing_id=ID)
        for comment in post.comments:
            if search_string in comment.body.lower():
                if comment.is_root:
                    return comment.replies[0]
                else:
                    return comment

def scan():
    refresh_db()

    comments = r.get_mentions(limit=MAXPOSTS)
    for comment in comments:
        
        cbody = comment.body.lower()
        Clink = comment.permalink
        cid = comment.id
        

        match = re.search(SUMMONTEXT, cbody)
        if not match:
            continue
        word = match.group(1)        
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            def_post = find_in_submission(word)
            
            print('Replying to ' + cid)
            comment.reply(REPLYMESSAGE.format(ILink))
            
            cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?)', [cid, Clink, ClinkParent, ILink])
            sql.commit()
        else:
            print("Already replied to that comment")
