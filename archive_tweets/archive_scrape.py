#Code adapted from: https://github.com/bpb27/twitter_scraping
import sys, os
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import json
import datetime

from twitter_settings import *

def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(twitter_handle, since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  twitter_handle + '%20since%3A' + since + '%20until%3A' + until# + ' include%3Aretweets&src=typd'
    return p1 + p2

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

def get_days_tweets(driver, delay):
    #parsing
    id_selector = '.time a.tweet-timestamp'
    tweet_selector = 'li.js-stream-item'
    ids = []

    try:
        found_tweets = driver.find_elements_by_css_selector(tweet_selector)
        increment = 10

        while len(found_tweets) >= increment:
            print('scrolling down to load more tweets')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(delay)
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            increment += 10

        print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))

        for tweet in found_tweets:
            try:
                id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                ids.append(id)
            except StaleElementReferenceException as e:
                print('lost element reference', tweet)

        return ids

    except NoSuchElementException:
        print('no tweets on this day')
        return ids


def fetch_twitter_archive_ids(twitter_handle, start, end):

    #total days for which tweets need to be scraped
    days = (end - start).days + 1
    ids = []

    #SCRAPER SETTINGS
    #CHECK: only edit these if you're having problems
    delay = 3  # time to wait on each page load before reading the page

    #run scraper for every day
    for day in range(days):

        d1 = format_day(increment_day(start, 0))
        d2 = format_day(increment_day(start, 1))

        url = form_url(twitter_handle, d1, d2)
        print url

        #fetch page
        driver.get(url)

        sleep(delay)

        #get tweets for the day
        day_ids = get_days_tweets(driver, delay)

        print d1, " done"
        start = increment_day(start, 1)

        directory = 'archive_ids/' + twitter_handle

        if not os.path.exists(directory):
            os.makedirs(directory)

        twitter_ids_filename_day = directory + '/' + twitter_handle + '_' + str(start.day) + '_' + str(start.month) + '_' + str(start.year) + '.txt'

        #out_file = open(twitter_ids_filename_day, 'w')

        print('tweets found on this scrape: ', len(ids))

        if len(day_ids)>0:
            #output_archive_ids(ids, twitter_ids_filename_day)
            with open(twitter_ids_filename_day, 'w') as out_file:
                for item in day_ids:
                    out_file.write("%s\n" % item)

    return ids

def output_archive_ids(ids, twitter_ids_filename):

    with open(twitter_ids_filename) as f:
            print ids
            all_ids = ids + json.load(f)
            data_to_write = list(set(all_ids))
            print('tweets found on this scrape: ', len(ids))
            print('total tweet count: ', len(data_to_write))

    with open(twitter_ids_filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

try:
    twitter_handle = sys.argv[1]
except:
    print "ERROR: twitter handle missing"
    print "USE THIS FORMAT: python " + sys.argv[0] + " <twitter_handle>"
    sys.exit()

driver = webdriver.Safari()  # options are Chrome() Firefox() Safari()

try:
    user_detail = api.get_user(twitter_handle)

    start_month = user_detail.created_at.month
    start_year = user_detail.created_at.year
    start_day = user_detail.created_at.day

    end_month = datetime.datetime.now().month
    end_year = datetime.datetime.now().year
    end_day = datetime.datetime.now().day

    #start scraping date
    start = datetime.datetime(start_year, start_month, start_day)  # year, month, day
    #last date of scraping
    end = datetime.datetime(end_year, end_month, end_day)  # year, month, day

except:
    print "ERROR: Getting account detail of ", twitter_handle
    sys.exit()

ids = fetch_twitter_archive_ids(twitter_handle, start, end)

print ids

print "COMPLETE: Process complete for ", twitter_handle

driver.close()
