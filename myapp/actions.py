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
from AnalysisHistoryHandler import *

class IndexHandler(webapp.RequestHandler):
	def get(self):
		a = AnalysesHandler()

		analyses_gdata = AnalysisGData.gql("ORDER BY created_at DESC LIMIT 0,1")
		
							
		template_values = {
			'gdata': analyses_gdata[0].gdatas,
			'TorontoSentiment': "%.2f" % a.getAnalysisForPlace('Toronto'), 
			'OxfordSentiment': "%.2f" % a.getAnalysisForPlace('Oxford'), 
			'LondonSentiment': "%.2f" % a.getAnalysisForPlace('London'), 
			'NYCSentiment': "%.2f" % a.getAnalysisForPlace('NYC'), 
			'MargateSentiment': "%.2f" %  a.getAnalysisForPlace('Margate'), 
			'TorontoImg': a.getImageForScore(a.getAnalysisForPlace('Toronto')), 
			'OxfordImg': a.getImageForScore(a.getAnalysisForPlace('Oxford')), 
			'LondonImg': a.getImageForScore(a.getAnalysisForPlace('London')), 
			'NYCImg': a.getImageForScore(a.getAnalysisForPlace('NYC')), 
			'MargateImg': a.getImageForScore(a.getAnalysisForPlace('Margate')), 
			'sitename': "Twitty City"
		}
		path = os.path.join(os.path.dirname(__file__) + '/../templates/', 'index.html')
			
		self.response.out.write(template.render(path, template_values))
