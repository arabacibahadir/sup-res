# This is for tweeting through api.
import tweepy
import git_tw_access.py  # Change this 

api_key = twaccess.tw_api
api_key_secret = twaccess.tw_key_secret
access_token = twaccess.tw_token
access_token_secret = twaccess.tw_token_secret
authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticator, wait_on_rate_limit=True)


def send_tweet(media, tweet):
    return api.update_with_media(media, tweet)


def is_image_tweet():
    stat = api.user_timeline(screen_name='@sup_res', count=1)
    return stat[0]
