from twitter_settings import *
from save_db import *
from functions import get_time
FOLLOWER_TABLE = "followers_track"

def save_follower_data(handle, data):
	time = get_time()

	follower_count = data[0]
	following_count = data[1]
	fav_count = data[2]
	latest_tweet_id = data[3]
	total_tweets = data[4]

	sql = """INSERT INTO {0} (handle_name, time, follower_count, following_count,fav_count,latest_tweet_id,total_tweets ) VALUES ("{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}")""".format(FOLLOWER_TABLE,handle, time, follower_count, following_count,fav_count,latest_tweet_id,total_tweets)
	print sql
	cursor.execute(sql)
	db.commit()


def get_data(account):
	user = api.get_user(account)

	follower_count = user.followers_count
	following_count = user.friends_count
	fav_count = user.favourites_count
	latest_tweet_id = user.status.id
	total_tweets = user.statuses_count

	return [follower_count, following_count, fav_count, latest_tweet_id, total_tweets]

accounts = ['officeofrg', 'arvindkejriwal', 'narendramodi']

for account in accounts:
	data = get_data(account)
	save_follower_data(account, data)
	print data
