#!/usr/bin/env python3
import praw  # simple interface to the reddit API
import time
import re
import sqlite3

#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT

    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")


add_regex = "add\((.+)\)"
rem_regex = "remove\((.+)\)"


# Logs into reddit
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)
print("Logged into Reddit")


sql = sqlite3.connect('users.db')
cur = sql.cursor()
sql.commit()

csql = sqlite3.connect('comments.db')
ccur = sql.cursor()
ccur.execute('CREATE TABLE IF NOT EXISTS comments(CID TEXT)')
csql.commit()

def update_database():
    comments = r.get_mentions(limit=MAXPOSTS)
    for comment in comments:
        
        cbody = comment.body
        cid = comment.id
        cauthor = comment.author

        ccur.execute('SELECT * FROM comments WHERE CID=?', [cid])
            if not ccur.fetchone():
                print("Found a summon comment")
            else:
                print("Already replied to that comment")
                continue

        add_match = re.match(add_regex, cbody)
        rem_match = re.match(rem_regex, cbody)

        if add_match:
            cur.execute('CREATE TABLE IF NOT EXISTS {user}(GAME TEXT)'.format(user=cauthor))
            add_list = add_match.group(1).split(', ')
            for game in add_list:
                cur.execute('INSERT INTO {user} VALUES(?)'.format(user=cauthor), [game])
        if rem_match:
            cur.execute('CREATE TABLE IF NOT EXISTS {user}(GAME TEXT)'.format(user=cauthor))
            rem_list = rem_match.group(1).split(', ')
            for game in rem_list:
                cur.execute('DELETE FROM comments WHERE GAME=?', [game])


        


# while True:
#     try:
#         mainLoop()
#     except Exception as e:
#         print("ERROR:", e)
#     print('Sleeping ' + str(WAIT) + ' seconds.\n')
#     time.sleep(WAIT)

mainLoop()
