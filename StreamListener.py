import json
import time
import tweepy
import config



class StreamListener(tweepy.StreamListener):
    au_bounds = config.au_bounds;

    # convert
    def convert(self, obj):
        id_str = obj['id_str']
        try:
            text = obj['extended_tweet']['full_text']
        except Exception:
            text = obj['full_text'] if 'full_text' in obj else obj['text']

        db_data = {**obj, "text": text, "_id": id_str}
        return db_data

    # get coord from tweet
    def get_coords(self, obj):
        coords = None
        try:
            coords = obj["geo"]["coordinates"]
        except Exception:
            try:
                coords_raw = obj["coordinates"]["coordinates"]
                if isinstance(coords_raw, list):
                    coords = coords_raw
            except Exception:
                pass
        return coords

    # once complete grabbing tweets from an user, mark user as done
    def user_exists(self, user_id):
        couch = StreamListener.couch
        db = couch.get_database(name="users")

        try:
            db.get(user_id)
        except:
            self.couch.saveUser({"_id": user_id})
            # start digging this user, save in db so next time we know to skip himm
            return False
        else:
            # user in db , means we have digged before
            return True

    def get_place_coord(self, points):
        col_totals = [sum(x) / len(points) for x in zip(*points)]
        col_totals.reverse()
        return col_totals

    # Method to check if tweet is posted in Australia
    def is_au(self, coordinates):
        if coordinates is not None and coordinates[0] and coordinates[1]:
            lat = float(coordinates[0])
            lng = float(coordinates[1])
            return self.au_bounds[3] >= lat >= self.au_bounds[1] and self.au_bounds[2] >= lng >= self.au_bounds[0]

    def handle_tweet(self, obj):
        coordinates = self.get_coords(obj)
        if not coordinates:
            if obj["place"] is not None:
                try:
                    place_coord = obj["place"]["bounding_box"]["coordinates"][0]
                    coordinates = self.get_place_coord(place_coord)
                except Exception as e:
                    print(e)
                    pass
        if coordinates:
            if self.is_au(coordinates):
                db_data = self.convert(obj)
                # todo analyzer
                # analysis = {}

                db_data["coordinates"] = coordinates
                self.couch.saveTweet(db_data)
                return True
            else:
                print("not in au", coordinates)
        return False

    # Method used to return user's history tweets through api.user_timeline wrapped in tweepy.Cursor
    def get_user_tweets(self, user_id):
        try:
            # 900 / 180 * 20  = 100
            # quota for user timeline is 900 every 15min
            # to use it fully, we can dig 100 user tweets
            tweets = tweepy.Cursor(StreamListener.api.user_timeline, user_id=user_id, tweet_mode="extended",
                                   exclude_replies=True).items(100)
        except tweepy.RateLimitError as e:
            print("RateLimitError", e)
            time.sleep(60)
        except Exception as e:
            print("user timeline general exception", e)
        else:
            pass

        for tweet in tweets:
            tweet_json = tweet._json
            if tweet_json is not None:
                self.handle_tweet(tweet_json)

    # When a streaming data comes in
    def on_data(self, raw_data):
        json_dict = json.loads(raw_data)
        has_coord = self.handle_tweet(json_dict)
        if has_coord :
            user_id = json_dict["user"]["id_str"]
            if not self.user_exists(user_id):
                print("start digging user tweet", user_id)
                self.get_user_tweets(user_id)

    # Error code
    @staticmethod
    def on_error(status_code):
        print(status_code)
