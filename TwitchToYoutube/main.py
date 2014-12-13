import twitchdownloader as td
import FormatVideoFile as fvd
import YoutubeLink as yl
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


#Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    SUBREDDIT = Config.SUBREDDIT
    MAXPOSTS = Config.MAXPOSTS
    WAIT = Config.WAIT
    
    VIDEOLENGTH = Config.VIDEOLENGTH
except ImportError:
    print("Error Importing Config.py")



#Regex pattern to get the correct twitch links
#SAMPLE LINK
#http://www.twitch.tv/pashabiceps/b/578370509?t=55m45s
url_pattern = re.compile("""http://www\.twitch\.tv\/.+\/b\/(\d+)(?:\?t=(\d+)m(\d+)s)""")

#Logs into reddit
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)


def ConvertMtoS(Minutes, Seconds):
    """Converts to seconds"""
    return (Minutes*60)+Seconds


def GetPosts():
    """Finds twitch url and returns id and time"""
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_new(limit=MAXPOSTS)
    for post in posts:
        if post.is_self == False:
            pid = post.id
            matched = re.match(url_pattern, post.url)
            if matched is None:
                pass #Do stuff if it doesn't match
            else:
                rID = matched.group(1)
                rMIN = matched.group(2)
                rSEC = matched.group(3)
                lst = [rID, rMIN, rSEC, pid]
                return lst
				
def DownloadTwitchANDReturnStartingTime(ID, TimeInSeconds):
    """Figures out which chunk to download and where the segment is in that chunk"""
    chunk_info = td.getChunkNum(ID, TimeInSeconds)
    td.download_broadcast(ID, chunk_info[0])
    return chunk_info[1]
    
def CutVideo(fileName, startTime, endTime):
    """Cuts the video files"""
    fvd.GetVideoSection(fileName, startTime, endTime)
  
def LoopVideoCheck(titleOfVideo, TimeBetweenLoops):
    UploadStatus = yl.CheckIfUploaded(titleOfVideo)
    while UploadStatus is None:
        UploadStatus = yl.CheckIfUploaded(titleOfVideo)
        if UploadStatus:
            return UploadStatus #YoutubeLink
        print('Sleeping ' + str(TimeBetweenLoops) + ' seconds to wait for video upload.\n')
        time.sleep(TimeBetweenLoops)
    

def mainLoop():
    url_info = GetPosts()
    #GetPosts returns this list if it finds a url match
    if url_info is not None:
        ID = url_info[0]
        STime = ConvertMtoS(url_info[1], url_info[2])
        StartingTime = DownloadTwitchANDReturnStartingTime(ID, STime)
        CutVideo(ID, StartingTime, StartingTime+VIDEOLENGTH)
        
        #Need to email this file to the mobile upload link
        
        LINK = LoopVideoCheck(videoTitle, 30) #Keeps Looping until uploaded video is detected
        