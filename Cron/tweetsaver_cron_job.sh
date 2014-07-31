#! /bin/sh
cd ~/Documents/Tweetsaver
git stash >> ~/Documents/TweetSaver/Cron/stash_errors.txt
python tweet_reader.py
git stash pop >> ~/Documents/TweetSaver/Cron/stash_errors.txt
