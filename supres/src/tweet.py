import tweepy
import git_twitter_access

api_key = git_twitter_access.twitter_credentials["api_key"]
api_key_secret = git_twitter_access.twitter_credentials["api_key_secret"]
access_token = git_twitter_access.twitter_credentials["access_token"]
access_token_secret = git_twitter_access.twitter_credentials["access_token_secret"]
authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticator, wait_on_rate_limit=True)


def send_tweet(media, tweet):
    """
    This function sends a tweet with media attached using the Twitter API.

    :param media: The media parameter is the file path or URL of the image or video that you want to
    attach to the tweet. It can be a local file path or a URL to an image or video hosted online
    :param tweet: The tweet parameter is a string that represents the text content of the tweet that you
    want to post. It can be up to 280 characters long
    :return: the result of calling the `update_with_media` method of the `api` object with the `media`
    and `tweet` arguments. The specific value being returned depends on the implementation of the
    `update_with_media` method, but it is likely to be a response object or a status code indicating the
    success or failure of the tweet update.
    """
    return api.update_with_media(media, tweet)


def is_image_tweet():
    """
    This function retrieves the last tweet of a specified user and returns it.
    :return: The function `is_image_tweet()` returns the last status (tweet) of a Twitter user with the
    specified screen name, which is obtained using the `api.user_timeline()` method.
    """
    get_last_status = api.user_timeline(
        screen_name=git_twitter_access.user_handle, count=1
    )
    return get_last_status[0]
