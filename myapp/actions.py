import os
import datetime
import logging
import time
import json

from lib.BeautifulSoup import BeautifulSoup, NavigableString
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *

class IndexHandler(webapp.RequestHandler):
	def get(self):
		# Do some processing                
		template_values = {
			'sitename': 'asdf' 
		}
		path = os.path.join(os.path.dirname(__file__) + '/../templates/', 'index.html')
		self.response.out.write(template.render(path, template_values))

class FooHandler(webapp.RequestHandler):
	def get(self):
		logging.debug("start of handler")
		
class GrabTweetsHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		pagename = 'NULL'
		search_url = 'http://search.twitter.com/search.json?geocode=51.751944%2C-1.257778%2C10km'
		self.response.out.write('About to access: %s\n' % search_url)
		f = urlfetch.fetch(url=search_url)
		
		if f.status_code == 200:
			j = json.loads(f.content)
			for result in j['results']:
				tweets_of_this_id = db.GqlQuery("SELECT * FROM Tweet WHERE tweet_id = :1", result['id'])
				
				if tweets_of_this_id.count == 0:
					self.response.out.write("\n\nTweet #%s not present in datastore\n" % result['id'] )
					self.response.out.write(result)
					tweet = Tweet(tweet_id = result['id'], 
									raw_tweet_json = json.dumps(result), 
									tweet_content = result['text'])
					tweet.put();
				else:
					self.response.out.write("\n\nTweet #%u IS present in datastore\n" % result['id'])