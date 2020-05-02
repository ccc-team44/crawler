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
