import csv
import re
import requests

from collections import Counter

def read_csv_to_list(filename):
    data = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

tweets = read_csv_to_list('kejriwal.csv')
regex = "(https:\/\/.[^\s]+)|(http:\/\/.[^\s]+)"

links = []


print len(links)

urls = []

for i in links:
	try:
		#i = "https://t.co/to647ZzR8Z"
		a = requests.get(i)
		urls.append(a.url)
		print a.url
	except:
		pass

print urls