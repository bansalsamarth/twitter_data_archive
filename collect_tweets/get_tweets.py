#Note: get_all_tweets takes handle as the input and returns the list of latest 3200 Tweet objects
import csv
import logging, time, sys

from twitter_settings import *
from save_db import *
from functions import *

# Check if a tweet with tweet_id exists in the database. 
# Returns 1 if tweet exists, 0 if not. 
def tweet_exists_in_database(tweet_id, table_name):
	sql = "SELECT COUNT(*) FROM {0} WHERE tweet_id='{1}';".format(table_name, tweet_id)
	cursor.execute(sql)

	return cursor.fetchone()[0]

#screen_name: Twitter handle 
#table_name: table in the database where tweets are stored
def get_all_tweets(screen_name, table_name):
	
	#initialize a list to store Tweet objects
	alltweets = []

	#Make initial request for most recent tweets (200 is the maximum allowed count)
	try:
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		print "...%s tweets downloaded so far" % (len(alltweets))

		#if the oldest tweet returned exists in the database, no more calls to be made. Return the tweets set. 
		if tweet_exists_in_database(alltweets[-1].id_str, table_name):
			print "...Tweet with ID %s exists in %s. Not fetching older tweets. %s tweets fetched." % (alltweets[-1].id_str, table_name, len(alltweets))
			return alltweets, oldest, "success"
		
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0 :
			print "getting tweets before %s" % (oldest)

			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
			#save most recent tweets
			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			print "...%s tweets downloaded so far" % (len(alltweets))

			#if the oldest tweet returned exists in the database, no more calls to be made. Return the tweets set.
			if tweet_exists_in_database(alltweets[-1].id_str, table_name):
				print "...Tweet with ID %s exists in %s. Not fetching older tweets. %s tweets fetched." % (alltweets[-1].id_str, table_name, len(alltweets))
				return alltweets, oldest, "success"

		return alltweets, oldest, "success"

	except Exception as e:
		#print e
		log_entry(screen_name, "FAILED", len(alltweets), "", sys.exc_info()[0])
		
		logging.exception("{0} : {1}".format(screen_name, get_time()))

		return [], "", "failed"
		
		"""
		err = e.args[0][0]['message']
		if err=="Sorry, that page does not exist." or err=="Not authorized.":

		if e=="Not authorized.":
			dont_exist.append(screen_name)
			with open("dontexist.csv", 'wb') as f:
				writer = csv.writer(f)
				writer.writerow(["%s" % screen_name])
		"""