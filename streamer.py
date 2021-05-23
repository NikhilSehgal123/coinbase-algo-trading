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

    def stream_tweets(self, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener()
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)
        print(polarity)
        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)

# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self):
        self.polarity = []

    def on_data(self, data):
        try:
            print(data)
            y = json.loads(data)
            text = y["text"]
            polarity = analyze_sentiment(text)
            self.polarity.append(polarity)
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)
        
    def get_average_polarity(self):
        #print(np.mean(self.polarity))
        return np.mean(self.polarity)

# Additional function for cleaning tweets
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# Additional function for analyzing the sentiment of a tweet
def analyze_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    polarity.append(analysis.sentiment.polarity)
    print('Average Polarity = %s'%(np.mean(polarity)))
    np.savetxt('current_polarity_array.txt', polarity)
    return analysis.sentiment.polarity

if __name__ == "__main__":
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["bitcoin"]
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list)