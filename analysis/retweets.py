import csv
import re
from collections import Counter

def read_csv_to_list(filename):
    data = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

tweets = read_csv_to_list('kejriwal.csv')


def get_retweet_count(tweets, count):
    import re
    from collections import Counter

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
