WAITS = str(WAIT)


article_links = []
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, ILink TEXT)')
print('Loaded SQL Database')
sql.commit()

def scan():
	subreddit = r.get_subreddit(SUBREDDIT)
	
