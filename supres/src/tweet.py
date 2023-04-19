import tweepy
import git_twitter_access

api_key = git_twitter_access.twitter_credentials["api_key"]
api_key_secret = git_twitter_access.twitter_credentials["api_key_secret"]
access_token = git_twitter_access.twitter_credentials["access_token"]
access_token_secret = git_twitter_access.twitter_credentials["access_token_secret"]
authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticator, wait_on_rate_limit=True)


def send_tweet(media: str, tweet: str) -> dict:
    """
    Uploads an image or video to Twitter and creates a tweet with it.

    Args:
        media (str): The path to the media file to be uploaded.
        tweet (str): The text content of the tweet.

    Returns:
        dict: A dictionary containing information about the created tweet.
    """
    return api.update_with_media(media, tweet)


def is_image_tweet():
    """
    Checks if the latest tweet by the specified user contains an image.

    Returns:
        tweepy.Status: The latest tweet by the user.
    """
    get_last_status = api.user_timeline(
        screen_name=git_twitter_access.user_handle, count=1
    )
    return get_last_status[0]
