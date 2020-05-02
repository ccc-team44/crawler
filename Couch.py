import json

import pycouchdb


class Couch():
	tweet_database_name = "tweets"
	users_database_name = "users"
	
	def get_database(self, name):
		try:
			database = self.server.database(name)
			return database
		except:
			print("Creating database",  name)
			self.server.create(name)
			return self.server.database(name)
	
	# save tweet to database
	def saveTweet(self, data):
		db = self.get_database(name=self.tweet_database_name)
		try:
			db.save(data)
		except:
			print("exists")
		else:
			print("tweet saved")
	
	# save user to database
	def saveUser(self, data):
		db = self.get_database(name=self.users_database_name)
		try:
			db.save(data)
		except:
			print("exists")
		else:
			print("user saved")
