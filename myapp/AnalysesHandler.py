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
