import pytest
import uuid
from tweets import storage as s

node_name = "test_joe"


def clear_globals():
    s.Storage._tweets.clear()

@pytest.fixture
def populate_tweets():

    tweet_1 = {'id': uuid.uuid4(), 'tweet': 'Tweet 1', 'name': node_name}
    tweet_2 = {'id': uuid.uuid4(), 'tweet': 'Tweet 2', 'name': node_name}

    s.Storage._tweets.append(tweet_1)
    s.Storage._tweets.append(tweet_2)

    return [tweet_1, tweet_2]


class TestStorage:

    def test_save_tweet(self):

        tweet_content_1 = "Tweet test 1"
        tweet = s.Storage.save_tweet(tweet_content_1, node_name)

        assert len(s.Storage._tweets) == 1
        assert tweet['tweet'] == tweet_content_1
        assert tweet['name'] == node_name

        tweet_content_2 = "Tweet test 2"
        tweet = s.Storage.save_tweet(tweet_content_2, node_name)

        assert len(s.Storage._tweets) == 2
        assert tweet['tweet'] == tweet_content_2
        assert tweet['name'] == node_name

        clear_globals()

    def test_get_tweets(self, populate_tweets):

        tweets = s.Storage.get_tweets()

        assert type(tweets) == list
        assert len(tweets) == 2

        t1 = tweets[0]
        t2 = tweets[1]

        assert t1['id'] == populate_tweets[0]['id']
        assert t2['id'] == populate_tweets[1]['id']

        assert t1['name'] == node_name
        assert t2['name'] == node_name

        assert t1['tweet'] == populate_tweets[0]['tweet']
        assert t2['tweet'] == populate_tweets[1]['tweet']

        clear_globals()

    def test_get_tweet(self, populate_tweets):
        tweet = s.Storage.get_tweet(str(populate_tweets[0]['id']))

        assert type(tweet) == dict

        assert tweet['id'] == populate_tweets[0]['id']
        assert tweet['name'] == node_name
        assert tweet['tweet'] == populate_tweets[0]['tweet']

        clear_globals()

    def test_delete_tweet(self, populate_tweets):
        tweet = s.Storage.delete_tweet(str(populate_tweets[0]['id']))

        assert type(tweet) == dict

        assert tweet['id'] == populate_tweets[0]['id']
        assert tweet['name'] == node_name
        assert tweet['tweet'] == populate_tweets[0]['tweet']
        assert len(s.Storage._tweets) == 1

        clear_globals()
