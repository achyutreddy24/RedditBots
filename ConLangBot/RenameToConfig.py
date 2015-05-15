"""REDDIT CONFIG"""
USERNAME  = "FusionGaming"
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD  = "CoolCandy4"
#This is the bot's Password. 
USERAGENT = "/r/conlangs /u/FusionGaming"
#This bot gets a twitch link and uploads the equivalent youtube mirror for 1 minute after the timestamp. /u/FusionGaming"
SUBREDDIT = "conlangs"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 30
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.

REPLYMESSAGE ="""
{text}

--{author}

This post was gotten from a weekly small questions, this post was found here {link}
"""


"""END REDDIT CONFIG"""

