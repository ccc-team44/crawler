import json

import tweepy


class Couch():
	tweet_database_name = "tweets"
	users_database_name = "users"

	def get_database(self, name):
		try:
			database = self.database(name)
			return database
		except:
			print("Creating database",  name)
			self.create(name)
			return self.database(name)
	
	# save tweet to database
	def saveTweet(self, data, db_name):
		db = self.get_database(self, self.tweet_database_name)
		try:
			db.save(data)
		except:
			print("exists")
		else:
			print("tweet saved")
			
	# save user to database
	def saveTweet(self, data, db_name):
		db = self.get_database(self, self.users_database_name)
		try:
			db.save(data)
		except:
			print("exists")
		else:
			print("user saved")
	
	
	# Method using user_id to check if this user's tweets have already been returned
	# through interaction with couchDB. If the user hasn't been returned, then return
	# True and save user_id in database.
	def is_user_tweet_already_returned(self, user_id):
		server = StdOutStreamListener.server
		print(server)
		try:
			database = server.database("userid_db")
		except:
			print("no such DB remotely..creating DB:" + "userid_db")
			database = server.create("userid_db")
			database = server.database("userid_db")
		try:
			database.get(user_id)
		except:
			database.save({"_id": user_id})
			return False
		else:
			return True
	
	# Method to check if tweet is posted in Australia
	def is_in_australia(self, tweet):
		tweet_json = json.loads(tweet)
		if tweet_json["geo"] is not None:
			if float(tweet_json["geo"]["coordinates"][0]) <= config.locations_australia[3] and float(
				tweet_json["geo"]["coordinates"][0]) >= config.locations_australia[1] and float(
				tweet_json["geo"]["coordinates"][1]) <= config.locations_australia[2] and float(
				tweet_json["geo"]["coordinates"][1]) >= config.locations_australia[0]:
				return True
			else:
				return False
		else:
			if float(tweet_json["coordinates"]["coordinates"][1]) <= config.locations_australia[3] and float(
				tweet_json["coordinates"]["coordinates"][1]) >= config.locations_australia[1] and float(
				tweet_json["coordinates"]["coordinates"][0]) <= config.locations_australia[2] and float(
				tweet_json["coordinates"]["coordinates"][0]) >= config.locations_australia[0]:
				return True
			else:
				return False
	
	# Method used to return user's history tweets through api.user_timeline wrapped in tweepy.Cursor
	def return_user_tweet(self, user_id):
		isFailed = True
		while isFailed:
			try:
				tweets = tweepy.Cursor(StdOutStreamListener.api.user_timeline, user_id=user_id,
									   tweet_mode="extended").items()
			except Exception:
				print("Cursor Issue.. Reconnecting")
				time.sleep(10)
				isFailed = True
			else:
				isFailed = False
		
		for tweet in tweets:
			tweet_json = tweet._json
			if tweet_json is None:
				print("This tweet is empty")
			else:
				coordinates = self.has_coordinates(json.dumps(tweet_json))
				if coordinates:
					print("This tweet has point coordinates!!!!")
					if self.is_in_australia(json.dumps(tweet_json)):
						print("This tweet is in Australia!!!!")
						db_data = self.generate_db_data(json.dumps(tweet_json))
						analysis_result = analyser.sin_analyse(db_data["text"])
						db_data["coordinates"] = coordinates
						if analysis_result:
							db_data["sin"] = analysis_result["sin"]
							db_data["sentiment"] = analysis_result["sentiment"]
							self.save2db(db_data)
					else:
						print("This tweet is not in Australia!!!!")
						print(tweet_json["geo"])
						print(tweet_json["coordinates"])
				else:
					print("This tweet has no point coordinates")
	
	# When a streaming data comes in
	def on_data(self, raw_data):
		coordinates = self.has_coordinates(raw_data)
		if coordinates:
			print("This tweet has point coordinates!!!!")
			db_data = self.generate_db_data(raw_data)
			db_data["coordinates"] = coordinates
			analysis_result = analyser.sin_analyse(db_data["text"])
			if analysis_result:
				db_data["sin"] = analysis_result["sin"]
				db_data["sentiment"] = analysis_result["sentiment"]
				self.save2db(db_data)
		user_id = json.loads(raw_data)["user"]["id_str"]
		if self.is_user_tweet_already_returned(user_id):
			print("user's tweets have been returned.")
		else:
			print("User history tweets harvesting has started...", "=" * 20)
			self.return_user_tweet(user_id)
	
	# Error code
	def on_error(self, status_code):
		print(status_code)
