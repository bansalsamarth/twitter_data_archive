from twitter_settings import *
import time

from save_db import *
from get_tweets import *

print "imported"
from functions import *

if __name__ == '__main__':
	#get list of handles from the database
	accounts = get_handles(TWITTER_HANDLE_TABLE)
	#accounts = ['ArvindKejriwal']

	for account in accounts:
		print "Fetching latest tweets for ", account
		oldest_tweet_id = ""
		tweets = []

		try:
			#collect latest tweets (max limit: 3200)
			tweets, oldest_tweet_id, process = get_all_tweets(account, TWEET_COLLECTION_TABLE)

			#tweet fetching process successful. add to log
			if process=="success":

				#collect metadata and store tweet in database
				print "collecting metadata for ", account
				collect_tweet_metadata(tweets)

				#all operations succeed
				status = "SUCCESS"
				log_entry(account, status, len(tweets), oldest_tweet_id, "")

			#tweet fetching process failed. log entry created. 
			else:
				continue

		except Exception, e:
			status = "FAILED"
			#TODO: Log the error
			log_entry(account, status, len(tweets), oldest_tweet_id, sys.exc_info()[0])
		
		#Wait for 10s. To ensure Twitter's rate limit is not exceeded
		print "Process complete for {0}. Sleeping for 10s".format(account)
		time.sleep(10)
