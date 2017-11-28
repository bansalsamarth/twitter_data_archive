from twitter_settings import *
import time

from save_db import *
from get_tweets import *

from datetime import datetime
from pytz import timezone    

def get_time():
	india = timezone('Asia/Kolkata')
	ind_time = datetime.now(india)
	return ind_time.strftime('%Y-%m-%d %H:%M:%S')

#returns list of all Twitter handles in the database
def get_handles(table_name):
	sql = "SELECT handle_name from {0};".format(table_name)
	cursor.execute(sql)
	accounts = [i[0] for i in cursor.fetchall()]
	return accounts

#extracts values from tweet objects and saves to database
#TODO: store the entre object in NoSQL database
def save_tweet_to_db(tweet, table_name):
	try:
		sql = """INSERT INTO {0} (handle_name, tweet_id, text, source, in_reply_to_screen_name,created_at,language) VALUES ("{1}", "{2}", "{3}","{4}", "{5}", "{6}", "{7}") ON DUPLICATE KEY UPDATE tweet_id=tweet_id;""".format(table_name, tweet.author.screen_name, tweet.id_str, MySQLdb.escape_string(tweet.text.encode("utf-8")), tweet.source, tweet.in_reply_to_screen_name, tweet.created_at, tweet.lang)
		cursor.execute(sql)
		db.commit()
		return 1
	except: 
		#TODO: what if the database transaction fails?
		log_entry(tweet.author.screen_name, "FAILED", 0, "", str(sys.exc_info()[0]))
		return 0

def collect_tweet_metadata(tweets):
	for tweet in tweets:
		save = save_tweet_to_db(tweet, "all_tweets")
	return 1

def log_entry(handle_name, status, tweets_fetched, oldest_tweet_id, error):
	time = get_time()

	#TODO: log errors here
 	sql = """INSERT INTO {0} (handle_name, time, status, tweets_fetched, oldest_tweet_id, error) VALUES ("{1}", "{2}", "{3}","{4}", "{5}", "{6}")""".format(TWEET_LOG_TABLE, handle_name, time, status, tweets_fetched, oldest_tweet_id, error)
 	print sql
	cursor.execute(sql)
	db.commit()

	return 1
