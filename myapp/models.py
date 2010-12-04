from google.appengine.ext import db

class Tweet(db.Model):
		tweet_id = db.IntegerProperty(required=True)
		raw_tweet_json = db.TextProperty(required=True)
		tweet_content = db.StringProperty(required=True, multiline=True)
		place = db.StringProperty()
		created_at = db.DateTimeProperty()
		
class Analysis(db.Model):
		start_time = db.DateTimeProperty()
		end_time = db.DateTimeProperty()