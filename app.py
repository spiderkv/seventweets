from flask import Flask, jsonify, request

from tweets.storage import Storage
from tweets.tweet import Tweet

app = Flask(__name__)

HEADERS = {'Content-Type': 'application/json; charset=utf=8'}


@app.route("/tweets", methods=['GET'])
def get_tweets():
    return jsonify([tweet.to_dict() for tweet in Storage.get_tweets()]), 200, HEADERS


@app.route("/tweets/<tweet_id>", methods=['GET'])
def get_tweet(tweet_id):
    tweet = Storage.get_tweet(tweet_id)
    return jsonify(tweet.to_dict()), 200, HEADERS if tweet else ("NOT FOUND", 404, HEADERS)


@app.route("/tweets", methods=['POST'])
def create_tweet():
    if 'tweet' in request.form:
        tweet = Storage.save_tweet(request.form['tweet'])
        return jsonify(tweet.to_dict()), 201, HEADERS
    else:
        return "BAD REQUEST", 400, HEADERS


@app.route("/tweets/<tweet_id>", methods=['DELETE'])
def delete_tweet(tweet_id):
    tweet = Storage.delete_tweet(tweet_id)
    return jsonify(tweet.to_dict()), 200, HEADERS

if __name__ == "__main__":
    app.run(host="0.0.0.0")
