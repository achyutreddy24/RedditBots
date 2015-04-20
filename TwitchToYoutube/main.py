#!/usr/bin/env python3
import os
import sys
import praw  # simple interface to the reddit API
import time
import re
import sqlite3
import requests

import twitchdownloader as td
import FormatVideoFile as fvd
import YoutubeLink as yl
import upload as upl
# import SendEmail as se # no longer needed with google api

#  Example of link
#  http://www.twitch.tv/pashabiceps/b/578370509?t=55m45s

#import moviepy.config
#  Delete this if moviepy is set up correctly already or change it to your path
#moviepy.config.change_settings({"FFMPEG_BINARY": r"C:\FFMPEG\bin\ffmpeg.exe"})
#  print(moviepy.config.get_setting("FFMPEG_BINARY"))


#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    SUBREDDIT = Config.SUBREDDIT
    MAXPOSTS = Config.MAXPOSTS
    REPLYMESSAGE = Config.REPLYMESSAGE
    WAIT = Config.WAIT
    EXCLUDEDSUBS = Config.EXCLUDEDSUBS

    VIDEOLENGTH = Config.VIDEOLENGTH

    EUSERNAME = Config.EUSERNAME
    UPLOADLINK = Config.UPLOADLINK
    VIDEODESCRIPTION = Config.VIDEODESCRIPTION
    BASELINK = Config.BASELINK
    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")

# Regex pattern to get the correct twitch links
# SAMPLE LINK
# http://www.twitch.tv/pashabiceps/b/578370509?t=55m45s
url_pattern = re.compile("""http://www\.twitch\.tv\/.+\/b\/(\d+)\?t=(?:(\d*)h)?(?:(\d*)m)?(?:(\d*)s)?""")
time_in_title = re.compile("""{{(\d+):(\d+)}}""")
extract_subreddit = re.compile("""\/r\/(.+?)\/""")

# Logs into reddit
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)
print("Logged into Reddit")


sql = sqlite3.connect('posts.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(PID TEXT, TITLE TEXT, TLINK TEXT, YLINK TEXT)')
print('Loaded SQL Database')
sql.commit()


def ConvertMtoS(Hours, Minutes, Seconds):
    """Converts to seconds"""
    Minutes = (int(Hours)*60)+int(Minutes)
    return int((int(Minutes)*60)+int(Seconds))
    
def MakeTime(Hours, Minutes, Seconds):
    if not Hours:
        Hours = 0
    if not Minutes:
        Minutes = 0
    if not Seconds:
        Seconds = 0
    return ConvertMtoS(Hours, Minutes, Seconds)
    
def expand_short_url(link):
    response = requests.get('http://api.longurl.org/v2/expand?url={url}&format=json&user-agent=TwitchToYoutubeRedditBot-see-reddit.com/r/TwitchToYoutubeBot'.format(url=link))
    return response.json()['long-url']

def get_subreddit(post):
    url = post.short_link
    long_url = expand_short_url(url)
    sub = re.search(extract_subreddit, long_url)
    return sub.group(1)
    

