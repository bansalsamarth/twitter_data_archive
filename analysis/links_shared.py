import re, csv
import requests

#regex = "(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])"
regex = "([a-z]+[:.].*?(?=\s))"

def read_csv_to_list(filename):
    data = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

tweets = read_csv_to_list('kejriwal.csv')

links = []

for tweet in tweets:
	if 'http' in tweet:
		print tweet
		match = re.match(regex, tweet)
		print match
		raw_input()
	#link.append(match.group(1))
