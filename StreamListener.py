import json
import time

import tweepy

import config


class StreamListener(tweepy.StreamListener):
	au_bounds = config.au_bounds;
	# convert
	def convert(self, obj):
		
		id_str = obj['id_str']
		created_at = obj['created_at']
		screen_name = obj['user']['screen_name']
		try:
			text = obj['extended_tweet']['full_text']
		except Exception:
			text = obj['full_text'] if 'full_text' in obj else obj['text']
		
		db_data = {"_id": id_str, "created_at": created_at, "screen_name": screen_name, "text": text}
		return db_data
	
	# check tweet has coord
	def get_coords(self, obj):
		try:
			coords = obj["geo"]["coordinates"]
		except Exception:
			try:
				coords = ["coordinates"]["coordinates"]
			except Exception:
				coords = None
		return coords
	
	# once complete grabbing tweets from an user, mark user as done
	def should_skip_user(self, user_id):
		couch = StreamListener.couch
		db = couch.get_database(name="users")
		
		try:
			db.get(user_id)
		except:
			self.couch.saveUser({"_id": user_id})
			return False  # should keep digging
		else:
			return True  # should skip this user
	
	# Method to check if tweet is posted in Australia
	def is_au(self, obj):
		if obj["geo"] is not None:
			geo = obj["geo"]
			coord = geo["coordinates"]
			lat = float(coord[0])
			lng = float(coord[1])
			return self.au_bounds[3] >= lat >= self.au_bounds[1] and self.au_bounds[2] >= lng >= self.au_bounds[0]
		else:
			coord = obj["coordinates"]["coordinates"]
			lat = float(coord[0])
			lng = float(coord[1])
			return self.au_bounds[3] >= lng >= self.au_bounds[1] and self.au_bounds[2] >= lat >= self.au_bounds[0]
	
	def handle_tweet(self, obj):
		coordinates = self.get_coords(obj)
		if coordinates:
			if self.is_au(obj):
				db_data = self.convert(obj)
				# todo analyzer
				analysis = {}
				
				db_data["coordinates"] = coordinates
				self.couch.saveTweet(db_data)
			else:
				print("not in au")
		# else:
		# 	print("no coords")
	
	# Method used to return user's history tweets through api.user_timeline wrapped in tweepy.Cursor
	def get_user_tweets(self, user_id):
		run = True
		while run:
			try:
				tweets = tweepy.Cursor(StreamListener.api.user_timeline, user_id=user_id, tweet_mode="extended").items()
			except Exception:
				print("Cursor Issue.. Reconnecting")
				time.sleep(10)
				run = True
			else:
				run = False
		
		for tweet in tweets:
			tweet_json = tweet._json
			if tweet_json is None:
				print("This tweet is empty")
			else:
				print(type(tweet_json))
				json_str = json.dumps(tweet_json)
				self.handle_tweet(json_str)
	
	# When a streaming data comes in
	def on_data(self, raw_data):
		json_dict = json.loads(raw_data)
		self.handle_tweet(json_dict)
		user_id = json.loads(raw_data)["user"]["id_str"]
		if self.should_skip_user(user_id):
			print("skip thi user")
		else:
			print("start digging user tweet", user_id)
			self.get_user_tweets(user_id)
	
	# Error code
	def on_error(self, status_code):
		print(status_code)
