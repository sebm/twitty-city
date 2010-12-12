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
from AnalysesHandler import *

class AnalysisHistoryHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers["Content-Type"] = "text/plain"
		
		a = AnalysesHandler()
		
		analyses = a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('Toronto', 7)) + \
							a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('NYC', 7)) + \
							a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('London', 7)) + \
							a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('Margate', 7)) + \
							a.getGDataForAnalyses(a.getDaysOfAnalysisForPlace('Oxford', 7))
		self.response.out.write(analyses)