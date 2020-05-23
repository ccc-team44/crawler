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
	"""
	If the coordinates field is populated, the values there will be tested against the bounding box. Note that this field uses geoJSON order (longitude, latitude).
	If coordinates is empty but place is populated, the region defined in place is checked for intersection against the locations bounding box. Any overlap will match.
	If none of the rules listed above match, the Tweet does not match the location query. Note that the geo field is deprecated, and ignored by the streaming API.
	"""
	listener = StreamListener()
	stream = Stream(listener.auth, listener)
	while True:
		try:
			stream.filter(locations=config.au_bounds)
		except tweepy.RateLimitError as e:
			print("stream RateLimitError error", e)
			time.sleep(15 * 60) # anti block
		except Exception as e:
			print("non rate related", e)


def init():
	db_user = os.environ['DATABASE_USER']
	db_password = os.environ['DATABASE_PASSWORD']
	db_host = os.environ['DATABASE_HOST']
	db_port = os.environ['DATABASE_PORT']
	node_index = int(os.environ['NODE_INDEX'])
	
	print(f"i'm node {node_index}")
	
	server_address = f"http://{db_user}:{db_password}@{db_host}:{db_port}"
	
	StreamListener.auth = tweepy.OAuthHandler(config.consumer_key[node_index], config.consumer_secret[node_index])
	StreamListener.auth.set_access_token(config.access_token[node_index], config.access_token_secret[node_index])
	StreamListener.api = tweepy.API(StreamListener.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
	keep_trying = True
	
	while keep_trying:
		try:
			limit = StreamListener.api.rate_limit_status()
			print("timeline",limit["resources"]["statuses"]["/statuses/user_timeline"])
			keep_trying = False
		except Exception as e:
			print(e)
			time.sleep(15) # just in case twitter blocks our account
	try:
		couch_server = pycouchdb.Server(server_address, authmethod="basic")
		couch = Couch()
		couch.server = couch_server
		StreamListener.couch = couch
	except Exception as e:
		print("unable connecting to DB", e)
		sys.exit(0)
	start_streaming()


def main():
	init()
	print("the end")


if __name__ == '__main__':
	main()
