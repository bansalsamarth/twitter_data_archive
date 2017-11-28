import tweepy, os

#Twitter API credentials
consumer_key =  os.environ['TWITTER_CONSUMER_KEY']
consumer_secret =  os.environ['TWITTER_CONSUMER_SECRET']
access_key =  os.environ['TWITTER_ACCESS_KEY']
access_secret =  os.environ['TWITTER_ACCESS_SECRET']

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
