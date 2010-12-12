import os
from datetime import datetime, timedelta
import logging
import time
import csv 
import urllib
import sys

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *

class AnalysesHandler():
	places = ['Oxford', 'London', 'NYC', 'Margate', 'Toronto']
	invalid_place_string = "Please provide a 'place' parameter: Oxford, London, Toronto, NYC or Margate."
	
	def getDaysOfAnalysisForPlace(self, myplace, days):		
		if myplace in self.places:
			x_days_ago = datetime.now() + timedelta(days=-days)
			analyses = Analysis.gql('WHERE place = :place AND created_at > :after', 
													place=myplace, after=x_days_ago )
			
			return analyses

	def getGDataForAnalyses(self, analyses):
		format_strings = {
			'Toronto': '[new Date(%s, %s, %s, %s, %s), %s, undefined, undefined, undefined, undefined], \n',
			'NYC': '[new Date(%s, %s, %s, %s, %s), undefined, %s, undefined, undefined, undefined], \n',
			'Oxford': '[new Date(%s, %s, %s, %s, %s), undefined, undefined, %s, undefined, undefined], \n',
			'Margate': '[new Date(%s, %s, %s, %s, %s), undefined, undefined, undefined, %s, undefined], \n',
			'London': '[new Date(%s, %s, %s, %s, %s), undefined, undefined, undefined, undefined, %s], \n'
		}
		
		gdatas = ''
		for a in analyses:
			formatString = format_strings.get(a.place)
							
			gdatas += formatString	% (a.created_at.year, a.created_at.month-1, a.created_at.day, a.created_at.hour, a.created_at.minute, a.avg_sentiment)

		return gdatas
		
	
	def runAnalysisForPlace(self, myplace, response):
		
		bulk_analysis_url = 'http://twittersentiment.appspot.com/api/bulkClassify'
		
		if not myplace in self.places:
			response.out.write(self.invalid_place_string)
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
				
				an_hour_of_tweets = an_hour_of_tweets.encode('utf8','xmlcharrefreplace')
				headers = {'Content-Type' : 'text/plain ; charset = utf-8'}
				f = urlfetch.fetch(url=bulk_analysis_url, method='POST', payload=an_hour_of_tweets)

				if not f.status_code == 200:
					response.out.write("Couldn't successfully access the sentiment API")
				else:
					rows = f.content.split('\n')
					running_total = 0
					for row in rows:
						if not row == '': 
							score = int(row.split(',')[0].strip('"'))
							running_total += score
							
					avg_sentiment = float(running_total) / number_of_tweets

					response.out.write(
						"The running total is %s and there were %s tweets. The average sentiment is %f" %
						(running_total, number_of_tweets, avg_sentiment)
					)
					analysis = Analysis(created_at=datetime.now(), place=myplace, avg_sentiment=avg_sentiment)
					analysis.put()
	
	def getAnalysisForPlace(self, myplace):		
		latest_analysis = Analysis.gql("WHERE place = :place ORDER BY created_at DESC LIMIT 1",
												place=myplace
											)
		return(latest_analysis[0].avg_sentiment)
	def getImageForScore(self, myscore):
		if myscore < 2.2:
			return "1.png"
		elif myscore < 2.4:
			return "2.png"
		elif myscore < 2.6:
			return "3.png"
		elif myscore < 2.8:
			return "4.png"
		else:
			return "5.png"
