/*
	RUN mysql -u root -p < db_prep.sql
*/

CREATE DATABASE twitter_data;
USE twitter_data;

CREATE TABLE all_tweets(
	handle_name VARCHAR (100),
	tweet_id VARCHAR (20) UNIQUE,
	text TEXT,
	source VARCHAR (300),
	in_reply_to_screen_name VARCHAR (200),
	created_at VARCHAR (100),
	language VARCHAR (20)
);


CREATE TABLE twitter_handles(
	handle_name VARCHAR(100),
	name VARCHAR (250),
	PRIMARY KEY(handle_name)
);

CREATE TABLE collection_log(
	handle_name VARCHAR (100),
	time VARCHAR (100),
	status VARCHAR (100),
	tweets_fetched INT,
	oldest_tweet_id VARCHAR (20),
	error VARCHAR (200)
);

CREATE TABLE followers_track(
	handle_name VARCHAR (100),
	time VARCHAR (100),
	follower_count INT,
	following_count INT,
	fav_count INT,
	latest_tweet_id VARCHAR (20),
	total_tweets INT
);

CREATE TABLE archive_tweet_ids(
	handle_name VARCHAR (100),
	time VARCHAR (100),
	tweet_id VARCHAR (20) UNIQUE
);
