import tweepy

consumer_key = ["JLkfNSC0HZvV1pcMDpp6nmFy5","ctWiUJKtUxhun8mS7Lud9BYDX","kEJRwDBQPGCZdbWE6FX5vvDn7","VIGCO4EJwtosb53rQRgnqKrge"]
consumer_secret = ["bvSKMhyUoqmrDOEKiviOfEfJ0dt1Q9lkT9gn5D06tiCoSsT7st","gpEE4UyNshRZCbinR4yvNVRCr6hu6LRTVlTCvHXLWeHIIRkI7e","JHnxs3ow5KuofwhpLVA9p7GIipwXIKFkWondBP7RrOiFwJ1dvr","6HIxqovOMPD7BQKSi85t7TiEh17VHNostpOVYR6NMSC6kNQcBL"]

access_token = ["1253946379602243584-SNo1fvSLjzaLIhwGrnz9083Str7iAq","1247737787085762562-fiQXT5hZHoPd7z2sbtRyyRfSLU9lRo","1253946379602243584-BUdGrq9sQZ2twgVRwgg2hccZYdYrME","1253946379602243584-MPNIYnjGNDMNOesKL2Hjhl7dryjiMv"]
access_token_secret = ["IIkhIswDGhOrFt6uhFEIsmgD7iYwH8FMxmqcMAx6LDmXv","ZHmQFTHfWe0LYummy1hVbANvZcWSa4ck3MCKJJB4gigiY","DwWZH3uY8V67k2HTgmO42UyWxiEQuI4bslBkGQ8WmxCYD","e0KS6L5JT72OaFigz9Wi2y31FX3svSF1nKt0tar1nHyKE"]

def api_launch(api_id):
    
    auth = tweepy.OAuthHandler(consumer_key[api_id], consumer_secret[api_id])
    auth.set_access_token(access_token[api_id], access_token_secret[api_id])
    
    api = tweepy.API(auth)
    
    return(api)

au_bounds = [110.390625, -44.276671273775165, 155.56640625, -11.005904459659451]