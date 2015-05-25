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

csql = sqlite3.connect('history.db')
ccur = csql.cursor()
ccur.execute('CREATE TABLE IF NOT EXISTS comments(CID TEXT)')
ccur.execute('CREATE TABLE IF NOT EXISTS posts(PID TEXT)')
csql.commit()

roman_numerals = (('M',1000),('CM',900),('D',500),('CD',400),('C',100),('XC',90),('L',50),('XL',40),('X',10),('IX',9),('V',5),('IV',4),('I',1))

def convert_to_roman(n):
    result = ""
    for numeral, integer in roman_numerals:
        while n >= integer:
            result += numeral
            n -= integer
    return result

def simple_format(s):
    s = s.lower()
    s = s.replace(" ", "")
    return s

def reddit_table_format(user_list):
    message_list = ['Game | Post', '--- | ---']
    for row in user_list:
        message_list.append('{game} | [{post}]({link})'.format(game=row[0], post=row[1], link=row[2]))
    return '\n'.join(message_list)

def update_database():
    comments = r.get_mentions(limit=50)
    for comment in comments:
        
        cbody = comment.body
        cid = comment.id
        cauthor = comment.author

        ccur.execute('SELECT * FROM comments WHERE CID=?', [cid])
        if not ccur.fetchone():
            print(cbody)
        else:
            print("Already replied to that comment")
            continue

        add_match = re.search(add_regex, cbody)
        rem_match = re.search(rem_regex, cbody)

        cur.execute('CREATE TABLE IF NOT EXISTS {user}(game TEXT)'.format(user=cauthor))
        
        reply = ""

        make_reply = False

        if '!NotifyAll' in cbody:
            make_reply = True
            print('Found notify keyword')
            game_list = []
            for row in cur.execute('SELECT game FROM {user}'.format(user=cauthor)):
                game_list.append(row[0])
            reply = reply + 'Here are all the games you are being notified of\n\n'
            reply = reply + '\n\n'.join(game_list)

        if '!StopNotify' in cbody:
            make_reply = True
            print('Found stop keyword')
            cur.execute('DROP TABLE {user}'.format(user=cauthor))
            reply = reply + '\n\nNo longer notifying you of game deals\n\n'

        if add_match:
            make_reply = True
            print('Found add keyword')
            add_list = add_match.group(1).split(', ')
            for game in add_list:
                cur.execute('SELECT * FROM {user} where game=?'.format(user=cauthor), [game])
                if cur.fetchone():
                    continue
                cur.execute('INSERT INTO {user} VALUES(?)'.format(user=cauthor), [game])
            print('Added {} into database for {}'.format(add_list, cauthor))
        if rem_match:
            make_reply = True
            print('Found remove keyword')
            rem_list = rem_match.group(1).split(', ')
            for game in rem_list:
                cur.execute('DELETE FROM {user} WHERE game=?'.format(user=cauthor), [game])
            print('Removed {} from database for {}'.format(rem_list, cauthor))

        if add_match:
            reply = reply + "The following games were added: {}\n\n".format(add_match.group(1))
        if rem_match:
            reply = reply + "The following games were removed: {}\n\n".format(rem_match.group(1))

        if make_reply:
            reply = reply + "\n\n***\n^^I'm ^^a ^^bot, ^^this ^^action ^^was ^^performed ^^automatically.\n***\n"
            comment.reply(reply)
            print('Replied to comment')
        else:
            print('No keywords found, skipping')

        ccur.execute('INSERT INTO comments VALUES(?)', [cid])

        sql.commit()
        csql.commit()

def iter_users():
    print('Getting newest posts')
    subreddit = r.get_subreddit("GameDeals")
    posts = list(subreddit.get_new(limit=50))

    for post in posts[:]:
        ccur.execute('SELECT PID FROM posts WHERE PID=?', [post.id])
        if ccur.fetchone():
            posts.remove(post)
        else:
            ccur.execute('INSERT INTO posts VALUES(?)', [post.id])
            csql.commit()

    csql.commit()
    
    print('Len of list is '+str(len(posts)))

    if not posts:
        print('No new posts, skipping')
        return 0

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for user in cur.fetchall():
        print('Iterating over users')
        user = user[0]

        user_list = []
        
        cur.execute('SELECT game FROM {user}'.format(user=user))
        if not cur.fetchone:
            #User with no games gets deleted
            print('Deleted '+user)
            cur.execute('DROP TABLE {user}'.format(user=user))
            continue

        for row in cur.execute('SELECT game FROM {user}'.format(user=user)):
            game = row[0]
            print(game)
            fgame = simple_format(game)

            for post in posts:
                title = post.title
                ftitle = simple_format(title)

                if fgame in ftitle:
                    print(game, title)
                    user_list.append([game, title, post.permalink])

        if user_list is False:
            continue

        print(user_list)

        message = reddit_table_format(user_list)
        message = "New notifications for games that you are tracking\n\n"+message

        r.send_message(user, "Game Notification", message)
        print('Sent PM with notifications')

        sql.commit()
        csql.commit()


            
def main_loop():
    while(True):
        try:
            update_database()
            iter_users()
            print('sleeping')
            time.sleep(30)
        except:
            time.sleep(30)

main_loop()





