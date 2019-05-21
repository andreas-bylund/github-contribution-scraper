import json
import requests
import time
from db import db

#Path to sqlite3 database
sqlite3_db_path = "database"

#Connect/Create database
conn = db.create_connection(sqlite3_db_path)

#Create the tables if they don't exists
db.create_tables(conn)

users_to_crawl = [
	'a17xxxxx',
	'a17xxxxx',
	'a17xxxxx'
]

#Global variables
already_scanned = False
user_to_scan = len(users_to_crawl)
user_scanned = 0

def coordinator():
	global already_scanned
	global user_to_scan
	global user_scanned

	for user in users_to_crawl:

		percent_left = user_scanned / user_to_scan * 100

		terminal_log("["+ user +"] ["+ str(user_scanned) + "/"+ str(user_to_scan) +" ] ("+ str(int(percent_left)) +"/100 %)")

		for x in range(1, 11):

			if already_scanned is True:
				terminal_log("\t[Scanned everything - Skipping the rest for saving API requests]")
				already_scanned = False
				break

			limit = get_api_rate_limit()

			if(limit['remaining'] == 0):
				sleep_time = limit['reset'] - int(time.time()) + 5
				sleep_time_min = sleep_time / 60
				terminal_log("Going to sleep for: " + str(sleep_time) + " seconds. (" + str(sleep_time_min) +" min)")
				time.sleep(sleep_time)

			terminal_log("\tStarting to fetch: " + user + " and page: " + str(x) + " API requests left: " + str(limit['remaining']))

			user_data_raw = requests.get(
				'https://api.github.com/users/' + user + '/events?page=' + str(x)
			)

			json_data = user_data_raw.json()
			parse_response_data(json_data)

			## Sleep so we don't spam the Github API
			time.sleep(3)

		user_scanned += 1

## Simple function that prints information to the terminal
def terminal_log(msg):
	print(msg)

## Get API limitation data
def get_api_rate_limit():
	response = requests.get('https://api.github.com/rate_limit')

	json_data = response.json()

	return json_data['rate']

## Parse the reponse data
def parse_response_data(json_data):
	global already_scanned

	response = True

	for event in json_data:

		##Created a new comment
		if(event['type'] == "IssueCommentEvent" and event['payload']['action'] == "created"):
			task = [
				event['id'],
				event['actor']['login'],
				event['created_at'],
				event['payload']['comment']['html_url'],
				event['payload']['comment']['body']
			]
			response = db.insert_comment(conn, task)

		##Created a new pull request
		if(event['type'] == "PullRequestEvent" and event['payload']['action'] == "opened"):
			task = [
				event['id'],
				event['actor']['login'],
				event['payload']['pull_request']['title'],
				event['payload']['pull_request']['html_url'],
				event['payload']['pull_request']['commits'],
				event['payload']['pull_request']['additions'],
				event['payload']['pull_request']['deletions'],
				event['payload']['pull_request']['changed_files'],
				event['created_at']
			]
			response = db.insert_pull_requests(conn, task)

		##Created a new issueFetch the data from the
		if(event['type'] == "IssuesEvent" and event['payload']['action'] == "opened"):
			task = [
				event['id'],
				event['actor']['login'],
				event['payload']['issue']['title'],
				event['payload']['issue']['html_url'],
				event['payload']['issue']['body'],
				event['created_at']
			]
			response = db.insert_issue(conn, task)

		##Push event, Triggered on a push to a repository branch
		if(event['type'] == "PushEvent"):
			task = [
				event['id'],
				event['actor']['login'],
				event['payload']['size'], #Number of commits in that push event
				event['created_at']
			]
			response = db.insert_push(conn, task)

		#Branches created
		if(event['type'] == "CreateEvent" and event['payload']['ref_type']):
			task = [
				event['id'],
				event['actor']['login'],
				event['created_at'],
				event['payload']['ref']
			]
			response = db.insert_branch(conn, task)

		if response is False:
			already_scanned = True
			break

## Start the script
coordinator()
