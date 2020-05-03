import tweepy

consumer_key = ["JLkfNSC0HZvV1pcMDpp6nmFy5", "iZuJDgOde44yDNe90WPQQf2Ec", "kEJRwDBQPGCZdbWE6FX5vvDn7",
				"VIGCO4EJwtosb53rQRgnqKrge", "YQHjKbr7C5kYOXYNZShfPY2Y1"]
consumer_secret = ["bvSKMhyUoqmrDOEKiviOfEfJ0dt1Q9lkT9gn5D06tiCoSsT7st",
				   "Y0LU9elbal8sfU8hpb4eurko7fCVNnApVffCI3U7APdEHm3mCe",
				   "JHnxs3ow5KuofwhpLVA9p7GIipwXIKFkWondBP7RrOiFwJ1dvr",
				   "6HIxqovOMPD7BQKSi85t7TiEh17VHNostpOVYR6NMSC6kNQcBL",
				   "T1LD28dAoMhqam6q9BCJzd0lEcdQGscnQ8ajEDzb8SyubqxEtE"]

access_token = ["1253946379602243584-SNo1fvSLjzaLIhwGrnz9083Str7iAq",
				"1253946379602243584-f43So0yMKvEhwJoCGz0NRnOlXIookN",
				"1253946379602243584-BUdGrq9sQZ2twgVRwgg2hccZYdYrME",
				"1253946379602243584-MPNIYnjGNDMNOesKL2Hjhl7dryjiMv",
				"1253946379602243584-5QT5OioVQTOD9L5QJlXHQHoiDRroRH"]
access_token_secret = ["IIkhIswDGhOrFt6uhFEIsmgD7iYwH8FMxmqcMAx6LDmXv", "Gn1eJRf9aNBhHYQoFqfHIIMRO7CXuuJEwO1W7isNrS9T3",
					   "DwWZH3uY8V67k2HTgmO42UyWxiEQuI4bslBkGQ8WmxCYD", "e0KS6L5JT72OaFigz9Wi2y31FX3svSF1nKt0tar1nHyKE",
					   "mesapsZJBFN9PWvRKV1zovbmrlbfgLkDahxidUIdUz97c"]


def api_launch(api_id):
	auth = tweepy.OAuthHandler(consumer_key[api_id], consumer_secret[api_id])
	auth.set_access_token(access_token[api_id], access_token_secret[api_id])
	
	api = tweepy.API(auth)
	
	return (api)


if __name__ == "__main__":
	for i in range(5):
		api_launch(i)
		print(i, "Success connect")
