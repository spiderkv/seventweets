import uuid, pg8000, functools
from tweets.tweet import Tweet
from tweets.config import Config


def uses_db(f):
    @functools.wraps(f)
    def wrapper(cls, *args, **kwargs):
        cursor = cls._conn.cursor()
        res = f(cls, cursor, *args, **kwargs)
        cursor.close()
        cls._conn.commit()
        return res

    return wrapper

class Storage(object):

    _conn = pg8000.connect(**Config.DB_CONFIG)

    _tweets = []

    @classmethod
    @uses_db
    def get_tweets(cls, cursor):
        cursor.execute(
            """
            SELECT id, name, tweet FROM tweets
            """
        )
        tweets = [Tweet(*data) for data in cursor.fetchall()]
        return tweets

    @classmethod
    @uses_db
    def get_tweet(cls, cursor, tweet_id):
        cursor.execute(
            """
            SELECT id, name, tweet FROM tweets
            WHERE id=%s
            """,
            (tweet_id,)
        )
        res = cursor.fetchone()
        return Tweet(*res)

    @classmethod
    @uses_db
    def save_tweet(cls, cursor, tweet_content):
        cursor.execute(
            """
            INSERT INTO tweets (name, tweet) VALUES (%s, %s) RETURNING id, name, tweet
            """,
            (Config.NAME, tweet_content)
        )
        data = cursor.fetchone()
        new_tweet = Tweet(*data)
        return new_tweet

    @classmethod
    @uses_db
    def delete_tweet(cls, cursor, tweet_id):
        tweet = cls.get_tweet(tweet_id)
        if tweet:
            cursor.execute(
                """DELETE FROM tweets WHERE id = %s""",
                (tweet_id,)
            )
        return tweet
