#! /bin/sh
cd ~/Documents/Tweetsaver
git stash >> ~/Documents/Cron/stash_errors.txt
python tweet_reader.py
git stash pop >> ~/Documents/Cron/stash_errors.txt