def GetMentions():
    comments = r.get_mentions(limit=MAXPOSTS)
    for comment in comments:
        
        cbody = comment.body.lower()
        Clink = comment.permalink
        cid = comment.id

        cur.execute('SELECT * FROM posts WHERE PID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
        else:
            print("Already replied to that comment")
            continue

        matched = re.match(url_pattern, cbody)
        if matched is None:
            pass
        else:
            rID = matched.group(1)
            rHRS = matched.group(2)
            rMIN = matched.group(3)
            rSEC = matched.group(4)
            
            dict = {"ID":rID, "HRS":rHRS, "MIN": rMIN, "SEC":rSEC, "POST":comment, "TITLE":Clink, "URL":matched.group(0)}
            return dict

        if comment.is_root:
            continue

        parent = r.get_info(thing_id=comment.parent_id)
        cbody = parent.body.lower()
        Clink = parent.permalink
        cid = parent.id

        cur.execute('SELECT * FROM posts WHERE PID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
        else:
            print("Already replied to that comment")
            continue

        matched = re.match(url_pattern, cbody)
        if matched is None:
            pass
        else:
            rID = matched.group(1)
            rHRS = matched.group(2)
            rMIN = matched.group(3)
            rSEC = matched.group(4)
            
            dict = {"ID":rID, "HRS":rHRS, "MIN": rMIN, "SEC":rSEC, "POST":parent, "TITLE":Clink, "URL":matched.group(0)}
            return dict
                
        

def GetPosts():
    """Finds twitch url and returns id and time"""
    # subreddit = r.get_subreddit("Fusion_Gaming")
    posts = r.get_domain_listing('twitch.tv', sort='new',limit=MAXPOSTS)
    # posts = subreddit.get_new(limit=MAXPOSTS)
    for post in posts:
        print(post.url)
        print("NSFW "+str(post.over_18))
        #If post is nsfw, it skips
        if post.over_18:
            continue
        cur.execute('SELECT * FROM posts WHERE TLINK=?', [post.url])
        #only executes if twitchlink is not in database
        if not cur.fetchone():
            print("HAVENOTREPLIED")
            if post.is_self is False:
                pid = post.id
                matched = re.match(url_pattern, post.url)
                if matched is None:
                    pass
                else:
                    sub = get_subreddit(post)
                    print('Sub is '+ sub)
                    if sub in EXCLUDEDSUBS:
                        print('Sub is Excluded')
                        cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?)', [pid, post.title, post.url, 'EXCLUDEDSUB'])
                        continue
                    rID = matched.group(1)
                    rHRS = matched.group(2)
                    rMIN = matched.group(3)
                    rSEC = matched.group(4)
                    
                    dict = {"ID":rID, "HRS":rHRS, "MIN": rMIN, "SEC":rSEC, "POST":post, "TITLE":post.title, "URL":post.url}
                    print("Title is "+post.title)
                    return dict
            else:
                print("Will not reply to self")
        else:
            print("Already replied to that")

def DownloadTwitchANDReturnStartingTime(ID, TimeInSeconds):
    """Figures out which chunk to download and where the segment is in that chunk"""
    chunk_info = td.getChunkNum(ID, TimeInSeconds)
    td.download_broadcast(ID, chunk_info[0])
    return chunk_info[1]
    
def CutVideo(fileName, startTime, endTime):
    """Cuts the video files"""
    fvd.GetVideoSection(fileName, startTime, endTime)
  
def LoopVideoCheck(titleOfVideo):
    UploadStatus = yl.CheckIfUploaded(titleOfVideo)
    count = 1
    while UploadStatus is None:
        UploadStatus = yl.CheckIfUploaded(titleOfVideo)
        if UploadStatus:
            return UploadStatus # YoutubeLink
        if count > 3600:
            print("Waited 1 hour, breaking loop")
            break
        sys.stdout.write("\rSleeping {} seconds to wait for video upload.".format(str(count)))
        sys.stdout.flush()
        time.sleep(1)
        count = count + 1
    sys.stdout.write("\n")
    return UploadStatus


def mainLoop():
    url_info = GetPosts()
    if url_info is None:
        url_info = GetMentions()
    # GetPosts returns this list if it finds a url match
    if url_info:
        ID = url_info["ID"]
        POST = url_info["POST"]
        TITLE = url_info["TITLE"]

        title_matched = re.search(time_in_title, TITLE)
        new_time = 0
        if title_matched:
            minutes = int(title_matched.group(1))
            seconds = int(title_matched.group(2))
            new_time = MakeTime(Hours=0,Minutes=minutes, Seconds=seconds)
        # Sets video length to time found in title
        video_length = new_time if new_time < 600 and new_time > 30 else VIDEOLENGTH

        # Truncates the title to match youtube's 95 character limit
        TITLE = (TITLE[:90] + '...') if len(TITLE) > 90 else TITLE

        URL = url_info["URL"]

        STime = MakeTime(url_info["HRS"], url_info["MIN"], url_info["SEC"])

        LINK = ""
        StartingTime = None
        try:
            StartingTime = DownloadTwitchANDReturnStartingTime(ID, STime)
        except Exception as e:
            print("Twitch Error is: "+str(e))
            LINK = "Twitch Error " + str(e)

        if StartingTime:
            try:
                CutVideo(ID+".flv", StartingTime, StartingTime+video_length)

                # Need to email this file to the mobile upload link
                # Old command replaced with google api now
                # se.send_mail(EUSERNAME, UPLOADLINK, TITLE, VIDEODESCRIPTION.format(URL), files=[ID+".flv_edited.mp4"])
                # LINK = LoopVideoCheck(TITLE) # Keeps Looping until uploaded video is detected


                # Uploads with google api
                try:
                    LINK = upl.upload(ID+".flv_edited.mp4", TITLE, VIDEODESCRIPTION.format(URL))
                except Exception as err:
                    import traceback
                    traceback.print_exc()
                    print(err)
                    if LINK is None:
                       print("upload returned none, running LoopVideoCheck")
                       LINK = LoopVideoCheck(TITLE) # Keeps Looping until uploaded video is detected
                        
                try:
                    POST.add_comment(REPLYMESSAGE.format(LINK))
                except:
                    POST.reply(REPLYMESSAGE.format(LINK))
                print("Comment reply success")
            except Exception as e:
                LINK = "ERROR: " + str(e)
        else:
            pass


        cur.execute('INSERT INTO posts VALUES(?, ?, ?, ?)', [ID, TITLE, URL, LINK])
        sql.commit()

        # os.remove(ID+".flv")
        # os.remove(ID+".flv_edited.mp4")
        # print("Deleted Files")

    else:
        print("No link found this time")

# while True:
#     try:
#         mainLoop()
#     except Exception as e:
#         print("ERROR:", e)
#     print('Sleeping ' + str(WAIT) + ' seconds.\n')
#     time.sleep(WAIT)

mainLoop()
