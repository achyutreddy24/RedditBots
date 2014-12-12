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

USERNAME  = ""
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD  = ""
#This is the bot's Password. 
USERAGENT = ""
#This is a short description of what the bot does."
SUBREDDIT = "all"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 3600
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.

try:
    import Config #This is a file in my python library which contains my Bot's username and password. I can push code to Git without showing credentials
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
except ImportError:
    pass

#Debugging variables
rMIN = 55
rSEC = 45
rID = 578370509

url_pattern = re.compile("""http://www\.twitch\.tv\/.+\/b\/(\d+)(?:\?t=(\d+)m(\d+)s)""")

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
            
            matched = re.match(url_pattern, post.url)
            if matched is None:
                pass #Do stuff if it doesn't match
            else:
                rID = matched.group(1)
                rMIN = matched.group(2)
                rSEC = matched.group(3)
				
def DownloadTwitchANDReturnStartingTime(ID, TimeInSeconds):
	chunk_info = td.getChunkNum(ID, TimeInSeconds)
    td.download_broadcast(ID, chunk_info[0])
    return chunk_info[1]
    
def CutVideo(fileName, startTime, endTime):
    fvd.GetVideoSection(fileName, 50, 100)
            

#http://www.twitch.tv/pashabiceps/b/578370509?t=55m45s


#td.download_broadcast(578370509, 1)
#fvd.GetVideoSection(r"578370509_01.flv", 50, 100)

#GetPosts()


