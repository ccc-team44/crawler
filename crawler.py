from config import api_launch
import tweepy
import time


def crawl(num_api,
        places_name = None,
        query = "*",
        lang = "en",
        count = 100,
        result_type = "recent",
        geocode = None,
        max_id = None,
        since_id = None,
        tweet_mode="extended",
        rate_limit = 180,
        wall_time = 900,
        host = None,
        log = None):

    if num_api != len(places_name):
        print("error")
        return(None)
    
    api_id = 1
    api = api_launch(api_id)

    places_id = []
    for name in places_name:
        for geo in api.geo_search(query = name, granularity="city"):
            places_id.append(geo.id)
            break
    
    max_id_list = [None] * num_api
    start_id_list = [None] * num_api
    
    reset_time_list = [-1] * num_api
    
    total_tweet_count = [0] * num_api

    while True:

        try:

            if max_id_list[api_id] == None:
                first_tweet = True

                # for test only
                content_print_time = 0 
                print("*"*10, api_id, "starts running","*"*10)

                for tweet in tweepy.Cursor(api.search, q = "place:%s" % places_id[api_id], lang = lang, count = count, max_id = max_id, result_type = result_type, tweet_mode=tweet_mode).items():
                    if first_tweet:
                        start_id_list[api_id] = tweet.id
                        first_tweet = False

                    total_tweet_count[api_id] += 1

                    # content # for test only
                    if content_print_time < 10:
                        create_time = tweet.created_at.strftime( '%Y-%m-%d %H:%M:%S %f' )
                        tweet_place = places_name[api_id]
                        print(tweet.id, create_time, tweet_place)
                        content_print_time += 1
            
            else:
                # search head
                
                # for test obly
                content_print_time = 0
                print("*"*10, api_id, "starts running","*"*10)

                print("search head")
                first_tweet = True
                since_id = start_id_list[api_id]
                for tweet in tweepy.Cursor(api.search, q = "place:%s" % places_id[api_id], lang = lang, count = count, since_id = since_id, result_type = result_type, tweet_mode=tweet_mode).items():
                    if first_tweet:
                        start_id_list[api_id] = tweet.id
                        first_tweet = False
                    
                    total_tweet_count[api_id] += 1

                    # content
                    if content_print_time < 10:
                        create_time = tweet.created_at.strftime( '%Y-%m-%d %H:%M:%S %f' )
                        tweet_place = places_name[api_id]
                        print(tweet.id, create_time, tweet_place)
                        content_print_time += 1
                
                # successfully finish searching head and still has limit
                print("*"*10, api_id, "keeps running","*"*10)
                time.sleep(5)

                # for test only
                content_print_time = 0

                print("search tail")
                max_id = max_id_list[api_id]
                for tweet in tweepy.Cursor(api.search, q = "place:%s" % places_id[api_id], lang = lang, count = count, max_id = max_id, result_type = result_type, tweet_mode=tweet_mode).items():
                    max_id = tweet.id

                    total_tweet_count[api_id] += 1

                    # content
                    if content_print_time < 10:
                        create_time = tweet.created_at.strftime( '%Y-%m-%d %H:%M:%S %f' )
                        tweet_place = places_name[api_id]
                        print(tweet.id, create_time, tweet_place)
                        content_print_time += 1


        except tweepy.error.TweepError as e:
            max_id_list[api_id] = tweet.id
            print("last tweet",tweet.id,create_time)
            print(api_id, str(e))
            print(api_id, "total_tweet_count", total_tweet_count[api_id])
            reset_time_list[api_id] = api.rate_limit_status()["resources"]["search"]['/search/tweets']["reset"]
            print("reset time", reset_time_list[api_id])

            # switch to next api
            api_id = (api_id + 1) % num_api
            print("switch to api", api_id)
            while True:
                if time.time() >= reset_time_list[api_id] :
                    api = api_launch(api_id)
                    break
                else:
                    print("wait for the next api, remain time", int(reset_time_list[api_id] - time.time())+3)
                    if int(reset_time_list[api_id] - time.time()) > 300:
                        time.sleep(300)
                    else:
                        time.sleep(int(reset_time_list[api_id] - time.time())+3)

                





if __name__ == "__main__":
    crawl(2, ["Melbourne","Sydney"])
    