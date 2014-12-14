"""REDDIT CONFIG"""
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

REPLYMESSAGE ="""
[Here is a YouTube mirror for that specific time in the twitch VOD](www.youtube.com{0})


^This ^action ^was ^performed ^by ^a ^bot, ^please ^message ^the ^creator ^/u/FusionGaming ^for ^more ^information
"""


"""END REDDIT CONFIG"""

VIDEOLENGTH = 60
#This is how long the video will be in seconds
FPS = 30
#How many frames per second the final video will be

YOUTUBEVIDEOSPAGE = "https://www.youtube.com/channel/UCAoktq8B395WJljEcIANALw/videos"
#This is the link to your videos page in youtube, for example
#https://www.youtube.com/channel/UCAoktq8B395WJljRcIANALp/videos"
#or
#https://www.youtube.com/user/LinusTechTips/videos


REGEXLINK = "\/watch\?v\=(\S)+"
BASELINK = "www.youtube.com"

EPASSWORD = ""
#Email password, can be any gmail, don't recommend using main account
EUSERNAME = ""
#Email address
UPLOADLINK = [""]
#Youtube Mobile Upload Link, square brackets are required

VIDEODESCRIPTION = """
This video was posted by a bot, view source here:
https://github.com/achyutreddy24/RedditBots/tree/master/TwitchToYoutube

View original twitch source here:
{0}

Created by /u/FusionGaming (Achyut Reddy)
"""
#Description of the youtube video