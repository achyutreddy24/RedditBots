import traceback
import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import re
import sqlite3
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    SUBREDDIT = Config.SUBREDDIT
    MAXPOSTS = Config.MAXPOSTS
    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
WAIT = 20
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.


CURRENCY = ["$", "€"]
LENGTH = ["kilometer", "mile"]

BIGLIST = [CURRENCY, LENGTH]
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

def makeConversion(unitNumber, unitType, unitIndex):
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
            print('Testing')
            cbody = comment.body.lower()
            for typeUnit in BIGLIST:
                i = 0
                for i in range(len(typeUnit)):
                    print('Looking for keyword '+typeUnit[i])
                    gex = "([\\d\\.]*)%s([\\d\\.]*)" % typeUnit[i].lower()
                    gex = gex.replace("$", "\\$")
                    match_object = re.search(gex, cbody)
                    if match_object: # re add no number handling
                        numberUnit = float(match_object.group(1) if len(match_object.group(1)) > 0 else match_object.group(2))
                        makeConversion(numberUnit, typeUnit, i)
                        print('Found %s by %s with value %s' % (typeUnit[i], cauthor, numberUnit))
                        comment.reply(REPLYSTRING)
                    i = i+1
            #cur.execute('INSERT INTO oldposts VALUES(?)', [cid])
    sql.commit()

def xor(a, b):
    return (a or b) and not (a and b)

while True:
    try:
        scanSub()
    except Exception as e:
        traceback.print_exc()
    print('Running again in ' + WAITS + ' seconds \n')
    sql.commit()
    time.sleep(WAIT)
