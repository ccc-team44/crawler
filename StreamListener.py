import json
import time

import tweepy

au_bounds = [110.390625, -44.276671273775165,155.56640625, -11.005904459659451]
class StreamListener(tweepy.StreamListener):
	user_name_list = []
	database_name = "tweets_db"
	
	# convert
	def convert(self, raw):
		
		obj = json.loads(raw)
		
		id_str = obj['id_str']
		created_at = obj['created_at']
		screen_name = obj['user']['screen_name']
		try:
			text = obj['extended_tweet']['full_text']
		except KeyError:
			text = obj['full_text'] if 'full_text' in obj else obj['text']
		
		db_data = {"_id": id_str, "created_at": created_at, "screen_name": screen_name, "text": text}
		return db_data
	
	# check tweet has coord
	def get_coords(self, raw):
		obj = json.loads(raw)
		
		try:
			coords = obj["geo"]["coordinates"]
		except KeyError:
			try:
				coords = ["coordinates"]["coordinates"]
			except KeyError:
				coords = None
		return coords
	
	# once complete grabbing tweets from an user, mark user as done
	def should_skip_user(self, user_id):
		couch = StreamListener.couch
		
		db = couch.get_database("users")
		
		try:
			db.get(user_id)
		except:
			db.save({"_id": user_id})
			return False  # should keep digging
		else:
			return True  # should skip this user
	
	# Method to check if tweet is posted in Australia
	def is_au(self, raw):
		obj = json.loads(raw)
		if obj["geo"] is not None:
			geo = obj["geo"]
			coord = geo["coordinates"]
			lat = float(coord[0])
			lng = float(coord[1])
			return au_bounds[3] >= lat >= au_bounds[1] and au_bounds[2] >= lng >= au_bounds[0]
		else:
			coord = obj["coordinates"]["coordinates"]
			lat = float(coord[0])
			lng = float(coord[1])
			return au_bounds[3] >= lng >= au_bounds[1] and au_bounds[2] >= lat >= au_bounds[0]
	
	def handle_tweet(self, json_str):
		
		coordinates = self.get_coords(json_str)
		if coordinates:
			if self.is_au(json_str):
				db_data = self.convert(json)
				
				# todo analyzer
				analysis = {}
				
				db_data["coordinates"] = coordinates
				self.couch.save(db_data)
			else:
				print("not in au")
		else:
			print("no coords")
	
	# Method used to return user's history tweets through api.user_timeline wrapped in tweepy.Cursor
	def get_user_tweets(self, user_id):
		run = True
		while run:
			try:
				tweets = tweepy.Cursor(StreamListener.api.user_timeline, user_id=user_id,
									   tweet_mode="extended").items()
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
				json_str = json.dumps(tweet_json)
				self.handle_tweet(json_str)
	
	# When a streaming data comes in
	def on_data(self, raw_data):
		self.handle_tweet(raw_data)
		user_id = json.loads(raw_data)["user"]["id_str"]
		if self.should_skip_user(user_id):
			print("skip thi user")
		else:
			print("start digging user tweet", user_id)
			self.get_user_tweets(user_id)
	
	# Error code
	def on_error(self, status_code):
		print(status_code)
