"""
Created on 7/16/14
@author: Louis Potok (louispotok@gmail.com)
"""


import os
import twitter
import ast
import datetime
import cPickle
import pymongo

class TweetBlogger():
    def __init__(self):
        self.home_dir = os.path.expanduser('~/Documents/Tweetsaver/')
        self.credentials_directory = self.home_dir + 'Credentials/'
        self.twitter_client = self._get_twitter_client()
        self.mongo_client = self._get_mongo_client()
        self.tweet_storage = self._get_tweet_storage()
        self.log_storage = self._get_log_storage()
        self.archive_directory = os.path.expanduser('~/Box Sync/Tweetsaver/Tweets/')
        self.log = self.home_dir + 'logs.txt'

    def _get_mongo_client(self):
        return pymongo.MongoClient('louismbp',27000)

    def _get_tweet_storage(self):
        return self.mongo_client.tweetsaver.tweets

    def _get_log_storage(self):
        return self.mongo_client.tweetsaver.logs

    def _get_twitter_client(self):
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
        try:
            home_timeline = self.twitter_client.GetHomeTimeline(count=200)
        except twitter.error.TwitterError:
            return
        prepared_timeline = self._prepare_timeline_for_insert(home_timeline)

        self.tweet_storage.insert(prepared_timeline)
        log = {'time': datetime.datetime.utcnow(),
               'entry': {'operation': 'write',
                         'number_tweets': str(len(prepared_timeline))}}

        self.log_storage.insert(log)

    def _prepare_timeline_for_insert(self,timeline):
        new_timeline = []
        for status in timeline:
            tweet = self._prepare_tweet_for_insert(status)

            new_timeline.append(d)
        return new_timeline

    def _prepare_tweet_for_insert(self,s):
        #mostly because mongo cannot accept field names with a '.' in them.
        # https://dev.twitter.com/overview/api/tweets is useful
        raw_tweet = s.AsDict()
        prepared_tweet = {}
        safe_fields = ['contributors',
                       'coordinates',
                       'created_at',
                       'current_user_retweet',
                       'favorite_count',
                       'favorited',
                       'filter_level'
                       'id_str',
                       'in_reply_to_screen_name',
                       'in_reply_to_status_id_str',
                       'in_reply_to_user_id_str',
                       'lang',
                       'place',
                       'possibly_sensitive',
                       'scopes',
                       'retweet_count',
                       'retweeted',
                       'retweeted_status',
                       'source',
                       'text',
                       # 'truncated', # From the docs: Since Twitter now rejects long Tweets vs truncating them, the large majority of Tweets will have this set to false.
                       'user',
                       'withheld_copyright',
                       'withheld_in_countries',
                       'withheld_scope'

                       #entities https://dev.twitter.com/overview/api/entities
                       'hashtags',
                       'media',
                       'user_mentions'
                       ]
        unsafe_fields = ['urls']
        for f in safe_fields:
            result = raw_tweet.get(f)
            if result:
                prepared_tweet[f] = result
        return prepared_tweet

        # possible ways to deal with the URLS:
            # replace the dot with something special e.g. LOUISHATESTWITTER
            # refactor from {u'short_url_1': 'long_url_1',
            #                  'short_url_2': 'long_url_2'}
            # to something like ((short_url_1,long_url_1'),
            #                    (short_url_2,long_url_2'))
            # unfortunately...twitter API does not seem to be consistent





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
        #TODO: use the timestamp from the ObjectIds
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


if __name__ == '__main__':
    main()
