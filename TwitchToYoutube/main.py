import twitchdownloader as td
import FormatVideoFile as fvd
import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import re
import sqlite3

#Example of link
#http://www.twitch.tv/pashabiceps/b/578370509?t=55m45s

import moviepy.config
#Delete this if moviepy is set up correctly already or change it to your path
moviepy.config.change_settings({"FFMPEG_BINARY": r"C:\FFMPEG\bin\ffmpeg.exe"})
#print(moviepy.config.get_setting("FFMPEG_BINARY"))

USERNAME  = "Convertor-Bot"
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD  = "Convertor-BotGO"
#This is the bot's Password. 
USERAGENT = "Testing things /u/FusionGaming"
#This is a short description of what the bot does."
SUBREDDIT = "all"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 3600
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.

#Debugging variables
MIN = 55
SEC = 45
ID = 578370509

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

def ConvertMtoS(Minutes, Seconds):
    return (Minutes*60)+Seconds


def GetPosts():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_new(limit=MAXPOSTS)
    for post in posts:
        if post.is_self == False:
            pid = post.id
            print(post.url)

#http://www.twitch.tv/pashabiceps/b/578370509?t=55m45s


#td.download_broadcast(578370509, 1)
#fvd.GetVideoSection(r"578370509_01.flv", 50, 100)

GetPosts()