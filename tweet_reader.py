"""
Created on 7/16/14
@author: Louis Potok (louispotok@gmail.com)
"""

#TODO: more fault tolerance
    # change crontab to every 15 minutes
    # change script to:
        # if time is within the range
        # and no archive in the last 2 hours
        # archive
    # change read-script:
        #any over 2 months old?
        # if yes take the most recent.
#TODO: Json the tweet-writing
    # and perhaps all into one file?

import os
import twitter
import json
import ast
import datetime

class TweetBlogger():
    def __init__(self):
        self.home_dir = os.path.expanduser('~/Documents/Tweetsaver/')
        self.credentials_directory = self.home_dir + 'Credentials/'
        self.client = self.get_client()
        self.archive = os.path.expanduser('~/Box Sync/Tweetsaver/Tweets')
        self.log = self.home_dir + 'logs.txt'

    def get_client(self):
        oath_file = self.credentials_directory + 'twitter_oauth_tokens'
        tokens = ast.literal_eval(open(oath_file).read())
        consumer_key = tokens['consumer_key']
        consumer_secret = tokens['consumer_secret']

        MY_TWITTER_CREDS = self.credentials_directory + '.app_credentials'

        oauth_token, oauth_secret = open(MY_TWITTER_CREDS).read().split('\n')

        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=oauth_token,
                          access_token_secret=oauth_secret)

        return api

    def record_now(self):
        home_timeline = self.client.GetHomeTimeline(count=200)
        home_timeline = [str(status) for status in home_timeline]

        now = datetime.datetime.now()
        file_name = str(now.date()) + ' h' + str(now.hour)
        todays_record = self.archive + file_name + '.txt'
        with open(todays_record, "w") as f:
            f.write(str(home_timeline))

        self.write_log(operation='write',
                       entry = '# tweets: ' + str(len(home_timeline)))

    def output_two_months_ago(self):
        archive = os.listdir(self.archive)
        now = datetime.datetime.now()
        date_to_retrieve = now.date() - datetime.timedelta(60)
        file_name = str(date_to_retrieve) + ' h' + str(now.hour) + '.txt'

        log_entry = []
        if file_name not in archive:
            log_entry.append('No timelines with correct name')
            self.write_log(operation='read',entry=log_entry)
            return None

        log_entry.append('Found a timeline')
        timeline = ast.literal_eval(open(self.archive + file_name, 'r').read())
        log_entry.append('# tweets: ' + str(len(timeline)))

        timeline = [json.loads(tweet) for tweet in timeline]

        self.write_log(operation='read',
                       entry=log_entry)

    def write_log(self,operation,entry):
        with open(self.log,'a') as f:
            f.write('\n')
            f.write(str({'date': datetime.datetime.today(),
                         'operation': operation,
                         'entry': entry}))


def main():
    blogger = TweetBlogger()
    blogger.record_now()
    blogger.output_two_months_ago()


main()