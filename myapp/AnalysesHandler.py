import os
from datetime import datetime, timedelta
import logging
import time
import json
import csv 
import urllib

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *

class AnalysesHandler(webapp.RequestHandler):
	def get(self):
		myplace = self.request.get('place')
		
		