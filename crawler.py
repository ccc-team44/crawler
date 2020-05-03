from config import api_launch
import tweepy
import time
import couchdb
import json


def crawl(num_api,
		  places_name,
		  host,
		  query="*",
		  lang="en",
		  count=100,
		  result_type="recent",
		  geocode=None,
		  max_id=None,
		  since_id=None,
		  tweet_mode="extended",
		  rate_limit=180,
		  wall_time=900,
		  log=None):
	if num_api != len(places_name):
		print("error")
		return (None)
	
	# connect to database
	couch = couchdb.Server(host)
	print("db connect success")
	
	api_id = 0
	api = api_launch(api_id)
	
	places_id = []
	for name in places_name:
		if name.lower() not in couch:
			couch.create(name.lower())
		for geo in api.geo_search(query=name, granularity="city"):
			places_id.append(geo.id)
			break
	
	if log == None:
		max_id_list = [None] * num_api
		start_id_list = [None] * num_api
		reset_time_list = [-1] * num_api
		total_tweet_count = [0] * num_api
		hit_bottom_list = [True] * num_api
	else:
		max_id_list = log["max_id_list"]
		start_id_list = log["start_id_list"]
		reset_time_list = log["reset_time_list"]
		total_tweet_count = log["total_tweet_count"]
		hit_bottom_list = log["hit_bottom_list"]
	
	while True:
		
		try:
			
			if max_id_list[api_id] == None:
				first_tweet = True
				
				# for test only
				
				print("*" * 10, api_id, "starts running", "*" * 10)
				
				for tweet in tweepy.Cursor(api.search, q="place:%s" % places_id[api_id], lang=lang, count=count,
										   max_id=max_id, result_type=result_type, tweet_mode=tweet_mode).items():
					if first_tweet:
						start_id_list[api_id] = tweet.id
						first_tweet = False
					
					total_tweet_count[api_id] += 1
					
					# output to db
					couch[places_name[api_id].lower()].save(tweet._json)
				
				# if search out all the tweet
				hit_bottom_list[api_id] = False
				raise tweepy.error.TweepError("Hit the bottom")
			
			else:
				# search head
				
				print("*" * 10, api_id, "starts running", "*" * 10)
				
				print("search head")
				first_tweet = True
				since_id = start_id_list[api_id]
				for tweet in tweepy.Cursor(api.search, q="place:%s" % places_id[api_id], lang=lang, count=count,
										   since_id=since_id, result_type=result_type, tweet_mode=tweet_mode).items():
					if first_tweet:
						start_id_list[api_id] = tweet.id
						first_tweet = False
					
					total_tweet_count[api_id] += 1
					
					# output to db
					couch[places_name[api_id].lower()].save(tweet._json)
				
				if hit_bottom_list[api_id]:
					print("Already hit bottom before, don't need to search tail")
				
				else:
					# successfully finish searching head and still has limit
					print("*" * 10, api_id, "keeps running", "*" * 10)
					time.sleep(5)
					
					print("search tail")
					max_id = max_id_list[api_id]
					for tweet in tweepy.Cursor(api.search, q="place:%s" % places_id[api_id], lang=lang, count=count,
											   max_id=max_id, result_type=result_type, tweet_mode=tweet_mode).items():
						max_id = tweet.id
						
						total_tweet_count[api_id] += 1
						
						# output to db
						couch[places_name[api_id].lower()].save(tweet._json)
					
					# if search out all the tweet
					hit_bottom_list[api_id] = False
					raise tweepy.error.TweepError("Hit the bottom")
		
		
		except tweepy.error.TweepError as e:
			max_id_list[api_id] = tweet.id
			print("last tweet", tweet.id)
			print(api_id, str(e))
			print(api_id, "total_tweet_count", total_tweet_count[api_id])
			reset_time_list[api_id] = api.rate_limit_status()["resources"]["search"]['/search/tweets']["reset"]
			print("reset time", reset_time_list[api_id])
			
			# log
			log_info = {}
			log_info["max_id_list"] = max_id_list
			log_info["start_id_list"] = start_id_list
			log_info["reset_time_list"] = reset_time_list
			log_info["total_tweet_count"] = total_tweet_count
			log_info["hit_bottom_list"] = hit_bottom_list
			with open("log.json", "w", encoding="utf-8") as k:
				json.dump(log_info, k)
			
			# switch to next api
			api_id = (api_id + 1) % num_api
			print("switch to api", api_id)
			while True:
				if time.time() >= reset_time_list[api_id]:
					api = api_launch(api_id)
					break
				else:
					print("wait for the next api, remain time", int(reset_time_list[api_id] - time.time()) + 3)
					if int(reset_time_list[api_id] - time.time()) > 300:
						time.sleep(300)
					else:
						time.sleep(int(reset_time_list[api_id] - time.time()) + 3)


if __name__ == "__main__":
	crawl(5, ["Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide"], "http://admin:1111@172.26.130.31:5984")
