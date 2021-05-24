from twitter_credentials import API_KEY,API_SECRET_KEY,BEARER_TOKEN,ACCESS_TOKEN,ACCESS_TOKEN_SECRET

# Import other relevant libs
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
import datetime

#initialize polarity as empty list
polarity = []

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets



# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

        
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        # print(analysis.sentiment.polarity)

        return analysis.sentiment.polarity
    
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
        # Check if bitcoin is mentioned in any of the tweets
        crypto_mention = []
        for tweet in df['Tweets']:
            if ('bitcoin' or 'crypto' or 'doge') in tweet:
                crypto_mention.append(True)
            else:
                crypto_mention.append(False)

        df['crypto_mention'] = np.array(crypto_mention)

        return df


def get_elons_tweets():
    # Authenticate using config.py and connect to Twitter Streaming API.
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api() # Tweepy API

    # Aggregate tweets from relevant user accounts

    # Tesla DF
    tweets = api.user_timeline(screen_name='tesla', count=1)
    # tweets = twitter_client.get_user_timeline_tweets(10)
    tesla_df = tweet_analyzer.tweets_to_data_frame(tweets)
    tesla_df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in tesla_df['Tweets']])

    # Elon Musk DF
    tweets = api.user_timeline(screen_name='elonmusk', count=1)
    # tweets = twitter_client.get_user_timeline_tweets(10)
    elon_df = tweet_analyzer.tweets_to_data_frame(tweets)
    elon_df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in elon_df['Tweets']])

    # SpaceX DF
    tweets = api.user_timeline(screen_name='spacex', count=1)
    # tweets = twitter_client.get_user_timeline_tweets(10)
    SpaceX_df = tweet_analyzer.tweets_to_data_frame(tweets)
    SpaceX_df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in SpaceX_df['Tweets']])

    # Concat relevant DFs
    final_df = pd.concat([tesla_df,elon_df,SpaceX_df], axis=0)
    return final_df

if __name__ == "__main__":
    
    # Authenticate using config.py and connect to Twitter Streaming API.
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api() # Tweepy API

    # Aggregate tweets from relevant user accounts

    # Tesla DF
    tweets = api.user_timeline(screen_name='tesla', count=1)
    # tweets = twitter_client.get_user_timeline_tweets(10)
    tesla_df = tweet_analyzer.tweets_to_data_frame(tweets)
    tesla_df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in tesla_df['Tweets']])

    # Elon Musk DF
    tweets = api.user_timeline(screen_name='elonmusk', count=1)
    # tweets = twitter_client.get_user_timeline_tweets(10)
    elon_df = tweet_analyzer.tweets_to_data_frame(tweets)
    elon_df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in elon_df['Tweets']])

    # SpaceX DF
    tweets = api.user_timeline(screen_name='spacex', count=1)
    # tweets = twitter_client.get_user_timeline_tweets(10)
    SpaceX_df = tweet_analyzer.tweets_to_data_frame(tweets)
    SpaceX_df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in SpaceX_df['Tweets']])

    # Concat relevant DFs
    final_df = pd.concat([tesla_df,elon_df,SpaceX_df], axis=0)

    print(final_df)