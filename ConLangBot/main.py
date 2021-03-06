import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
import re

SUMMONTEXT = """\+\/u\/connielangston\s*what\s*is\s*\"([\s\S]+)\""""

#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    MAXPOSTS = Config.MAXPOSTS
    REPLYMESSAGE = Config.REPLYMESSAGE
    SUBREDDIT = Config.SUBREDDIT
    WAIT = Config.WAIT
    NOTFOUNDTEXT = config.NOTFOUNDTEXT

    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
    

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

sql = sqlite3.connect('data.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT, Word TEXT, SQPOST TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS threads(PID TEXT, Title TEXT)')
sql.commit()

print('Loaded SQL Database')

roman_numerals = (('M',1000),('CM',900),('D',500),('CD',400),('C',100),('XC',90),('L',50),('XL',40),('X',10),('IX',9),('V',5),('IV',4),('I',1))

def convert_to_roman(n):
    result = ""
    for numeral, integer in roman_numerals:
        while n >= integer:
            result += numeral
            n -= integer
    return result

def refresh_db():
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_new(limit=MAXPOSTS)
    for post in posts:
        pid = post.id
        cur.execute('SELECT * FROM threads WHERE PID=?', [pid])
        if cur.fetchone():
            continue
        if 'Small Questions' in post.title or 'WWSQ' in post.title:
            cur.execute('INSERT INTO threads VALUES(?, ?)', [pid, post.title])
            sql.commit()


def find_in_submissions(search_string):
    cur.execute('SELECT * FROM threads')
    list_of_comments = []
    for row in cur:
        print(row)
        ID = row[0]
        post = r.get_submission(submission_id=ID)
        for comment in post.comments:
            if search_string in comment.body.lower():
                if comment.is_root:
                    print(comment.score)
                    list_of_comments.append([comment.replies[0], int(comment.score)])
                else:
                    print(comment.score)
                    list_of_comments.append([comment, int(comment.score)])
    return list_of_comments

def scan():
    refresh_db()

    comments = r.get_mentions(limit=5)
    for comment in comments:
        
        cbody = comment.body.lower()
        cid = comment.id
        
        print(cid)
        print(cbody)

        match = re.search(SUMMONTEXT, cbody)
        if not match:
            print("Comment has no summon text")
            continue
            
        word = match.group(1)        
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            def_post = find_in_submissions(word)
            def_post = sorted(def_post,key=lambda l:l[1], reverse=True)
            if def_post:
                author = "/u/" + str(def_post[0][0].author)
                print(author)
                body = str(def_post[0][0].body)
                link = str(def_post[0][0].permalink)
                iden = str(def_post[0][0].id)

                lst = body.split("\n")
                for x in range(len(lst)):
                    lst[x] = "> " + lst[x]

                body = "\n".join(lst)

                table_lst = []
                for i in range(len(def_post)):
                    if i is 0:
                        continue
                    table_lst.append(" | ".join(['[Post]('+str(def_post[i][0].permalink)+')', str(def_post[i][1])]))
                table = "\n".join(table_lst)

                print('Replying to ' + cid)
                comment.reply(REPLYMESSAGE.format(text=body, author=author, link=link, table=table))
            else:
                print('Replying to ' + cid)
                comment.reply(NOTFOUNDTEXT)
                iden = 'NOT FOUND'

            cur.execute('INSERT INTO posts VALUES(?, ?, ?)', [cid, word, iden])
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
