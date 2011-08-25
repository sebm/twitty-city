from google.appengine.ext import db

class Tweet(db.Model):
		tweet_id = db.IntegerProperty(required=True)
		tweet_content = db.StringProperty(required=True, multiline=True)
		place = db.StringProperty()
		created_at = db.DateTimeProperty()
		
class Analysis(db.Model):
		created_at = db.DateTimeProperty(required=True)
		place = db.StringProperty(required=True)
		avg_sentiment = db.FloatProperty(required=True)
		
class AnalysisGData(db.Model):
		created_at = db.DateTimeProperty(required=True)
		gdatas = db.TextProperty(required=True)