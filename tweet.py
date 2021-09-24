# This is for tweeting through api.

import tweepy
import twaccess

api_key = twaccess.tw_api
api_key_secret = twaccess.tw_key_secret
access_token = twaccess.tw_token
access_token_secret = twaccess.tw_token_secret
authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)

api = tweepy.API(authenticator, wait_on_rate_limit=True)


def send_tweet(media,tweet):
    return api.update_with_media(media,tweet)

