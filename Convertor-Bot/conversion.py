import traceback
import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import re
import sqlite3

'''USER CONFIGURATION'''

USERNAME  = "Convertor-Bot"
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD  = "Convertor-BotGO"
#This is the bot's Password. 
USERAGENT = "/u/FusionGaming's bot. Converts from one unit into another unit"
#This is a short description of what the bot does. For example "/u/GoldenSights' Newsletter bot"
SUBREDDIT = "Fusion_Gaming"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
KEYWORDS = ["$", "€"]
#These are the words you are looking for
REPLYSTRING = "Found it!"
#This is the word you want to put in reply
MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 20
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.


'''All done!'''




WAITS = str(WAIT)

sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
print('Loaded Completed table')

sql.commit()

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

def makeConversion(str):
    pass

def scanSub():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    comments = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        cid = comment.id
        print('Looking at this comment: ' + cid)
        try:
            cauthor = comment.author.name
        except AttributeError:
            cauthor = '[DELETED]'
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [cid])
        if not cur.fetchone():
            print('Testting')
            cbody = comment.body.lower()
            i = 0
            for i in range(len(KEYWORDS)):
                print('Looking for keyword '+KEYWORDS[i])
                gex = "\\b%s\\b" % KEYWORDS[i].lower()
                match_object = re.search(gex, cbody)
                if match_object:
                    print('Found %s by %s' % (KEYWORDS[i], cauthor))
                    comment.reply(REPLYSTRING)
                i = i+1
            #cur.execute('INSERT INTO oldposts VALUES(?)', [cid])
    sql.commit()


while True:
    try:
        scanSub()
    except Exception as e:
        traceback.print_exc()
    print('Running again in ' + WAITS + ' seconds \n')
    sql.commit()
    time.sleep(WAIT)
