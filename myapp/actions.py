import os
from datetime import datetime
import logging
import time
import json

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *
from GrabTweetsHandler import *
from GrabAnalysisHandler import *

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
		
		