"""REDDIT CONFIG"""
USERNAME  = ""
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD  = ""
#This is the bot's Password. 
USERAGENT = ""
#This bot gets a twitch link and uploads the equivalent youtube mirror for 1 minute after the timestamp."
SUBREDDIT = "all"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.

REPLYMESSAGE ="""
[Here is an Imgur link for that ASCII art]({0})

---
^^This ^^action ^^was ^^performed ^^by ^^a ^^bot, ^^please ^^message ^^the ^^creator ^^/u/FusionGaming ^^for ^^more ^^information ^^and ^^to ^^report ^^bugs.
"""
"""END REDDIT CONFIG"""

"""IMGUR CONFIG"""
ID = 'API ID'
SECRET = 'API Secret'