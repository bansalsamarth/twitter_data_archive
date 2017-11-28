import MySQLdb, os

#Database Settings
HOST = os.environ['DB_HOST']
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']
DATABASE_NAME = os.environ['DB_DATABASE_NAME']

db = MySQLdb.connect(HOST,USER,PASSWORD,DATABASE_NAME)
cursor = db.cursor()

#Table Variables
TWEET_COLLECTION_TABLE = "all_tweets"
TWITTER_HANDLE_TABLE = "twitter_handles"
TWEET_LOG_TABLE = "collection_log"
