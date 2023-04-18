import os
import pytest
import tweepy
import git_twitter_access
from unittest import mock

from tweet import send_tweet, is_image_tweet


@pytest.fixture
def api():
    api_key = git_twitter_access.twitter_credentials["api_key"]
    api_key_secret = git_twitter_access.twitter_credentials["api_key_secret"]
    access_token = git_twitter_access.twitter_credentials["access_token"]
    access_token_secret = git_twitter_access.twitter_credentials["access_token_secret"]
    authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
    authenticator.set_access_token(access_token, access_token_secret)
    api = tweepy.API(authenticator, wait_on_rate_limit=True)
    return api


@pytest.fixture
def image_file():
    return os.path.join(os.path.dirname(__file__), "test_image.png")


def test_send_tweet(api, image_file):
    with mock.patch.object(api, "update_with_media") as mock_update_with_media:
        tweet = "Test tweet"
        send_tweet(image_file, tweet)
        mock_update_with_media.assert_called_once_with(image_file, tweet)


def test_is_image_tweet(api):
    with mock.patch.object(api, "user_timeline") as mock_user_timeline:
        tweet = tweepy.models.Status()
        tweet.entities = {"media": [{"type": "photo"}]}
        mock_user_timeline.return_value = [tweet]
        assert is_image_tweet() == tweet
