#USAGE: python update_handles.py file_with_handles.csv
#file_with_handles.csv should have two columns:twitter handle, name

import csv
import sys

from save_db import *

def read_csv_to_list(filename):
    data = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

if __name__ == '__main__':
	#csv file name taken as command line argument
	handle_file_name = sys.argv[-1]

	#read the file and store all values in a list
	handle_list = read_csv_to_list(handle_file_name)

	for handle in handle_list:
		#Insert handle in the table if it doesn't already exist
		sql="""INSERT INTO {0} (handle_name, name) VALUES ("{1}", "{2}") ON DUPLICATE KEY UPDATE name = "{2}";""".format(TWITTER_HANDLE_TABLE, handle[0], handle[1])
		cursor.execute(sql)
		db.commit()