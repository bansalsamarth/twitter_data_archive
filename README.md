# Twitter Archive of Indian Politicians

##### Why collect Twitter Data for Politicians?
* Twitter—a tool for political messaging and framing online narratives
* Twitter API has returns the latest 3200 tweets only
* No comprehensive dataset of tweets of Indian politicians to study aggregate patterns
* Resource for data scientists



#### collect_tweets
` twitter_handles.csv` List of handles to track
` get_tweets.py`Code to collect tweets of a specific handle
` run_scraper.py` Code to collect tweets of all politicians in the list. Runs once every day. 
 #### cabinet_ministers
`scrape.py` Script to scrape the list of cabinet ministers in the Government of India. Fetches name, twitter handle, facebook username and contact of ministers
#### archive_tweets 
`archive_scrape.py` Script to fetch tweets using Twitter's search interface. Gets all tweets for a particular day. Doesn't get retweets. 
#### analysis
`analysis.py` Collection of basic text analytics functions to analyse tweets data

### Status
The system is deployed on Google Cloud Platform and is collecting tweets of all politicians listed in  `twitter_handles.csv`

**Under development:** Frontend tool for automated analytics. Will be launched in March 2018. 

**Want to contribute?** Drop me an email `samarthbansal42@gmail.com`







