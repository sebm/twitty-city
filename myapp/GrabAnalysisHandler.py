import os
from datetime import datetime, timedelta
import logging
import time
import json
import csv 

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *

class GrabAnalysisHandler(webapp.RequestHandler):
	def get(self):

		bulk_analysis_url = 'http://twittersentiment.appspot.com/api/bulkClassify'

		self.response.headers["Content-Type"] = "text/plain"

		myplace = self.request.get('place')
		places = ['Oxford', 'London', 'NYC', 'Margate']
		
		if not myplace in places:
			self.response.out.write("Please provide a 'place' parameter: Oxford, London, NYC or Margate.")
		else:
			# get the last hour's worth of tweets from our DB, for that place.
			one_hour_ago = datetime.now() + timedelta(hours=-1)
			tweets = Tweet.gql('WHERE place = :place AND created_at > :after', 
													place=myplace, after=one_hour_ago )

			if tweets.count() > 0:
				number_of_tweets = tweets.count()
				an_hour_of_tweets = ''
				for t in tweets:
					an_hour_of_tweets += t.tweet_content + '\n'
				
				self.response.out.write(an_hour_of_tweets)
				
				f = urlfetch.fetch(url=bulk_analysis_url, method='POST', payload=an_hour_of_tweets)

				if not f.status_code == 200:
					self.response.out.write("Couldn't successfully access the sentiment API")
				else:
					rows = f.content.split('\n')
					running_total = 0
					for row in rows:
						if not row == '': 
							score = int(row.split(',')[0].strip('"'))
							running_total += score
							
					self.response.out.write("The running total is %s and there were tweets" % running_total)
