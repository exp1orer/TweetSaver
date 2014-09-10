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
        self.archive_directory = os.path.expanduser('~/Box Sync/Tweetsaver/Tweets/')
        self.log = self.home_dir + 'logs.txt'

    def _get_client(self):
        oauth_file = self.credentials_directory + 'twitter_oauth_tokens'
        tokens = ast.literal_eval(open(oauth_file).read())
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
        archive = self.get_archive()

        if not self._is_time_to_record(archive.keys()):
            return

        home_timeline = self.client.GetHomeTimeline(count=200)
        now = datetime.datetime.utcnow()
        current_archive = {now: home_timeline}
        file_name = now.strftime('%Y-%m-%d h%H')
        filepath_for_archive = self.archive_directory+file_name+'.pkl'

        cPickle.dump(current_archive,open(filepath_for_archive,'w'))

        self._write_log(operation='write',
                       entry = '# tweets: ' + str(len(home_timeline)))

    def get_archive(self):
        archive_files = [f for f in os.listdir(self.archive_directory) if '.pkl' in f]
        archive = {}
        for f in archive_files:
            rel_archive = cPickle.load(open(self.archive_directory + f))
            archive.update(rel_archive)
        return archive

    # def play_with_archive(self,days_ago=60):
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

    def _is_time_to_record(self,archive_times):
        current_time_local = datetime.datetime.now()
        if not 9<=current_time_local.hour <= 19:
            return False
        if len(archive_times) == 0:
            return True

        current_time_utc = datetime.datetime.utcnow()

        most_recent_archive_entry = sorted(archive_times)[-1]
        time_since_last_archive = current_time_utc - most_recent_archive_entry
        seconds_since_last_archive = time_since_last_archive.total_seconds()
        return seconds_since_last_archive > 60*60*2



def main():
    blogger = TweetBlogger()
    blogger.record_now()
    # blogger.get_archive()


main()