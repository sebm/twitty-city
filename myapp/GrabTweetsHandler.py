from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from django.utils import simplejson as json
from models import *
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime

class GrabTweetsHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"

		myplace = self.request.get('place')
		
		if myplace == 'Oxford':
			search_url = 'http://search.twitter.com/search.json?geocode=51.751944%2C-1.257778%2C10km'
		elif myplace == 'London':
			search_url = 'http://search.twitter.com/search.json?geocode=51.511676%2C-0.133209%2C10km'
		elif myplace == 'NYC':
			search_url = 'http://search.twitter.com/search.json?geocode=40.717711%2C-74.00150%2C10km'
		elif myplace == 'Margate':
			search_url = 'http://search.twitter.com/search.json?geocode=51.382681%2C1.3664245%2C10km'
		elif myplace == 'Toronto':
			search_url = 'http://search.twitter.com/search.json?geocode=43.716589%2C-79.340686%2C10km'
		else:
			self.response.out.write("Please provide a 'place' parameter: Oxford, London, NYC, Toronto or Margate.")
			
		self.response.out.write('About to access: %s\n\n' % search_url)
		f = urlfetch.fetch(url=search_url)
		
		if f.status_code == 200:
			j = json.loads(f.content)
			for result in j['results']:
				self.response.out.write(result)
				self.response.out.write('\n')
				if (result['id']):
					same_id = Tweet.gql('WHERE tweet_id = :1', result['id'])
					
					if (same_id.count() > 0):
						self.response.out.write('Tweet id #%s exists in the datastore\n' % result['id'])
					else:
						self.response.out.write('Adding tweet id #%s to datastore\n' % result['id'])
						tweet = Tweet(tweet_id = result['id'], 
							raw_tweet_json = json.dumps(result), 
							tweet_content = result['text'],
							place = myplace,
							created_at = datetime.fromtimestamp(mktime_tz(parsedate_tz(result['created_at'])))
						)
						
						tweet.put()
						
		elif f.status_code == 400:
			self.response.out.write('UHOH! You have hit the rate limit...')
