"""REDDIT CONFIG"""
USERNAME  = "TwitchToYoutubeBot"
#This is the bot's Username. In order to send mail, he must have some amount of Karma.
PASSWORD  = "ThisIsNotACommonWord"
#This is the bot's Password. 
USERAGENT = "Uploads twitch past braodcasts to youtube(2 minutes, highlight) /u/FusionGaming"
#This bot gets a twitch link and uploads the equivalent youtube mirror for 1 minute after the timestamp. /u/FusionGaming"
SUBREDDIT = "conlangs"
#This is the sub or list of subs to scan for new posts. For a single sub, use "sub1". For multiple subreddits, use "sub1+sub2+sub3+..."
MAXPOSTS = 100
#This is how many posts you want to retrieve all at once. PRAW can download 100 at a time.
WAIT = 30
#This is how many seconds you will wait between cycles. The bot is completely inactive during this time.

REPLYMESSAGE ="""
[Here is a YouTube mirror for that specific time in the twitch VOD]({0})

---
^^This ^^action ^^was ^^performed ^^by ^^a ^^bot, ^^please ^^message ^^the ^^creator ^^/u/FusionGaming ^^for ^^more ^^information.

^^Click ^^Here ^^if ^^you ^^have ^^any ^^[suggestions](http://www.reddit.com/r/TwitchToYoutubeBot/comments/2pedjj/suggestions/)

^^Click ^^Here ^^if ^^you ^^want ^^to ^^learn ^^[more](http://www.reddit.com/r/TwitchToYoutubeBot/wiki/about)
[](/GNU Terry Pratchett)
"""


"""END REDDIT CONFIG"""

