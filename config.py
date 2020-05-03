import tweepy

consumer_key = ["4KAUitGIKfaJFsVoOcfkueDht","IQMp8rrFFCOBc5po8sBRurDxG","ExDU4DRSw7DhQ88UTWws5RdIU","Yi2OYOBYRBtrgX8syO5CWrB2Q"]
consumer_secret = ["BqMa7ZuSKYx2TrxcfAtzDQYovzMLOhAAVaQHm3qY9hEhCy0FhX","hJFhRpwyelUjeLDTc3eKPITaOeyBwHl07QVfZxI5FdAuhqFQJq","xOAKyaGvjJcvzSyZC3lNvp5Jof7jLQPjAtajAPfALhlb9agxd4","3NFZdjVVU1BgyRd0rxE8NLX7wrlcnDVS61XkO51KuY2xNv41Ru"]

access_token = ["4781445212-zXdPzSwXnVxE2Y1zTuUNifm2PZ95D9ErgTQF3zB","4781445212-EwfY0Ohl2m3YOFKyYp7pMKq1yOW5muEPXamcg6x","4781445212-LGH2zA6wkx6m2fCBGApCrJi3UHZ2DR12l2Y43gm","4781445212-VvkmJkQrW2JLOvPFfh8kSaLaOdAixZAsPf0PYWR"]
access_token_secret = ["c2F19xopOphiiBRW9JHJHFb08peyUfYZR5i5RqDxe1xsK","oFuP0lYktT9xy9uT6zcwg1CuNEiIgk4YH0iTSZdATYhoP","iBRDlSF4Dtwe7qQhJicJYSNr2Qa1RGOpebu6HHvgTMORB","JRowIP2u8v10nOA0ZgSzV9leI5oc9Q1yEAEpTlKi6C9Pj"]

def api_launch(api_id):
    
    auth = tweepy.OAuthHandler(consumer_key[api_id], consumer_secret[api_id])
    auth.set_access_token(access_token[api_id], access_token_secret[api_id])
    
    api = tweepy.API(auth)
    
    return(api)

# https://gist.github.com/graydon/11198540
au_bounds = [113.338953078, -43.6345972634, 153.569469029, -10.6681857235]