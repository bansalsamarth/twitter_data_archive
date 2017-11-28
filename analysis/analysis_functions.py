#Pre Processing Tweets
from nltk.tokenize import word_tokenize
import re

#Stop Words
from nltk.corpus import stopwords
import string

#Term Frequency
import operator 
from collections import Counter

#bigrams
from nltk import bigrams 

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

def tokenize(s):
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']


def tweet_words_analytics(tweets):

    count_all_terms = Counter()
    count_all_hashtags = Counter()
    count_all_bigrams = Counter()
    count_all_retweets = Counter()
    
    tweet_count = 0
    tweet_error = []
    
    for tweet_set in tweets:
            try:
                #convert all tweets to lower case
                tweet = tweet_set.lower()

            except Exception, e:
                print tweet_set
                tweet_error.append(tweet)
                print e
                continue
            
            tweet_count+=1

            # Create a list with all the terms without stop words
            terms_stop = [term for term in preprocess(tweet) if term not in stop]
            
            #Hashtags
            terms_hash = [term for term in preprocess(tweet) if term.startswith('#')]

            #bigrams
            terms_bigram = bigrams(terms_stop)

            # Update the counter
            count_all_terms.update(terms_stop)
            count_all_hashtags.update(terms_hash)
            count_all_bigrams.update(terms_bigram)

    return count_all_terms, count_all_hashtags, count_all_bigrams


def get_retweet_count(tweets, count):
    retweet = []
    retweet_count = []
    regex = "^RT @(\w*)"

    for tweet in tweets:
    	if "RT @" in tweet:
                
                match = re.match(regex, tweet.strip())
                try:
                    retweet.append(match.group(1))
                except:
                    continue

    number_of_retweets = Counter(retweet)
    for i in number_of_retweets.most_common(count):
        retweet_count.append([i[0], i[1]])
    return retweet_count
