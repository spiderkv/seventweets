from flask import Flask, jsonify, request
from storage import Storage

app = Flask(__name__)

server_name = "john_doe"


@app.route("/tweets", methods=['GET'])
def get_tweets():
    return jsonify(Storage.get_tweets())


@app.route("/tweets/<tweet_id>", methods=['GET'])
def get_tweet(tweet_id):
    tweet = Storage.get_tweet(tweet_id)
    return jsonify(tweet) if tweet else ("NOT FOUND", 404)


@app.route("/tweets", methods=['POST'])
def create_tweet():
    if 'tweet' in request.form:
        global server_name
        tweet = Storage.save_tweet(request.form['tweet'], server_name)
        return jsonify(tweet), 201
    else:
        return "BAD REQUEST", 400


@app.route("/tweets/<tweet_id>", methods=['DELETE'])
def delete_tweet(tweet_id):
    tweet = Storage.delete_tweet(tweet_id)
    return jsonify(tweet), 204

if __name__ == "__main__":
    app.run()
