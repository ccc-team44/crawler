import getopt
import os
import sys

import pycouchdb
from tweepy import Stream

from Couch import Couch
from StreamListener import StreamListener
import config
import tweepy
import time


def start_streaming():
	listener = StreamListener()
	stream = Stream(listener.auth, listener)
	run = True
	while run:
		try:
			stream.filter(locations=config.au_bounds)
		except tweepy.RateLimitError as e:
			print("stream RateLimitError error", str(e))
			time.sleep(15 * 60)
			run = True
		except Exception as e:
			print("non rate related", str(e))
			time.sleep(15 * 60)
			run = True
		else:
			print('streaming Stopping')
			run = False


def main():
	db_user = os.environ['DATABASE_USER']
	db_password = os.environ['DATABASE_PASSWORD']
	db_host = os.environ['DATABASE_HOST']
	db_port = os.environ['DATABASE_PORT']
	node_index = int(os.environ['NODE_INDEX'])
	
	print(f"i'm node {node_index}")
	
	server_address = f"http://{db_user}:{db_password}@{db_host}:{db_port}"
	
	StreamListener.auth = tweepy.OAuthHandler(config.consumer_key[node_index], config.consumer_secret[node_index])
	StreamListener.auth.set_access_token(config.access_token[node_index], config.access_token_secret[node_index])
	StreamListener.api = tweepy.API(StreamListener.auth, wait_on_rate_limit=True)
	
	keep_trying = True
	
	while keep_trying:
		try:
			limit = StreamListener.api.rate_limit_status()
			print(limit)
			keep_trying = False
		except Exception as e:
			print(e)
			time.sleep(15)
	try:
		couch_server = pycouchdb.Server(server_address, authmethod="basic")
		couch = Couch()
		couch.server = couch_server
		StreamListener.couch = couch
	except Exception as e:
		print("unable connecting to DB", e)
		sys.exit(0)
	start_streaming()


if __name__ == '__main__':
	main()
