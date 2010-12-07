import os
from datetime import datetime
import logging
import time
import sys

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *
from GrabTweetsHandler import *
from GrabAnalysisHandler import *
from AnalysesHandler import *

class IndexHandler(webapp.RequestHandler):
	def get(self):
		a = AnalysesHandler()

		template_values = {
			'TorontoSentiment': a.getAnalysis('Toronto'), 
			'OxfordSentiment': a.getAnalysis('Oxford'), 
			'LondonSentiment': a.getAnalysis('London'), 
			'NYCSentiment': a.getAnalysis('NYC'), 
			'MargateSentiment': a.getAnalysis('Margate'), 
			'TorontoImg': a.getImage(a.getAnalysis('Toronto')), 
			'OxfordImg': a.getImage(a.getAnalysis('Oxford')), 
			'LondonImg': a.getImage(a.getAnalysis('London')), 
			'NYCImg': a.getImage(a.getAnalysis('NYC')), 
			'MargateImg': a.getImage(a.getAnalysis('Margate')), 
			'sitename': "Twitter Sentiment Worldwide"
		}
		path = os.path.join(os.path.dirname(__file__) + '/../templates/', 'index.html')
			
		self.response.out.write(template.render(path, template_values))
