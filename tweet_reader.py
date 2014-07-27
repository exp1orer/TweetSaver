"""
Created on 7/16/14
@author: Louis Potok (louispotok@gmail.com)
"""


import os
import twitter
import ast
import datetime
import cPickle

class TweetBlogger():
    def __init__(self):
        self.home_dir = os.path.expanduser('~/Documents/Tweetsaver/')
        self.credentials_directory = self.home_dir + 'Credentials/'
        self.client = self._get_client()
        self.archive_filepath = os.path.expanduser('~/Box Sync/Tweetsaver/Tweets/tweet_archive.pkl')
        self.log = self.home_dir + 'logs.txt'

    def _get_client(self):
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
        now = datetime.datetime.utcnow()

        try:
            archive_file = open(self.archive_filepath,'r')
            archive = cPickle.load(archive_file)
        except IOError:
            archive = {}
        archive[now] = home_timeline

        cPickle.dump(archive,open(self.archive_filepath,'w'))

        self._write_log(operation='write',
                       entry = '# tweets: ' + str(len(home_timeline)))

    # def get_archive(self,days_ago=60):
    #     archive = os.listdir(self.archive)
    #     now = datetime.datetime.now()
    #     date_to_retrieve = now.date() - datetime.timedelta(days=days_ago)
    #     file_name = str(date_to_retrieve) + ' h' + str(now.hour) + '.txt'
    #
    #     log_entry = []
    #     if file_name not in archive:
    #         log_entry.append('No timelines with correct name')
    #         self._write_log(operation='read',entry=log_entry)
    #         return None
    #
    #     log_entry.append('Found a timeline')
    #     timeline = ast.literal_eval(open(self.archive + file_name, 'r').read())
    #     log_entry.append('# tweets: ' + str(len(timeline)))
    #
    #     timeline = [json.loads(tweet) for tweet in timeline]
    #
    #     self._write_log(operation='read',
    #                    entry=log_entry)

    def _write_log(self,operation,entry):
        with open(self.log,'a') as f:
            f.write('\n')
            f.write(str({'date': datetime.datetime.today(),
                         'operation': operation,
                         'entry': entry}))


def main():
    blogger = TweetBlogger()
    blogger.record_now()
    # blogger.get_archive()


main()