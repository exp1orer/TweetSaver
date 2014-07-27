TweetSaver
==========

What if you could only view Twitter on a two month delay? What would you still care about? Who would you stop following?

TweetSaver is meant to get you thinking about your (social) media consumption on a longer timeframe. Why would you want to read something that you wouldn't care about two months from now?

TweetSaver is currently implemented as a class TweetBlogger with two public methods: record_now() and view_old_timeline().

record_now() as currently implemented, checks whether you have saved your home timeline in the last two hours. If not, and the local time is between 9AM and 8PM, it retrieves and saves your current home timeline. The archive is stored as a pickled dictionary of the format {'time_recorded (UTC)' :[tweets in your timeline]}.

view_old_timeline() is not ready for use yet. The first version will likely use the Storify API to create a "story" that is your saved tweets from N days ago.

I run record_now() as a cron job every 15 minutes. (Recall that it will only save tweets every two hours, tops.) Run the following command in the command line to set this up: 'crontab *DIRECTORY*/TweetSaver/Cron/crontab.txt'. You can use 'crontab -e' to verify.
