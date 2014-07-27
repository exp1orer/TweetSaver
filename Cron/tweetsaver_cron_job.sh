#! /bin/sh
cd ~/Documents/Tweetsaver
git stash
python tweet_reader.py
git stash pop