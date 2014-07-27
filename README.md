TweetSaver
==========

What if you could only view Twitter on a two month delay? What would you still care about? Who would you stop following?

TweetSaver is meant to get you thinking about your (social) media consumption on a longer timeframe. Why would you want to read something that you wouldn't care about two months from now?

TweetSaver is currently implemented as a class TweetBlogger with two public methods: record_now() and view_old_timeline().

record_now() saves your current home timeline in JSON to an archive location of your choosing. view_old_timeline() is not ready for use yet. The first version will likely use the Storify API to create a "story" that is your saved tweets from N days ago.

I run record_now() as a cron job every few hours.
