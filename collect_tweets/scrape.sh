#!/bin/bash
echo "Archiving Tweets..."
python upload_handles.py twitter_handles.csv
python run_scraper.py