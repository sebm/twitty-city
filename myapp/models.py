from google.appengine.ext import db

class Tweet(db.Model):
    tweet_id = db.IntegerProperty(required=True)
    raw_tweet_json = db.TextProperty(required=True)
    tweet_content = db.StringProperty(required=True)