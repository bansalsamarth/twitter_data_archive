import csv, codecs

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
 
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    #sv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def read_csv_to_list(filename):
    data = []
    with open(filename, 'rb') as f:
        #reader = csv.reader(f)
        reader = unicode_csv_reader(codecs.open(filename, 'rb', 'utf-8'))
        for row in reader:
            data.append(row)
        return data

def output_to_csv(data, filename):
    with open(filename, "wb") as f:
                writer = csv.writer(f)
                writer.writerows(data)

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

count_all_terms = Counter()
count_all_hashtags = Counter()
count_all_bigrams = Counter()
count_all_retweets = Counter()

print "Reading Data..."

twitter_tata = read_csv_to_list('tweets.csv')

print "Data read..", len(twitter_data)

complete_data = []

#Data Cleaning (tweets.csv is already clean)
#Remove rows with header data from individual files ["id", "created_at"]
#Also remove rows which have less than 5 columns
for i in twitter_data:
    try:
        if i[2]=='id' or len(i)!=5:
            print i
            continue
        else:
            i[-1] = i[-1].encode("utf-8")
            complete_data.append(i)
    except Exception,e:
        print i,e

tweet_error = []
tweet_count = 0

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
            print tweet_count

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

print "Error for: ", len(tweet_error)

output_to_csv(count_all_bigrams.most_common(1000), "bigrams_1000.csv")
output_to_csv(count_all_terms.most_common(1000), "terms_1000.csv")
output_to_csv(count_all_hashtags.most_common(1000), "hashtags_1000.csv")
