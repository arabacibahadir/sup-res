# This is for tweeting through api.
import tweepy
import git_tw_access

api_key = git_tw_access.tw_api
api_key_secret = git_tw_access.tw_key_secret
access_token = git_tw_access.tw_token
access_token_secret = git_tw_access.tw_token_secret
authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticator, wait_on_rate_limit=True)


def send_tweet(media, tweet):
    """
    Send a tweet with an image attached
    :param media: The path to the media file (e.g. image)
    :param tweet: The text you want to tweet
    :return: The return value is a tweepy.models.Status object.
    """
    return api.update_with_media(media, tweet)


def is_image_tweet():
    """
    This is getting the latest tweet from the user.
    """
    stat = api.user_timeline(screen_name=git_tw_access.user_handle, count=1) # Change with your twitter handle name
    return stat[0]
