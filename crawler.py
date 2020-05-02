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


def parse_cli(argv):
	try:
		opts, args = getopt.getopt(argv, "i:h:p")
	except getopt.GetoptError as error:
		print(error)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-i':
			node_index = int(arg)
	return node_index


def start_streaming():
	listener = StreamListener()
	stream = Stream(listener.auth, listener)
	run = True
	while run:
		try:
			stream.filter(locations=config.au_bounds)
		except Exception as e:
			print ("stream error", str(e))
			time.sleep(10)
			run = True
		else:
			print(1)
			run = False

def main(argv):
	node_index = parse_cli(argv)
	print(f"i'm node {node_index}")
	
	db_user = os.environ['DATABASE_USER']
	db_password = os.environ['DATABASE_PASSWORD']
	db_host = os.environ['DATABASE_HOST']
	db_port = os.environ['DATABASE_PORT']
	
	server_address = f"http://{db_user}:{db_password}@{db_host}:{db_port}"
	
	StreamListener.auth = tweepy.OAuthHandler(config.consumer_key[node_index], config.consumer_secret[node_index])
	StreamListener.auth.set_access_token(config.access_token[node_index], config.access_token_secret[node_index])
	StreamListener.api = tweepy.API(StreamListener.auth, wait_on_rate_limit=True)
	
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
	main(sys.argv[1:])
