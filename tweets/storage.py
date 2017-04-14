import uuid


class Storage(object):

    _tweets = []

    @classmethod
    def get_tweets(cls):
        return cls._tweets

    @classmethod
    def get_tweet(cls, tweet_id):
        for tweet in cls._tweets:
            if str(tweet['id']) == tweet_id:
                return tweet
            else:
                return None

    @classmethod
    def save_tweet(cls, tweet_content, name):
        tweet = {'tweet': tweet_content, 'name': name, 'id': uuid.uuid4()}
        cls._tweets.append(tweet)
        return tweet

    @classmethod
    def delete_tweet(cls, tweet_id):
        tweet = cls.get_tweet(tweet_id)
        if tweet:
            cls._tweets.remove(tweet)

        return tweet
