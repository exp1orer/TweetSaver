#! /bin/sh
cd ~/Documents/Tweetsaver
git reset HEAD origin/master >> ~/Documents/TweetSaver/Cron/stash_errors.txt
python tweet_reader.py
