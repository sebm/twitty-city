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
from TidyUpHandler import *

class IndexHandler(webapp.RequestHandler):
	def get(self):
		a = AnalysesHandler()

		analyses_gdata = AnalysisGData.gql("ORDER BY created_at DESC LIMIT 0,1")
		
							
		template_values = {
			'gdata': analyses_gdata[0].gdatas,
			'BristolSentiment': "%.2f" % a.getAnalysisForPlace('Bristol'), 
			'OxfordSentiment': "%.2f" % a.getAnalysisForPlace('Oxford'), 
			'LondonSentiment': "%.2f" % a.getAnalysisForPlace('London'), 
			'YorkSentiment': "%.2f" % a.getAnalysisForPlace('York'), 
			'MargateSentiment': "%.2f" %  a.getAnalysisForPlace('Margate'), 
			'BristolImg': a.getImageForScore(a.getAnalysisForPlace('Bristol')), 
			'OxfordImg': a.getImageForScore(a.getAnalysisForPlace('Oxford')), 
			'LondonImg': a.getImageForScore(a.getAnalysisForPlace('London')), 
			'YorkImg': a.getImageForScore(a.getAnalysisForPlace('York')), 
			'MargateImg': a.getImageForScore(a.getAnalysisForPlace('Margate')), 
			'sitename': "Twitty City"
		}
		path = os.path.join(os.path.dirname(__file__) + '/../templates/', 'index.html')
			
		self.response.out.write(template.render(path, template_values))
