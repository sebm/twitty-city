import os
from datetime import datetime, timedelta
import logging
import time
import csv
import urllib

from email.utils import parsedate_tz, mktime_tz
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from django.utils import simplejson as json
from models import *
from AnalysesHandler import *


class GrabAnalysisHandler(webapp.RequestHandler):
    def get(self):
        a = AnalysesHandler()

        self.response.headers["Content-Type"] = "text/plain"
        myplace = self.request.get('place')
        a.runAnalysisForPlace(myplace, self.response)
