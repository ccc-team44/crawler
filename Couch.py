import json

import tweepy


class Couch():
	database_name = "tweets_db"
	
	def get_database(self, name):
		try:
			database = self.server.database(self.database_name)
			return database
		except:
			print("no such DB remotely..creating DB:" + self.database_name)
			self.server.create(self.database_name)
			return self.server.database(self.database_name)
	
	# save data to database
	def save(self, data):
		db = self.get_database(self, self.database_name)
		try:
			db.save(data)
		except:
			print("exists")
		else:
			print("saved")
	
	# convert
	def convert(self, raw):
		
		obj = json.loads(raw)
		
		id_str = obj['id_str']
		created_at = obj['created_at']
		screen_name = obj['user']['screen_name']
		text = ['extended_tweet'] if 'extended_tweet' in obj else (
			obj['full_text'] if 'full_text' in obj else obj['text'])
		
		db_data = {"_id": id_str, "created_at": created_at, "screen_name": screen_name, "text": text}
		return db_data
	
	
