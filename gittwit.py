#!/usr/bin/env python

import oauth2
import json
import csv

API_KEY = "RfcPJR2anHGaGneui86hYopVv"
API_SECRET = "gsrJHRTNTMhvQ6KVNs1uKHfLL8RvUuRpBQLJ8E4dozjnmwoH94"
TOKEN_KEY = "1673966274-lmyX90buRhFOTuHah9B6iRih5I6KKcSsIbynoaN"
TOKEN_SECRET = "ros0ByXaiifC3ZXH8KyvegTWKkzSoWw1hZNmnIBtiaIfh"

def  oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
	consumer =oauth2.Consumer(key=API_KEY, secret=API_SECRET)
	token = oauth2.Token(key=key, secret=secret)
	client = oauth2.Client(consumer,token)
	resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
	return content

excel_name = raw_input("Please enter a name for your csv file: ") + ".csv"	
sinceid = raw_input("Please enter an id: ")
csv_out = open(excel_name, 'w') #opens csv file
writer = csv.writer(csv_out) #create the csv writer object
fields = ['created_at', 'id', 'text', 'screen_name', 'followers', 'friends', 'rt', 'fav'] #field names
writer.writerow(fields) #writes field


def get_data(since):
	if since < 602000800000000000:
		return ""

	else:
		url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=mint&exclude_replies=true&count=199&max_id="
		data = oauth_req(url+str(since), TOKEN_KEY, TOKEN_SECRET)

		data=json.loads(data)

		csv_out = open(excel_name, 'r') #read csv

		for line in data:
			#writes a row and gets the fields from the json object
			#screen_name and followers/friends are found on the second level hence two get methods
			writer.writerow([line.get('created_at'),
							 line.get('id'),
							 line.get('text').encode('unicode_escape'), #unicode escape to fix emoji issue
							 line.get('user').get('screen_name'),
							 line.get('user').get('followers_count'),
							 line.get('user').get('friends_count'),
							 line.get('retweet_count'),
							 line.get('favorite_count')])
		last_id = line.get('id')	
		print(last_id)
		print("\n")
		
		csv_out.close()
		get_data(last_id)
		
	
get_data(sinceid)